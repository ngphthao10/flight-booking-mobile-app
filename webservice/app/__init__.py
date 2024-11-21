from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config) 
    CORS(app)  
    # Khởi tạo db và login_manager với ứng dụng Flask
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        return NguoiDung.query.get(int(user_id))  
   
    from app.models import NguoiDung 

    from app.routes.auth_route import auth_bp 
    from app.routes.user_routes import user_bp 
    from app.routes.user.chuyenbay import chuyenbay
    app.register_blueprint(auth_bp)  
    app.register_blueprint(user_bp) 
    app.register_blueprint(chuyenbay)
    
    return app
