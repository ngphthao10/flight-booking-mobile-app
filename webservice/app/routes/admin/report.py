from flask import Blueprint, jsonify, request
from app import db
from app.models import *
from sqlalchemy import func, distinct
from datetime import datetime, timedelta

report = Blueprint('report', __name__)

@report.route('/api/report/market_share', methods=['GET'])
def get_market_share():
    """Gets market share by airlines with time filters."""
    try:
        # Lấy tham số thời gian từ query string
        time_filter = request.args.get('time', 'today')  # Mặc định là 'today'
        now = datetime.now()

        # Tính khoảng thời gian filter
        if time_filter == 'today':
            start_date = now.date()
            end_date = start_date + timedelta(days=1)
        elif time_filter == 'yesterday':
            start_date = (now - timedelta(days=1)).date()
            end_date = start_date + timedelta(days=1)
        elif time_filter == 'last_7_days':
            start_date = (now - timedelta(days=7)).date()
            end_date = now.date() + timedelta(days=1)
        elif time_filter == 'last_14_days':
            start_date = (now - timedelta(days=14)).date()
            end_date = now.date() + timedelta(days=1)
        elif time_filter == 'last_21_days':
            start_date = (now - timedelta(days=21)).date()
            end_date = now.date() + timedelta(days=1)
        elif time_filter == 'last_month':
            first_day_of_this_month = now.replace(day=1)
            start_date = (first_day_of_this_month - timedelta(days=1)).replace(day=1).date()
            end_date = first_day_of_this_month.date()
        else:
            return jsonify({"status": "error", "message": "Invalid time filter"}), 400

        # Tính tổng số đặt chỗ và thị phần
        total_bookings = db.session.query(
            HangHangKhong.MaHHK,
            HangHangKhong.TenHHK,
            func.count(DatCho.MaDatCho).label('booking_count')
        ).join(
            MayBay, HangHangKhong.MaHHK == MayBay.MaHHK
        ).join(
            ChuyenBay, MayBay.MaMayBay == ChuyenBay.MaMB
        ).join(
            DatCho, ChuyenBay.MaChuyenBay == DatCho.MaCB
        ).filter(
            DatCho.TrangThai == 'Đã thanh toán',
            func.date(DatCho.NgayMua) >= start_date,
            func.date(DatCho.NgayMua) < end_date
        ).group_by(
            HangHangKhong.MaHHK,
            HangHangKhong.TenHHK
        ).all()

        # Tính tổng số lượng đặt chỗ
        total = sum(booking.booking_count for booking in total_bookings)

        # Tạo kết quả trả về
        result = [
            {
                "airline_code": booking.MaHHK,
                "airline_name": booking.TenHHK,
                "total_bookings": int(booking.booking_count),
                "market_share": round((booking.booking_count / total * 100), 1) if total > 0 else 0.0
            }
            for booking in total_bookings
        ]

        return jsonify({"status": "success", "data": result, "time_filter": time_filter}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@report.route('/api/report/revenue', methods=['GET'])
def get_revenue_report():
    try:
        current_date = datetime.now()

        # Lấy các tham số từ query string
        report_type = request.args.get('type', 'monthly')
        month = request.args.get('month', str(current_date.month))  # 'all' hoặc chuỗi số
        year = request.args.get('year', str(current_date.year))     # 'all' hoặc chuỗi số
        include_growth = request.args.get('include_growth', 'false').lower() == 'true'

        if report_type == 'monthly':
            # === TÍNH DOANH THU THEO NGÀY ===
            base_query = db.session.query(
                func.date(DatCho.NgayMua).label('date'),
                func.count(DatCho.MaDatCho).label('total_orders'),
                func.coalesce(func.sum(ThanhToan.SoTien), 0).label('total_revenue')
            ).join(
                ThanhToan, DatCho.MaDatCho == ThanhToan.MaDatCho
            ).filter(
                DatCho.TrangThai == 'Đã thanh toán'
            )

            # Nếu month != 'all', lọc thêm theo tháng
            if month != 'all':
                base_query = base_query.filter(func.month(DatCho.NgayMua) == int(month))

            # Nếu year != 'all', lọc thêm theo năm
            if year != 'all':
                base_query = base_query.filter(func.year(DatCho.NgayMua) == int(year))

            query = base_query.group_by(
                func.date(DatCho.NgayMua)
            ).order_by(
                func.date(DatCho.NgayMua)
            )

            # Trả kết quả
            result = [
                {
                    "date": record.date.strftime('%Y-%m-%d'),
                    "total_orders": int(record.total_orders),
                    "total_revenue": float(record.total_revenue)
                }
                for record in query.all()
            ]

        elif report_type == 'weekly':
            # === TÍNH DOANH THU THEO TUẦN ===
            base_query = db.session.query(
                func.week(DatCho.NgayMua).label('week_number'),
                func.year(DatCho.NgayMua).label('year'),
                func.count(DatCho.MaDatCho).label('total_orders'),
                func.coalesce(func.sum(ThanhToan.SoTien), 0).label('total_revenue')
            ).join(
                ThanhToan, DatCho.MaDatCho == ThanhToan.MaDatCho
            ).filter(
                DatCho.TrangThai == 'Đã thanh toán'
            )

            if month != 'all':
                base_query = base_query.filter(func.month(DatCho.NgayMua) == int(month))
            if year != 'all':
                base_query = base_query.filter(func.year(DatCho.NgayMua) == int(year))

            query = base_query.group_by(
                func.week(DatCho.NgayMua),
                func.year(DatCho.NgayMua)
            ).order_by(
                func.year(DatCho.NgayMua),
                func.week(DatCho.NgayMua)
            )

            weekly_data = query.all()
            # Chuyển kết quả raw thành danh sách dict
            result = [
                {
                    "week_number": int(week.week_number),
                    "year": int(week.year),
                    "total_orders": int(week.total_orders),
                    "total_revenue": float(week.total_revenue)
                }
                for week in weekly_data
            ]

            if include_growth:
                result_sorted = sorted(result, key=lambda x: (x['year'], x['week_number']))
                prev_revenue = None
                for i, row in enumerate(result_sorted):
                    current_revenue = row["total_revenue"]
                    if prev_revenue and prev_revenue != 0:
                        row["growth_rate"] = round((current_revenue - prev_revenue) / prev_revenue * 100, 2)
                    else:
                        row["growth_rate"] = 0
                    prev_revenue = current_revenue
                
                # Cuối cùng, gán result = result_sorted
                result = result_sorted

        else:
            # Nếu type không hợp lệ, trả về lỗi
            return jsonify({
                "status": "error",
                "message": "Invalid report type. Use 'monthly' or 'weekly'."
            }), 400

        return jsonify({
            "status": "success",
            "data": result,
            "report_type": report_type,
            "month": month,
            "year": year
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@report.route('/api/report/passengers', methods=['GET']) 
def get_passengers():
    try:
        # Count total users and passengers
        total_users = NguoiDung.query.filter_by(MaNND=2).count()
        total_passengers = HanhKhach.query.count()
        
        # Calculate percentage of users compared to passengers
        user_passenger_ratio = 0
        if total_passengers > 0:
            user_passenger_ratio = round((total_passengers / total_users) * 100, 2)
        
        # Prepare response
        result = {
            "total_users": total_users,
            "total_passengers": total_passengers,
            "user_passenger_ratio": user_passenger_ratio
        }
        
        return jsonify({"status": "success", "data": result}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@report.route('/api/report/booking_stats', methods=['GET'])
def get_booking_stats():
    """Gets booking statistics for different time periods."""
    try:        
        # Get current date at start of day
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Define time periods
        time_periods = {
            'today': {
                'start': today,
                'end': datetime.now(),
                'label': 'Hôm nay'
            },
            'yesterday': {
                'start': today - timedelta(days=1),
                'end': today,
                'label': 'Hôm qua'
            },
            'last_7_days': {
                'start': today - timedelta(days=7),
                'end': datetime.now(),
                'label': '7 ngày qua'
            },
            'last_14_days': {
                'start': today - timedelta(days=14),
                'end': datetime.now(),
                'label': '14 ngày qua'
            },
            'last_21_days': {
                'start': today - timedelta(days=21),
                'end': datetime.now(),
                'label': '21 ngày qua'
            },
            'last_month': {
                'start': today.replace(day=1) - timedelta(days=1),
                'end': today,
                'label': 'Tháng trước'
            },
            'last_3_months': {
                'start': (today.replace(day=1) - timedelta(days=90)),
                'end': datetime.now(),
                'label': '3 tháng trước'
            }
        }

        # Query for each time period
        result = []
        for period_key, period in time_periods.items():
            # Get daily stats for the period
            daily_stats = db.session.query(
                func.date(DatCho.NgayMua).label('date'),
                func.count(DatCho.MaDatCho).label('total_bookings'),
                func.sum(DatCho.SoLuongGheBus + DatCho.SoLuongGheEco).label('total_passengers')
            ).filter(
                DatCho.NgayMua >= period['start'],
                DatCho.NgayMua <= period['end']
            ).group_by(
                func.date(DatCho.NgayMua)
            ).order_by(
                func.date(DatCho.NgayMua)
            ).all()

            # Format the results
            period_data = {
                'period': period['label'],
                'data': [
                    {
                        'date': stats.date.strftime('%Y-%m-%d'),
                        'total_bookings': int(stats.total_bookings or 0),
                        'total_passengers': int(stats.total_passengers or 0)
                    }
                    for stats in daily_stats
                ]
            }
            
            # Add cumulative totals for the period
            period_data['totals'] = {
                'total_bookings': sum(day['total_bookings'] for day in period_data['data']),
                'total_passengers': sum(day['total_passengers'] for day in period_data['data'])
            }
            
            result.append(period_data)

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# @report.route('/api/report/flight_stats', methods=['GET'])
# def get_flight_stats():
#     """Gets statistics about flights."""
#     try:
#         # Lấy thống kê chuyến bay the o loại (quốc tế/nội địa)
#         flight_stats = db.session.query(
#             ChuyenBay.LoaiChuyenBay,
#             func.count(ChuyenBay.MaChuyenBay).label('total_flights'),
#             func.avg(ChuyenBay.GiaVeBus).label('avg_business_price'),
#             func.avg(ChuyenBay.GiaVeEco).label('avg_economy_price')
#         ).group_by(
#             ChuyenBay.LoaiChuyenBay
#         ).all()

#         result = [
#             {
#                 "flight_type": stats.LoaiChuyenBay,
#                 "total_flights": int(stats.total_flights),
#                 "avg_business_price": float(stats.avg_business_price),
#                 "avg_economy_price": float(stats.avg_economy_price)
#             }
#             for stats in flight_stats
#         ]

#         return jsonify({"status": "success", "data": result}), 200
        
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


@report.route('/api/report/baggage_service_stats', methods=['GET'])
def get_baggage_service_stats():
    """Gets baggage service statistics for different time periods."""
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Get time range from request
        time_range = request.args.get('time_range', 'last_7_days')
        
        # Get current date at start of day
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Define date range based on time_range
        if time_range == 'today':
            start_date = today
            end_date = datetime.now()
        elif time_range == 'yesterday':
            start_date = today - timedelta(days=1)
            end_date = today
        elif time_range == 'last_7_days':
            start_date = today - timedelta(days=7)
            end_date = datetime.now()
        elif time_range == 'last_14_days':
            start_date = today - timedelta(days=14)
            end_date = datetime.now()
        elif time_range == 'last_21_days':
            start_date = today - timedelta(days=21)
            end_date = datetime.now()
        elif time_range == 'last_month':
            start_date = today.replace(day=1) - timedelta(days=1)
            end_date = today
        else:  # last_3_months
            start_date = today - timedelta(days=90)
            end_date = datetime.now()

        # Query statistics
        stats = db.session.query(
            DichVuHanhLy.SoKy.label('weight'),
            func.count(ChiTietDatCho.MaDatCho).label('bookings'),
            func.sum(DichVuHanhLy.Gia).label('revenue')
        ).join(
            ChiTietDatCho, DichVuHanhLy.MaDichVu == ChiTietDatCho.MaDichVu
        ).join(
            DatCho, ChiTietDatCho.MaDatCho == DatCho.MaDatCho
        ).filter(
            DatCho.NgayMua.between(start_date, end_date)
        ).group_by(
            DichVuHanhLy.SoKy
        ).order_by(
            DichVuHanhLy.SoKy
        ).all()

        # Format results
        result = [{
            'weight': f'{stat.weight}kg',
            'bookings': int(stat.bookings),
            'revenue': float(stat.revenue),
            'percentage': 0  # Will be calculated below
        } for stat in stats]

        # Calculate percentages
        total_bookings = sum(item['bookings'] for item in result)
        if total_bookings > 0:
            for item in result:
                item['percentage'] = round(item['bookings'] / total_bookings * 100, 1)

        return jsonify({
            "status": "success",
            "data": {
                "stats": result,
                "total_bookings": total_bookings,
                "total_revenue": sum(item['revenue'] for item in result)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500