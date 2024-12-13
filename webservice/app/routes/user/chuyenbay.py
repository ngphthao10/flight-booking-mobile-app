from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.models import ChuyenBay, MayBay, HangHangKhong, SanBay
from app import db
from typing import List
from sqlalchemy.orm import aliased

chuyenbay = Blueprint('chuyenbay', __name__)

@chuyenbay.route('/api/sanbay', methods=['GET'])
def get_sanbay():
   sanbay_list = SanBay.query.all()
   return jsonify([{
       "ma_san_bay": sb.MaSanBay,
       "thanh_pho": sb.ThanhPho
   } for sb in sanbay_list])

from flask import jsonify, request

@chuyenbay.route('/api/flights/<ma_chuyen_bay>', methods=['GET'])
def get_flight_details(ma_chuyen_bay):
   try:
       # Tạo alias cho bảng SanBay để phân biệt sân bay đi và đến
       SanBayDi = aliased(SanBay)
       SanBayDen = aliased(SanBay)

       flight = db.session.query(
           ChuyenBay.MaChuyenBay,
           SanBayDi.TenSanBay.label('san_bay_di'),
           SanBayDen.TenSanBay.label('san_bay_den'), 
           ChuyenBay.ThoiGianDi,
           ChuyenBay.ThoiGianDen,
           HangHangKhong.TenHHK.label('hang_bay')
       ).join(
           SanBayDi,
           ChuyenBay.MaSanBayDi == SanBayDi.MaSanBay
       ).join(
           SanBayDen,
           ChuyenBay.MaSanBayDen == SanBayDen.MaSanBay
       ).join(
           MayBay,
           ChuyenBay.MaMB == MayBay.MaMayBay
       ).join(
           HangHangKhong,
           MayBay.MaHHK == HangHangKhong.MaHHK
       ).filter(
           ChuyenBay.MaChuyenBay == ma_chuyen_bay,
           ChuyenBay.TrangThai == 0
       ).first()

       if not flight:
           return jsonify({
               'error': 'Không tìm thấy chuyến bay'
           }), 404

       thoi_gian_bay = flight.ThoiGianDen - flight.ThoiGianDi
       hours = thoi_gian_bay.seconds // 3600 
       minutes = (thoi_gian_bay.seconds % 3600) // 60
       thoi_gian_bay_str = f"{hours}h {minutes}m"

       response_data = {
           'ma_chuyen_bay': flight.MaChuyenBay,
           'san_bay_di': flight.san_bay_di,
           'san_bay_den': flight.san_bay_den,
           'thoi_gian_di': flight.ThoiGianDi.isoformat(),
           'thoi_gian_den': flight.ThoiGianDen.isoformat(),
           'thoi_gian_bay': thoi_gian_bay_str,
           'hang_bay': flight.hang_bay
       }

       return jsonify(response_data)

   except Exception as e:
       return jsonify({
           'error': f'Có lỗi xảy ra: {str(e)}'
       }), 500

@chuyenbay.route('/api/flights/search', methods=['POST'])
def search_flights():
    try:
        data = request.get_json()
        
        required_fields = ['san_bay_di', 'san_bay_den', 'ngay_di', 'so_luong_khach', 'loai_ghe']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        san_bay_di = data['san_bay_di']
        san_bay_den = data['san_bay_den']
        ngay_di = datetime.strptime(data['ngay_di'], '%d-%m-%Y').date()
        so_luong_khach = int(data['so_luong_khach'])
        loai_ghe = data['loai_ghe'].upper()  # 'ECO' or 'BUS'
        khu_hoi = data.get('khu_hoi', False)
        include_connecting = data.get('include_connecting', False)
        max_stops = data.get('max_stops', 3)  # Số điểm dừng tối đa
        
        direct_flights = search_direct_flights(
            san_bay_di, san_bay_den, ngay_di, so_luong_khach, loai_ghe
        )
        
        connecting_flights = []
        if include_connecting:
            connecting_routes = search_connecting_flights(
                san_bay_di, san_bay_den, ngay_di, 
                so_luong_khach, loai_ghe, max_stops
            )
            connecting_flights = [
                flight_dict for flight_dict in [
                    connecting_flight_to_dict(route, loai_ghe) 
                    for route in connecting_routes
                ]
                if flight_dict is not None  
            ]
        
        return_flights = []
        return_connecting = []
        if khu_hoi and 'ngay_ve' in data and data['ngay_ve']:
            ngay_ve = datetime.strptime(data['ngay_ve'], '%d-%m-%Y').date()
            return_flights = search_direct_flights(
                san_bay_den, san_bay_di, ngay_ve, so_luong_khach, loai_ghe
            )
            
            if include_connecting:
                return_routes = search_connecting_flights(
                    san_bay_den, san_bay_di, ngay_ve, 
                    so_luong_khach, loai_ghe, max_stops
                )
                return_connecting = [
                    flight_dict for flight_dict in [
                        connecting_flight_to_dict(route, loai_ghe) 
                        for route in return_routes
                    ]
                    if flight_dict is not None
                ]
        
        return jsonify({
            'direct_flights': [flight_to_dict(f, loai_ghe) for f in direct_flights],
            'connecting_flights': connecting_flights,
            'return_direct_flights': [flight_to_dict(f, loai_ghe) for f in return_flights],
            'return_connecting_flights': return_connecting
        })
        
    except Exception as e:
        print(f"Search flights error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def search_direct_flights(san_bay_di: str, san_bay_den: str, 
                        ngay_di: datetime.date, so_luong_khach: int, 
                        loai_ghe: str) -> List[ChuyenBay]:
    
    try:
        query = ChuyenBay.query\
            .join(MayBay)\
            .join(HangHangKhong)\
            .filter(
                ChuyenBay.MaSanBayDi == san_bay_di,
                ChuyenBay.MaSanBayDen == san_bay_den,
                db.func.date(ChuyenBay.ThoiGianDi) == ngay_di,
                ChuyenBay.TrangThai == 0,
                ChuyenBay.TrangThaiVe == 0
            )
        
        if loai_ghe == 'ECO':
            query = query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
        else:
            query = query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
            
        return query.all()
    except Exception as e:
        print(f"Search direct flights error: {str(e)}")
        return []

