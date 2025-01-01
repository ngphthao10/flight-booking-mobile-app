from flask import Blueprint, render_template, request, jsonify, session, current_app, url_for
from datetime import datetime, timedelta

datcho = Blueprint('datcho', __name__)

@datcho.route('/passenger-info', methods=['GET', 'POST'])
def passenger_info():
    return render_template('user/thongtindatcho.html', api_url=current_app.config['API_URL'])

@datcho.route('/thanhtoan', methods=['GET', 'POST'])
def thanhtoan():
    user_info = session.get('user_info') 
    print(user_info)
    return render_template('user/thanhtoan.html', api_url=current_app.config['API_URL'], user_info=user_info)

@datcho.route('/booking-success', methods=['GET'])
def booking_success():
    return render_template('user/thanhToanThanhCong.html')

