import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_cors import CORS
from flask_mail import Mail

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 
db = SQLAlchemy()
login_manager = LoginManager()

mail = Mail()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config) 

    CORS(app)  
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        if 'user_id' not in session:
            return None
        return NguoiDung.query.get(int(user_id))
        
    app.config['MAIL_DEBUG'] = True

    mail.init_app(app)

    from app.models import NguoiDung 

    from app.routes.auth_route import auth_bp, init_oauth 
    from app.routes.user.chuyenbay import chuyenbay
    from app.routes.user.khuyenmai import khuyenmai
    from app.routes.user.dichvuve import dichvuve
    from app.routes.user.datcho import datcho
    from app.routes.user.dichvuhanhly import dichvuhanhly
    from app.routes.admin.hanghangkhong import hanghangkhong
    from app.routes.admin.maybay import maybay
    from app.routes.admin.report import report
    from app.routes.admin.maybay import maybay
    from app.routes.admin.sanbay import sanbay
    from app.routes.admin.quocgia import quocgia
    from app.routes.admin.nguoilienhe import nguoilienhe
    from app.routes.admin.hanhkhach import hanhkhach

    app.register_blueprint(auth_bp) 
    app.register_blueprint(chuyenbay)
    app.register_blueprint(hanghangkhong)
    app.register_blueprint(maybay)
    app.register_blueprint(sanbay)
    app.register_blueprint(quocgia)
    app.register_blueprint(nguoilienhe)
    app.register_blueprint(hanhkhach)
    app.register_blueprint(khuyenmai)
    app.register_blueprint(dichvuve)
    app.register_blueprint(dichvuhanhly)
    app.register_blueprint(datcho)
    app.register_blueprint(report)

    with app.app_context():
        db.create_all()
        init_oauth(app)
    return app