def search_connecting_flights(san_bay_di: str, san_bay_den: str,
                           ngay_di: datetime.date, so_luong_khach: int,
                           loai_ghe: str, max_stops: int = 3) -> List[List[ChuyenBay]]:
    try:
        min_layover = timedelta(hours=2)
        max_layover = timedelta(hours=8)
        max_total_time = timedelta(hours=36) 
        
        def find_connecting_flights(current_route: List[ChuyenBay], visited_airports: set) -> List[List[ChuyenBay]]:
            
            last_flight = current_route[-1]
            if last_flight.MaSanBayDen == san_bay_den:
                return [current_route]

            if len(current_route) >= max_stops + 1: 
                return []
                
            total_time = last_flight.ThoiGianDen - current_route[0].ThoiGianDi
            if total_time > max_total_time:
                return []

            next_flights_query = ChuyenBay.query\
                .join(MayBay)\
                .filter(
                    ChuyenBay.MaSanBayDi == last_flight.MaSanBayDen,
                    ChuyenBay.MaSanBayDen.notin_(visited_airports),  # Không bay qua sân bay đã đi
                    ChuyenBay.TrangThai == 0,
                    ChuyenBay.TrangThaiVe == 0,
                    ChuyenBay.ThoiGianDi > last_flight.ThoiGianDen + min_layover,
                    ChuyenBay.ThoiGianDi < last_flight.ThoiGianDen + max_layover,
                    MayBay.MaHHK == current_route[0].may_bay.MaHHK  # Cùng hãng với chuyến đầu tiên
                )
            
            if loai_ghe == 'ECO':
                next_flights_query = next_flights_query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
            else:
                next_flights_query = next_flights_query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
            
            all_routes = []
            next_flights = next_flights_query.all()
            
            for next_flight in next_flights:
                new_visited = visited_airports | {next_flight.MaSanBayDen}
                new_route = current_route + [next_flight]
                routes = find_connecting_flights(new_route, new_visited)
                all_routes.extend(routes)
            
            return all_routes

        first_flights_query = ChuyenBay.query\
            .join(MayBay)\
            .filter(
                ChuyenBay.MaSanBayDi == san_bay_di,
                db.func.date(ChuyenBay.ThoiGianDi) == ngay_di,
                ChuyenBay.TrangThai == 0,
                ChuyenBay.TrangThaiVe == 0
            )
        
        if loai_ghe == 'ECO':
            first_flights_query = first_flights_query.filter(ChuyenBay.SLEcoConLai >= so_luong_khach)
        else:
            first_flights_query = first_flights_query.filter(ChuyenBay.SLBusConLai >= so_luong_khach)
        
        all_routes = []
        first_flights = first_flights_query.all()
        
        for first_flight in first_flights:
            visited = {san_bay_di, first_flight.MaSanBayDen}
            routes = find_connecting_flights([first_flight], visited)
            all_routes.extend(routes)
        
        all_routes.sort(key=lambda route: (route[-1].ThoiGianDen - route[0].ThoiGianDi))
        
        return all_routes
        
    except Exception as e:
        print(f"Search connecting flights error: {str(e)}")
        return []

