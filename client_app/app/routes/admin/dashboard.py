from flask import Blueprint, jsonify, request, render_template, current_app
import requests
from app.decorators import admin_required
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@admin_required
def index():
    return render_template('admin/dashboard.html')

@dashboard.route('/market-share')
@admin_required
def get_market_share():
    """Get airlines market share with time filter"""
    try:
        time_filter = request.args.get('time', 'today') 

        response = requests.get(
            f"{current_app.config['API_URL']}/api/report/market_share",
            params={"time": time_filter}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard.route('/booking-stats')
@admin_required
def get_booking_stats():
    """Get booking statistics based on time period"""
    try:
        # Lấy thời gian từ query params, mặc định 7 ngày
        time_range = request.args.get('time_range', 'last_7_days')
    
        response = requests.get(
            f"{current_app.config['API_URL']}/api/report/booking_stats",
            params={'time_range': time_range}
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
            
        return jsonify({
            "status": "error",
            "message": "Không thể lấy dữ liệu thống kê"
        }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Lỗi hệ thống"
        }), 500

@dashboard.route('/passengers')
@admin_required
def get_passengers():
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/report/passengers")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dashboard.route('/revenue')
@admin_required
def get_revenue_dashboard():
    """Proxy endpoint to get revenue data from the main API (dashboard/revenue)."""
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

@dashboard.route('/baggage_service_stats')
@admin_required
def get_baggage_stats():
    """Get baggage service statistics"""
    try:
        time_range = request.args.get('time_range', 'last_7_days')
        
        response = requests.get(
            f"{current_app.config['API_URL']}/api/report/baggage_service_stats",
            params={'time_range': time_range}
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
            
        return jsonify({
            "status": "error",
            "message": "Không thể lấy dữ liệu thống kê"
        }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Lỗi hệ thống"
        }), 500

