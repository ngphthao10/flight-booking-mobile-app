from flask import Blueprint, render_template, current_app
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', api_url=current_app.config['API_URL'])

# @main.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("auth.login"))

@main.route('/home')
def homepage():
    return render_template('admin/admin_home.html', api_url=current_app.config['API_URL'])
