import os
from dotenv import load_dotenv

load_dotenv()

# Flask configurations
class Config:
    JWT_KEY = os.getenv("JWT_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
