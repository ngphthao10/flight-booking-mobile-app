from flask import Blueprint, request, jsonify
from datetime import datetime,timedelta
from app.models import ChuyenBay, MayBay, HangHangKhong
from app import db
from typing import List

chuyenbay = Blueprint('chuyenbay', __name__)

@chuyenbay.route('/api/flights/search', methods=['POST'])
def search_flights():
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['san_bay_di', 'san_bay_den', 'ngay_di', 'so_luong_khach', 'loai_ghe']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse input parameters
        san_bay_di = data['san_bay_di']
        san_bay_den = data['san_bay_den']
        ngay_di = datetime.strptime(data['ngay_di'], '%Y-%m-%d').date()
        so_luong_khach = int(data['so_luong_khach'])
        loai_ghe = data['loai_ghe'].upper()  # 'ECO' or 'BUS'
        khu_hoi = data.get('khu_hoi', False)
        ngay_ve = data.get('ngay_ve')
        include_connecting = data.get('include_connecting', False)
        
        # Tìm chuyến bay trực tiếp
        direct_flights = search_direct_flights(
            san_bay_di, san_bay_den, ngay_di, so_luong_khach, loai_ghe
        )
        
        # Tìm chuyến bay quá cảnh nếu được yêu cầu
        connecting_flights = []
        if include_connecting:
            connecting_flights = search_connecting_flights(
                san_bay_di, san_bay_den, ngay_di, so_luong_khach, loai_ghe
            )
        
        # Tìm chuyến bay khứ hồi nếu được yêu cầu
        return_flights = []
        if khu_hoi and ngay_ve:
            ngay_ve = datetime.strptime(ngay_ve, '%Y-%m-%d').date()
            return_flights = search_direct_flights(
                san_bay_den, san_bay_di, ngay_ve, so_luong_khach, loai_ghe
            )
            if include_connecting:
                return_connecting_flights = search_connecting_flights(
                    san_bay_den, san_bay_di, ngay_ve, so_luong_khach, loai_ghe
                )
                return_flights.extend(return_connecting_flights)
        
        return jsonify({
            'direct_flights': [flight_to_dict(f) for f in direct_flights],
            'connecting_flights': [connecting_flight_to_dict(f) for f in connecting_flights],
            'return_flights': [flight_to_dict(f) for f in return_flights]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def search_direct_flights(san_bay_di: str, san_bay_den: str, 
                        ngay_di: datetime.date, so_luong_khach: int, 
                        loai_ghe: str) -> List[ChuyenBay]:
    """Tìm các chuyến bay trực tiếp theo điều kiện"""
    
    query = ChuyenBay.query\
        .join(MayBay)\
        .join(HangHangKhong)\
        .filter(
            ChuyenBay.MaSanBayDi == san_bay_di,
            ChuyenBay.MaSanBayDen == san_bay_den,
            db.func.date(ChuyenBay.ThoiGianDi) == ngay_di,
            ChuyenBay.TrangThai == 0
        )
    
    if loai_ghe == 'ECO':
        query = query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
    else:
        query = query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
        
    return query.all()

def search_connecting_flights(san_bay_di: str, san_bay_den: str,
                           ngay_di: datetime.date, so_luong_khach: int,
                           loai_ghe: str) -> List[tuple]:
    """Tìm các chuyến bay quá cảnh theo điều kiện"""
    
    # Tìm các chuyến bay quá cảnh với thời gian chờ từ 2-8 tiếng
    min_layover = timedelta(hours=2)
    max_layover = timedelta(hours=8)
    
    connecting_flights = []
    
    # Tìm tất cả các chuyến bay xuất phát từ sân bay đi trong ngày
    first_leg_query = ChuyenBay.query\
        .join(MayBay)\
        .filter(
            ChuyenBay.MaSanBayDi == san_bay_di,
            db.func.date(ChuyenBay.ThoiGianDi) == ngay_di,
            ChuyenBay.TrangThai == 0
        )
    
    if loai_ghe == 'ECO':
        first_leg_query = first_leg_query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
    else:
        first_leg_query = first_leg_query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
    
    first_leg_flights = first_leg_query.all()
    
    for first_flight in first_leg_flights:
        # Tìm các chuyến bay kết nối phù hợp
        second_leg_query = ChuyenBay.query\
            .join(MayBay)\
            .filter(
                ChuyenBay.MaSanBayDi == first_flight.MaSanBayDen,
                ChuyenBay.MaSanBayDen == san_bay_den,
                ChuyenBay.TrangThai == 0,
                ChuyenBay.ThoiGianDi > first_flight.ThoiGianDen + min_layover,
                ChuyenBay.ThoiGianDi < first_flight.ThoiGianDen + max_layover,
                MayBay.MaHHK == first_flight.may_bay.MaHHK  # Cùng hãng hàng không
            )
        
        if loai_ghe == 'ECO':
            second_leg_query = second_leg_query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
        else:
            second_leg_query = second_leg_query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
        
        second_leg_flights = second_leg_query.all()
        
        for second_flight in second_leg_flights:
            connecting_flights.append((first_flight, second_flight))
    
    return connecting_flights

def flight_to_dict(flight: ChuyenBay) -> dict:
    """Chuyển đổi đối tượng ChuyenBay thành dictionary"""
    return {
        'ma_chuyen_bay': flight.MaChuyenBay,
        'hang_hang_khong': flight.may_bay.hang_hang_khong.TenHHK,
        'ma_hhk': flight.may_bay.MaHHK,
        'san_bay_di': flight.MaSanBayDi,
        'san_bay_den': flight.MaSanBayDen,
        'thoi_gian_di': flight.ThoiGianDi.isoformat(),
        'thoi_gian_den': flight.ThoiGianDen.isoformat(),
        'gia_ve_eco': float(flight.GiaVeEco) if flight.GiaVeEco else None,
        'gia_ve_bus': float(flight.GiaVeBus) if flight.GiaVeBus else None,
        'ghe_eco_con_lai': flight.SLEcoConLai,
        'ghe_bus_con_lai': flight.SLBusConLai
    }

def connecting_flight_to_dict(flights: tuple) -> dict:
    """Chuyển đổi cặp chuyến bay quá cảnh thành dictionary"""
    first_flight, second_flight = flights
    return {
        'first_flight': flight_to_dict(first_flight),
        'second_flight': flight_to_dict(second_flight),
        'total_time': (second_flight.ThoiGianDen - first_flight.ThoiGianDi).total_seconds() / 3600,
        'layover_time': (second_flight.ThoiGianDi - first_flight.ThoiGianDen).total_seconds() / 3600
    }
