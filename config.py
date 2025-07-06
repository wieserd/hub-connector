import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HUBSPOT_PRIVATE_APP_TOKEN: str = os.getenv("HUBSPOT_PRIVATE_APP_TOKEN", "")
    HUBSPOT_WEBHOOK_SECRET: str = os.getenv("HUBSPOT_WEBHOOK_SECRET", "")
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "100/minute") # Default to 100 requests per minute

settings = Settings()
