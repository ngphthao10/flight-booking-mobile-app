from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_URL = 'http://127.0.0.1:5000'
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Cấu hình cho upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')
    # FONT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'fonts')
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # # Các định dạng file được phép
    # ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    
    # # Cấu hình cho file tạm
    # TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'temp')
    
    # # Đảm bảo các thư mục tồn tại
    # @staticmethod
    # def init_folders():
    #     folders = [Config.UPLOAD_FOLDER, Config.FONT_FOLDER, Config.TEMP_FOLDER]
    #     for folder in folders:
    #         if not os.path.exists(folder):
    #             os.makedirs(folder)