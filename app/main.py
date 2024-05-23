from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies import create_sale_service
from app.api.endpoints import sales

# Crear la aplicación FastAPI
app = FastAPI(
    title="Celes Microservicio",
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


@app.on_event("startup")
async def startup_event():
    app.state.sale_service = create_sale_service()


@app.middleware("http")
async def add_sale_service_to_request(request: Request, call_next):
    request.state.sale_service = app.state.sale_service
    response = await call_next(request)
    return response


app.include_router(sales.router, prefix="/api/v1", tags=["sales"])

# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
