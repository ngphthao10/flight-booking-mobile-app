from flask import Blueprint, render_template, session, current_app, jsonify, send_file
from app.decorators import admin_required

xemdatcho = Blueprint('xemdatcho', __name__)

@xemdatcho.route('/', methods=['GET'])
@admin_required
def booking_info():
    return render_template('admin/datcho/xemdatcho.html', api_url=current_app.config['API_URL'])