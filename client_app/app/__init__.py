from flask import Flask, session
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['API_URL'] = Config.API_URL 
    
    from app.routes.auth import auth
    from app.routes.user.homepage import homepage
    from app.routes.user.datcho import datcho
    from app.routes.user.khuyenmai import promotion
    from app.routes.admin.hanghangkhong import hanghangkhong
    from app.routes.admin.sanbay import sanbay
    from app.routes.admin.dashboard import dashboard
    from app.routes.admin.report import report

    app.register_blueprint(homepage)
    app.register_blueprint(datcho, url_prefix="/datcho")
    app.register_blueprint(hanghangkhong, url_prefix="/hanghangkhong")
    app.register_blueprint(sanbay, url_prefix="/sanbay")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(report, url_prefix="/report")
    app.register_blueprint(promotion, url_prefix="/promotion")
        
    return app