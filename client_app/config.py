from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_URL = 'http://127.0.0.1:5000'
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')