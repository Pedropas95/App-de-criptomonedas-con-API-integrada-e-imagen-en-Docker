import os
from dotenv import load_dotenv

# -------------------------
# Cargar variables desde .env
# -------------------------
load_dotenv()

# -------------------------
# Configuración de la base de datoslue
# -------------------------
config = {
    "host": os.environ.get("DB_HOST"),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "port": os.environ.get("DB_PORT"),
}

# -------------------------
# API key de Groq
# -------------------------
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Falta la variable GROQ_API_KEY en el .env")
