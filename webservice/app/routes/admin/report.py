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
    """
    Endpoint: /api/report/revenue
    Params:
        - type: 'monthly' or 'weekly' (mặc định 'monthly')
        - month: 1-12 hoặc 'all' (mặc định là tháng hiện tại)
        - year: 4-digit year hoặc 'all' (mặc định là năm hiện tại)
        - include_growth: true/false (mặc định false)
    Chức năng:
        - Tính doanh thu 'monthly': group_by date (theo ngày)
        - Tính doanh thu 'weekly': group_by (week_number, year)
        - Tùy chọn tính 'growth_rate' (theo tuần) so sánh tuần hiện tại và tuần trước.
    """
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
    """Gets statistics about bookings."""
    try:
        # Lấy thống kê đặt chỗ theo trạng thái
        booking_stats = db.session.query(
            DatCho.TrangThai,
            func.count(DatCho.MaDatCho).label('total_bookings'),
            func.sum(DatCho.SoLuongGheBus + DatCho.SoLuongGheEco).label('total_passengers')
        ).group_by(
            DatCho.TrangThai
        ).all()

        result = [
            {
                "status": stats.TrangThai,
                "total_bookings": int(stats.total_bookings),
                "total_passengers": int(stats.total_passengers)
            }
            for stats in booking_stats
        ]

        return jsonify({"status": "success", "data": result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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

@report.route('/api/report/passenger_stats', methods=['GET'])
def get_passenger_stats():
    """Gets statistics about passengers."""
    try:
        # Thống kê theo loại hành khách
        passenger_stats = db.session.query(
            HanhKhach.LoaiHK,
            HanhKhach.QuocTich,
            func.count(HanhKhach.MaHanhKhach).label('total_passengers'),
            func.count(distinct(DatCho.MaDatCho)).label('total_bookings')
        ).join(
            ChiTietDatCho, HanhKhach.MaHanhKhach == ChiTietDatCho.MaHK
        ).join(
            DatCho, ChiTietDatCho.MaDatCho == DatCho.MaDatCho
        ).group_by(
            HanhKhach.LoaiHK,
            HanhKhach.QuocTich
        ).all()

        result = [
            {
                "passenger_type": stats.LoaiHK,
                "nationality": stats.QuocTich,
                "total_passengers": int(stats.total_passengers),
                "total_bookings": int(stats.total_bookings)
            }
            for stats in passenger_stats
        ]

        return jsonify({"status": "success", "data": result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@report.route('/api/report/baggage_service_stats', methods=['GET'])
def get_baggage_service_stats():
    """Gets statistics about baggage services."""
    try:
        # Thống kê dịch vụ hành lý
        baggage_stats = db.session.query(
            DichVuHanhLy.SoKy,
            func.count(ChiTietDatCho.MaDatCho).label('total_bookings'),
            func.avg(DichVuHanhLy.Gia).label('average_price')
        ).join(
            ChiTietDatCho, DichVuHanhLy.MaDichVu == ChiTietDatCho.MaDichVu
        ).group_by(
            DichVuHanhLy.SoKy
        ).order_by(
            DichVuHanhLy.SoKy
        ).all()

        result = [  
            {
                "weight": int(stats.SoKy),
                "total_bookings": int(stats.total_bookings),
                "average_price": float(stats.average_price)
            }
            for stats in baggage_stats
        ]

        return jsonify({"status": "success", "data": result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500