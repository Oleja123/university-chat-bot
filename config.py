import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    API_BASE_URL=os.getenv('API_BASE_URL') or 'pososamba'
    BOT_TOKEN=os.getenv('BOT_TOKEN') or 'pososamba'