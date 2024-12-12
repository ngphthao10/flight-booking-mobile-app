from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta

datcho = Blueprint('datcho', __name__)

@datcho.route('/passenger-info', methods=['GET', 'POST'])
def passenger_info():
    # if request.method == 'POST':
    #     # Nhận dữ liệu từ form
    #     booking_data = request.json
    #     print(booking_data)
    #     return jsonify({'status': 'success'})
    
    return render_template('user/thongtindatcho.html')

@datcho.route('/thanhtoan', methods=['GET', 'POST'])
def thanhtoan():
    return render_template('user/thanhtoan.html')

@datcho.route('/booking-success', methods=['GET'])
def booking_success():
    return render_template('user/thanhToanThanhCong.html')

@datcho.route('/clear-temp-booking', methods=['POST'])
def clear_temp_booking():
    session.pop('temp_booking', None)
    return jsonify({'success': True})