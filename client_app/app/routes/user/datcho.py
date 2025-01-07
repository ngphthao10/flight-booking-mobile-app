from flask import Blueprint, render_template, session, current_app
from app.decorators import login_required

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

@datcho.route('/booking-info', methods=['GET'])
@login_required
def booking_info():
    return render_template('user/danhsachdatcho.html', api_url=current_app.config['API_URL'])

@datcho.route('/booking-detailed', methods=['GET'])
def booking_detailed():
    return render_template('user/ketquatracuu.html', api_url=current_app.config['API_URL'])
