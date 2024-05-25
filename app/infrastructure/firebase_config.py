import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from app.infrastructure.logging_config import logger

load_dotenv()


def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": os.getenv("FIREBASE_TYPE"),
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
                "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
                "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
            })
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully with app")
            print("Firebase initialized successfully with app")
        else:
            logger.warning("Firebase app already initialized")
            print("Firebase app already initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        print(f"Failed to initialize Firebase: {e}")


def get_firestore_client():
    if firebase_admin._apps:
        return firestore.client()
    else:
        logger.error("Firebase is not initialized")
        raise Exception("Firebase is not initialized")
