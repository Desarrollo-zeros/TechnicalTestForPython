from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.dependencies import get_sale_service, oauth2_scheme, get_user_service
from app.api.endpoints import sales, user
from app.infrastructure.firebase_config import initialize_firebase
from app.infrastructure.middleware import add_sale_service_to_request
from app.infrastructure.logging_config import logger

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION_API,
)

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        settings.ml_models["sale_service"] = get_sale_service()
        settings.ml_models["user_service"] = get_user_service()
        _ = settings.ml_models["sale_service"].get_sales_dataframe()
        yield
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError during startup: {e}")
        print(f"FileNotFoundError during startup: {e}")
        yield
    except Exception as e:
        logger.error(f"Exception during startup: {e}")
        print(f"Exception during startup: {e}")
        yield


app.router.lifespan_context = lifespan

app.middleware("http")(add_sale_service_to_request)

app.include_router(sales.router, prefix="/api/v1", tags=["sales"], dependencies=[Depends(oauth2_scheme)])
app.include_router(user.router, prefix="/api/v1", tags=["users"], dependencies=[Depends(initialize_firebase)])

# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
