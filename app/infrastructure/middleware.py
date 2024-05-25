from fastapi import FastAPI, Request
from jose import JWTError
from starlette.responses import JSONResponse

from app.api.dependencies import oauth2_scheme
from app.core.config import settings
from app.infrastructure.logging_config import logger
from app.infrastructure.token import validate_token

app = FastAPI()


def log_and_return_response(status_code: int, message: str):
    logger.error(message)
    return JSONResponse(status_code=status_code, content={"message": message})


@app.middleware("http")
async def add_sale_service_to_request(request: Request, call_next):
    try:
        if request.url.path.startswith("/api/v1/sales"):
            token = await oauth2_scheme(request)
            validate_token(token)
            request.state.sale_service = settings.ml_models["sale_service"]
        if request.url.path.startswith("/api/v1/users"):
            request.state.user_service = settings.ml_models["user_service"]

        response = await call_next(request)
        return response
    except AttributeError as e:
        return log_and_return_response(
            500, f"{request.url.path}: Internal server error {e}"
        )
    except JWTError as e:
        return log_and_return_response(
            401, f"{request.url.path}: Authorization invalid {e}"
        )
    except Exception as e:
        return log_and_return_response(
            500, f"{request.url.path}: Internal server error {e}"
        )
