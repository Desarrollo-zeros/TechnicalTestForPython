from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
