import imp
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['API_URL'] = Config.API_URL 
    
    from app.routes.auth import main
    from app.routes.user.homepage import homepage
    from app.routes.user.datcho import datcho
    from app.routes.admin.hanghangkhong import hanghangkhong
    app.register_blueprint(homepage)
    app.register_blueprint(datcho, url_prefix="/datcho")
    app.register_blueprint(hanghangkhong, url_prefix="/hanghangkhong")
    app.register_blueprint(main, url_prefix="/admin")

    return app