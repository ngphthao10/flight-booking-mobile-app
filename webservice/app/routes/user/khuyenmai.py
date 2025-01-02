from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from app.models import HangHangKhong, KhuyenMai
from app import db

khuyenmai = Blueprint('khuyenmai', __name__)

@khuyenmai.route('/api/bookings/temp/promotions', methods=['POST'])
def get_temp_booking_promotions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Không có dữ liệu gửi lên'}), 400
            
        list_hang_hang_khong = data.get('hang_hang_khong', []) 
        list_ma_chuyen_bay = data.get('ma_chuyen_bay', [])
        tong_tien = data.get('tong_tien', 0)
        
        # if not list_hang_hang_khong or not list_ma_chuyen_bay or not tong_tien:
        #     return jsonify({'error': 'Thiếu thông tin cần thiết'}), 400
            
        hang_hang_khong_info = HangHangKhong.query.filter(
            HangHangKhong.TenHHK.in_(list_hang_hang_khong)
        ).all()
        
        if not hang_hang_khong_info:
            return jsonify({'error': 'Không tìm thấy hãng hàng không'}), 404
            
        ma_hhk_list = [hhk.MaHHK for hhk in hang_hang_khong_info]
        current_date = datetime.now().date()
        
        all_promotions = KhuyenMai.query.filter(
            KhuyenMai.NgayBatDau <= current_date,
            KhuyenMai.NgayKetThuc >= current_date
        ).all()

        promotions_result = {
            'HANG_HANG_KHONG': [],
            'CHUYEN_BAY': []
        }

        for km in all_promotions:
            if km.ds_hang_hang_khong:
                for hhk in km.ds_hang_hang_khong:
                    if hhk.MaHHK in ma_hhk_list:
                        tien_giam = km.calculate_discount(tong_tien)
                        promotions_result['HANG_HANG_KHONG'].append({
                            'ma_khuyen_mai': km.MaKhuyenMai,
                            'ten_khuyen_mai': km.TenKhuyenMai,
                            'mo_ta': km.MoTa,
                            'loai_khuyen_mai': km.LoaiKhuyenMai,
                            'gia_tri': float(km.GiaTri),
                            'tien_giam': float(tien_giam),
                            'ap_dung_cho': hhk.TenHHK
                        })
                        
            if km.ds_chuyen_bay:
                km_flight_codes = {cb.MaChuyenBay for cb in km.ds_chuyen_bay}
                matching_flights = set(list_ma_chuyen_bay) & km_flight_codes
                
                if matching_flights:
                    tien_giam = km.calculate_discount(tong_tien)
                    promotions_result['CHUYEN_BAY'].append({
                        'ma_khuyen_mai': km.MaKhuyenMai,
                        'ten_khuyen_mai': km.TenKhuyenMai,
                        'mo_ta': km.MoTa,
                        'loai_khuyen_mai': km.LoaiKhuyenMai,
                        'gia_tri': float(km.GiaTri),
                        'tien_giam': float(tien_giam),
                        'ap_dung_cho': list(matching_flights)
                    })

        return jsonify({
            'tong_tien': float(tong_tien),
            'khuyen_mai': promotions_result
        })

    except Exception as e:
        print(f"Error getting promotions: {str(e)}")
        return jsonify({'error': str(e)}), 500
