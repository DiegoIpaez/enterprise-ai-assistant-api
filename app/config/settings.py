import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "")

    # API
    API_TITLE: str = os.getenv("API_TITLE", "Entrerprise AI Assistant")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")


settings = Settings()
