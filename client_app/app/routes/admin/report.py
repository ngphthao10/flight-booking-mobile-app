from flask import Blueprint, jsonify, request, render_template, current_app
import requests

report = Blueprint('report', __name__)

@report.route('/')
def dashboard():
    return render_template('admin/dashboard.html')

@report.route('/dashboard/current-week-revenue')
def get_current_week_revenue():
    """Get current week revenue details"""
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/current_week_revenue")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report.route('/dashboard/market-share')
def get_market_share():
    """Get airlines market share with time filter"""
    try:
        # Lấy tham số time từ query string
        time_filter = request.args.get('time', 'today')  # Mặc định là 'today'

        # Gửi request đến API
        response = requests.get(
            f"{current_app.config['API_URL']}/api/report/market_share",
            params={"time": time_filter}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report.route('/dashboard/booking-stats')
def get_booking_stats():
    """Get booking statistics"""
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/booking_stats")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report.route('/dashboard/passenger-stats') 
def get_passenger_stats():
    """Get passenger statistics"""
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/passenger_stats")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report.route('/dashboard/baggage-stats')
def get_baggage_stats():
    """Get baggage service statistics"""
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/baggage_service_stats")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report.route('/dashboard/passengers')
def get_passengers():
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/passengers")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from datetime import datetime

@report.route('/dashboard/revenue')
def get_revenue_dashboard():
    """Proxy endpoint to get revenue data from the main API (report/revenue)."""
    try:
        # Lấy tháng và năm hiện tại
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Lấy tham số từ request
        report_type = request.args.get('type', 'monthly')  # Mặc định là 'monthly'
        month = request.args.get('month', str(current_month))  # Mặc định là tháng hiện tại
        year = request.args.get('year', str(current_year))    # Mặc định là năm hiện tại
        include_growth = request.args.get('include_growth', 'false')

        # URL của backend API
        url = f"{current_app.config['API_URL']}/api/report/revenue"

        # Chuẩn bị params để gọi API
        params = {
            'type': report_type,
            'month': month,
            'year': year,
            'include_growth': include_growth
        }

        # Gọi API
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            return jsonify(response.json()), response.status_code

    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"Error connecting to backend API: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }), 500