def flight_to_dict(flight, loai_ghe='ECO'):
    try:
        return {
            'ma_chuyen_bay': flight.MaChuyenBay,
            'hang_hang_khong': flight.may_bay.hang_hang_khong.TenHHK,
            'ma_hhk': flight.may_bay.MaHHK,
            'san_bay_di': flight.san_bay_di.ThanhPho,
            'san_bay_den': flight.san_bay_den.ThanhPho,
            'ma_sb_di' : flight.MaSanBayDi,
            'ma_sb_den' : flight.MaSanBayDen,
            'thoi_gian_di': flight.ThoiGianDi.isoformat(),
            'thoi_gian_den': flight.ThoiGianDen.isoformat(),
            'gia_ve_eco': float(flight.GiaVeEco) if flight.GiaVeEco else None,
            'gia_ve_bus': float(flight.GiaVeBus) if flight.GiaVeBus else None,
            'loai_ghe': loai_ghe.upper(),
            'thoi_gian_bay': (flight.ThoiGianDen - flight.ThoiGianDi).total_seconds() / 3600,
        }
    except Exception as e:
        print(f"Convert flight to dict error: {str(e)}")
        return {}

def connecting_flight_to_dict(flights: List[ChuyenBay], loai_ghe='ECO') -> dict:
    try:
        if len(flights) <= 1:
            return None
            
        flight_dicts = []
        layover_times = []
        tong_gia = 0
        
        for i, flight in enumerate(flights):
            flight_dict = flight_to_dict(flight, loai_ghe)
            flight_dicts.append(flight_dict)
        
            if loai_ghe == 'ECO':
                gia_ve = flight_dict.get('gia_ve_eco', 0) or 0
            else:
                gia_ve = flight_dict.get('gia_ve_bus', 0) or 0
            tong_gia += gia_ve
            
            if i > 0:
                layover = (flight.ThoiGianDi - flights[i-1].ThoiGianDen).total_seconds() / 3600
                layover_times.append(round(layover, 2))

        total_time = (flights[-1].ThoiGianDen - flights[0].ThoiGianDi).total_seconds() / 3600
        
        return {
            'flights': flight_dicts,
            'total_time': round(total_time, 2),
            'layover_times': layover_times,
            'num_stops': len(flights) - 1,
            'tong_gia_ve': tong_gia
        }
            
    except Exception as e:
        print(f"Convert connecting flight to dict error: {str(e)}")
        return None


@chuyenbay.route('/api/flights/filter', methods=['POST'])
def filter_flights():
    try:
        data = request.get_json()
        flights_data = data.get('flights', {})
        filter_params = data.get('filters', {})

        flight_type = filter_params.get('flight_type') 
        departure_time_range = filter_params.get('departure_time', [])  
        arrival_time_range = filter_params.get('arrival_time', [])  
        airlines = filter_params.get('airlines', [])  
        max_price = float(filter_params.get('max_price', float('inf')))

        def time_in_ranges(time_str, time_ranges):
            """Kiểm tra thời gian có nằm trong các khoảng cho phép"""
            if not time_ranges:
                return True
                
            flight_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S").time()
            
            for time_range in time_ranges:
                start_time, end_time = time_range.split('-')
                range_start = datetime.strptime(start_time, "%H:%M").time()
                range_end = datetime.strptime(end_time, "%H:%M").time()
                
                if range_start <= range_end:
                    if range_start <= flight_time <= range_end:
                        return True
                else:
                    if flight_time >= range_start or flight_time <= range_end:
                        return True
            return False

        def filter_flight(flight):
            if airlines and flight['ma_hhk'] not in airlines:
                return False

            if not time_in_ranges(flight['thoi_gian_di'], departure_time_range):
                return False

            if not time_in_ranges(flight['thoi_gian_den'], arrival_time_range):
                return False

            flight_price = min(
                flight.get('gia_ve_eco', float('inf')),
                flight.get('gia_ve_bus', float('inf'))
            )
            if flight_price > max_price:
                return False

            return True

        filtered_results = {
            'direct_flights': [],
            'connecting_flights': [],
            'return_direct_flights': [],
            'return_connecting_flights': []
        }

        if flight_type in [None, 'direct', 'all']:
            filtered_results['direct_flights'] = [
                flight for flight in flights_data.get('direct_flights', [])
                if filter_flight(flight)
            ]
            filtered_results['return_direct_flights'] = [
                flight for flight in flights_data.get('return_direct_flights', [])
                if filter_flight(flight)
            ]

        if flight_type in [None, '1stop', 'all']:
            filtered_results['connecting_flights'] = [
                flight for flight in flights_data.get('connecting_flights', [])
                if all(filter_flight(f) for f in flight['flights'])
            ]
            filtered_results['return_connecting_flights'] = [
                flight for flight in flights_data.get('return_connecting_flights', [])
                if all(filter_flight(f) for f in flight['flights'])
            ]

        return jsonify({
            'status': 'success',
            'data': filtered_results
        })

    except Exception as e:
        print(f"Filter flights error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

