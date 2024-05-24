import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.core.config import settings



def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized successfully with app")
        else:
            print(f"Firebase app already initialized")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")

def get_firestore_client():
    if firebase_admin._apps:
        return firestore.client()
    else:
        raise Exception("Firebase is not initialized")
