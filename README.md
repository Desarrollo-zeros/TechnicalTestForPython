# Proyecto de FastAPI con Firebase y JWT

Este proyecto es una aplicación web construida con FastAPI que utiliza Firebase para la autenticación de usuarios y JWT para la autorización. También incluye servicios de ventas y usuarios, junto con un sistema de logging para manejar errores y excepciones.

## Instalación

1. Clona el repositorio en tu máquina local:
    ```bash
    git clone <URL_del_repositorio>
    cd <nombre_del_repositorio>
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno creando un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```plaintext
    SECRET_KEY=<tu_clave_secreta>
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    SERVICE_ACCOUNT_KEY=<ruta_a_tu_archivo_de_clave_de_cuenta_de_servicio>
    ```

## Ejecución

1. Inicia la aplicación FastAPI:
    ```bash
    uvicorn app.main:app --reload
    ```

2. La aplicación estará disponible en `http://localhost:8000`.

## Endpoints

### Registro de Usuario
- **URL**: `/api/v1/register`
- **Método**: `POST`
- **Cuerpo**:
    ```json
    {
        "email": "test@example.com",
        "password": "testpassword",
        "display_name": "Test User"
    }
    ```

### Login de Usuario
- **URL**: `/api/v1/login`
- **Método**: `POST`
- **Cuerpo**:
    ```json
    {
        "email": "test@example.com",
        "password": "testpassword"
    }
    ```

### Obtener Información del Usuario
- **URL**: `/api/v1/users/me`
- **Método**: `GET`
- **Header**: `Authorization: Bearer <token_jwt>`

### Endpoints de Ventas
- **URL**: `/api/v1/sales/employee`
- **Método**: `POST`
- **Header**: `Authorization: Bearer <token_jwt>`
- **Cuerpo**:
    ```json
    {
        "KeyEmployee": "1|343",
        "StartDate": "2023-05-24T02:31:17.061Z",
        "EndDate": "2024-10-10T02:31:17.061Z"
    }
    ```

## Pruebas

1. Ejecuta las pruebas unitarias con el siguiente comando:
    ```bash
    python -m unittest discover -s tests -p "*.py"
    ```

## Estructura del Proyecto

```json
TechnicalTestForPython/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── sales.py
│   │   │   ├── user.py
│   │   │   ├── dependencies.py
│   ├── core/
│   │   ├── config.py
│   ├── domain/
│   │   ├── contracts/
│   │   │   ├── infrastructures/
│   │   │   │   ├── i_data_frame_manager.py
│   │   │   │   ├── i_data_loader.py
│   │   │   ├── services/
│   │   │   │   ├── i_sale_service.py
│   │   │   │   ├── i_user_service.py
│   │   ├── entities/
│   │   │   ├── sales/
│   │   │   │   ├── sale.py
│   │   ├── inputs/
│   │   │   ├── employee_input.py
│   │   │   ├── product_input.py
│   │   │   ├── store_input.py
│   │   │   ├── user_login_input.py
│   │   │   ├── user_register_input.py
│   │   ├── outputs/
│   │   │   ├── employee_sales_output.py
│   │   │   ├── product_sales_output.py
│   │   │   ├── sale_output.py
│   │   │   ├── store_sales_output.py
│   │   │   ├── user_model_output.py
│   ├── infrastructure/
│   │   ├── data/
│   │   │   ├── data_frame_manager.py
│   │   │   ├── data_loader.py
│   │   │   ├── cached_property.py
│   │   │   ├── firebase_config.py
│   │   │   ├── logging_config.py
│   │   │   ├── middleware.py
│   │   │   ├── token.py
│   │   ├── services/
│   │   │   ├── sale_service.py
│   │   │   ├── user_service.py
│   ├── main.py
├── tests/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── test_sales_endpoints.py
│   │   │   ├── test_user_endpoints.py
│   │   ├── domain/
│   ├── infrastructure/
│   │   ├── data/
│   │   │   ├── test_data_frame_manager.py
│   │   │   ├── test_data_loader.py
│   ├── services/
│   │   ├── test_sale_service.py
│   │   ├── test_user_service.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── docker-compose.yml


```

## Notas

- Asegúrate de tener el archivo de claves de la cuenta de servicio de Firebase en el directorio especificado en `.env`.
- La aplicación está configurada para usar tokens JWT con un tiempo de expiración de 30 minutos.
- Los logs de errores se gestionan y almacenan utilizando la configuración especificada en `app/infrastructure/logging_config.py`.
