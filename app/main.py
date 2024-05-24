from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import FastAPI, Request, Depends
from firebase_admin import auth
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.dependencies import get_sale_service, oauth2_scheme
from app.api.endpoints import sales, user
from app.infrastructure.firebase_config import initialize_firebase


# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservicio para la gestión de ventas con autenticación Firebase y JWT",
    version="1.0.0",
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
        _ = settings.ml_models["sale_service"].get_sales_dataframe()
        initialize_firebase()
        yield
    except FileNotFoundError as e:
        print(f"FileNotFoundError during startup: {e}")
        yield
    except Exception as e:
        print(f"Exception during startup: {e}")
        yield

app.router.lifespan_context = lifespan

@app.middleware("http")
async def add_sale_service_to_request(request: Request, call_next):
    try:
        request.state.sale_service = settings.ml_models["sale_service"]
        response = await call_next(request)
        return response
    except AttributeError as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Internal server error"})


app.include_router(sales.router, prefix="/api/v1", tags=["sales"], dependencies=[Depends(oauth2_scheme)])
app.include_router(user.router, prefix="/api/v1", tags=["users"])

# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
