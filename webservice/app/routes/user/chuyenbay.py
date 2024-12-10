from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from app.models import ChuyenBay, MayBay, HangHangKhong, DichVu, DichVuVe, GoiDichVu, DichVuHanhLy,\
    HanhKhach, NguoiLienHe, DatCho, ChiTietDatCho, SanBay, BookingTamThoi, KhuyenMai, CB_KhuyenMai, HHK_KhuyenMai, ThanhToan
from app import db
from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy import func
import redis

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

       # Query với các join được chỉ định rõ ràng
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

       # Tính thời gian bay
       thoi_gian_bay = flight.ThoiGianDen - flight.ThoiGianDi
       hours = thoi_gian_bay.seconds // 3600 
       minutes = (thoi_gian_bay.seconds % 3600) // 60
       thoi_gian_bay_str = f"{hours}h {minutes}m"

       # Tạo response data
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
        
        # Validate input
        required_fields = ['san_bay_di', 'san_bay_den', 'ngay_di', 'so_luong_khach', 'loai_ghe']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse input parameters
        san_bay_di = data['san_bay_di']
        san_bay_den = data['san_bay_den']
        ngay_di = datetime.strptime(data['ngay_di'], '%d-%m-%Y').date()
        so_luong_khach = int(data['so_luong_khach'])
        loai_ghe = data['loai_ghe'].upper()  # 'ECO' or 'BUS'
        khu_hoi = data.get('khu_hoi', False)
        include_connecting = data.get('include_connecting', False)
        max_stops = data.get('max_stops', 3)  # Số điểm dừng tối đa
        
        # Tìm chuyến bay trực tiếp
        direct_flights = search_direct_flights(
            san_bay_di, san_bay_den, ngay_di, so_luong_khach, loai_ghe
        )
        
        # Tìm chuyến bay quá cảnh
        connecting_flights = []
        if include_connecting:
            connecting_routes = search_connecting_flights(
                san_bay_di, san_bay_den, ngay_di, 
                so_luong_khach, loai_ghe, max_stops
            )
            # Lọc bỏ các route None (không có điểm dừng)
            connecting_flights = [
                flight_dict for flight_dict in [
                    connecting_flight_to_dict(route, loai_ghe) 
                    for route in connecting_routes
                ]
                if flight_dict is not None  # Chỉ giữ lại các chuyến có điểm dừng
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
                # Lọc bỏ các route None
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

@chuyenbay.route('/api/flights/<ma_chuyen_bay>/services', methods=['POST'])
def get_flight_services_api(ma_chuyen_bay):
    """API endpoint để lấy danh sách dịch vụ của một chuyến bay"""
    try:
        data = request.get_json()
        loai_ghe = data.get('loai_ghe', 'ECO').upper()
        
        # Lấy thông tin chuyến bay
        flight = ChuyenBay.query\
            .join(MayBay)\
            .join(HangHangKhong)\
            .filter(ChuyenBay.MaChuyenBay == ma_chuyen_bay)\
            .first()
            
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404

        # Chuẩn bị thông tin chuyến bay để tìm dịch vụ
        flight_info = {
            'ma_hhk': flight.may_bay.MaHHK,
            'loai_ghe': loai_ghe,
            'gia_ve_eco': float(flight.GiaVeEco) if flight.GiaVeEco else None,
            'gia_ve_bus': float(flight.GiaVeBus) if flight.GiaVeBus else None
        }

        # Sử dụng hàm get_flight_services đã có
        services = get_flight_services(flight_info)

        return jsonify({
            'flight': flight_to_dict(flight, loai_ghe),
            'goi_dich_vu': services
        })

    except Exception as e:
        print(f"Get flight services error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def search_direct_flights(san_bay_di: str, san_bay_den: str, 
                        ngay_di: datetime.date, so_luong_khach: int, 
                        loai_ghe: str) -> List[ChuyenBay]:
    """Tìm các chuyến bay trực tiếp theo điều kiện"""
    
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
    """
    Tìm các chuyến bay quá cảnh nhiều chặng
    
    Args:
        san_bay_di: Mã sân bay đi
        san_bay_den: Mã sân bay đến
        ngay_di: Ngày đi
        so_luong_khach: Số lượng khách
        loai_ghe: Loại ghế (ECO/BUS)
        max_stops: Số điểm dừng tối đa
    """
    try:
        min_layover = timedelta(hours=2)
        max_layover = timedelta(hours=8)
        max_total_time = timedelta(hours=36)  # Giới hạn tổng thời gian bay
        
        def find_connecting_flights(current_route: List[ChuyenBay], visited_airports: set) -> List[List[ChuyenBay]]:
            """Tìm các chuyến bay kết nối tiếp theo có thể kết nối"""
            
            # Nếu đã đến sân bay đích
            last_flight = current_route[-1]
            if last_flight.MaSanBayDen == san_bay_den:
                return [current_route]

            # Kiểm tra điều kiện dừng
            if len(current_route) >= max_stops + 1:  # +1 vì số chặng = số điểm dừng + 1
                return []
                
            # Kiểm tra tổng thời gian bay
            total_time = last_flight.ThoiGianDen - current_route[0].ThoiGianDi
            if total_time > max_total_time:
                return []

            # Tìm các chuyến bay tiếp theo
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

        # Tìm chuyến bay đầu tiên
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
        
        # Sắp xếp các route theo tổng thời gian bay
        all_routes.sort(key=lambda route: (route[-1].ThoiGianDen - route[0].ThoiGianDi))
        
        return all_routes
        
    except Exception as e:
        print(f"Search connecting flights error: {str(e)}")
        return []

def get_flight_services(flight_dict):
    """Lấy thông tin các gói dịch vụ cho một chuyến bay"""
    try:
        ma_hhk = flight_dict['ma_hhk']
        loai_ve = 'Business' if flight_dict.get('loai_ghe', '').upper() == 'BUS' else 'Economy'
        
        # Lấy tất cả các gói dịch vụ có sẵn
        services = db.session.query(
            DichVuVe, DichVu, GoiDichVu
        ).join(
            DichVu,
            DichVuVe.MaDV == DichVu.MaDV
        ).join(
            GoiDichVu,
            DichVuVe.MaGoi == GoiDichVu.MaGoi
        ).filter(
            DichVuVe.MaHHK == ma_hhk,
            DichVuVe.LoaiVeApDung == loai_ve,
            GoiDichVu.TrangThai == 0
        ).all()

        if not services:
            return {}

        packages = {}
        for dv_ve, dv, goi in services:
            if goi.MaGoi not in packages:
                # Tính giá gói
                base_price = flight_dict['gia_ve_bus'] if loai_ve == 'Business' else flight_dict['gia_ve_eco']
                if base_price is None:
                    continue
                    
                package_price = float(base_price) * float(goi.HeSoGia)
                
                packages[goi.MaGoi] = {
                    'ma_goi': goi.MaGoi,
                    'ten_goi': goi.TenGoi,
                    'mo_ta': goi.MoTa,
                    'gia_goi': package_price,
                    'dich_vu': []
                }
            
            # Thêm chi tiết dịch vụ
            chi_tiet = ''
            if 'xách tay' in dv.TenDichVu.lower():
                chi_tiet = f'Được phép mang {dv_ve.ThamSo}kg hành lý xách tay'
            elif 'ký gửi' in dv.TenDichVu.lower():
                chi_tiet = f'Được phép ký gửi {dv_ve.ThamSo}kg hành lý'
            elif 'đổi' in dv.TenDichVu.lower():
                chi_tiet = f'Phí đổi vé: {dv_ve.ThamSo}% giá vé'
            elif 'hoàn' in dv.TenDichVu.lower():
                chi_tiet = f'Hoàn {dv_ve.ThamSo}% giá vé'
            elif 'bảo hiểm' in dv.TenDichVu.lower():
                chi_tiet = 'Có bảo hiểm du lịch' if dv_ve.ThamSo > 0 else 'Không có bảo hiểm'

            packages[goi.MaGoi]['dich_vu'].append({
                'ma_dv': dv.MaDV,
                'ten_dich_vu': dv.TenDichVu,
                'mo_ta': dv.MoTa,
                'tham_so': float(dv_ve.ThamSo),
                'chi_tiet': chi_tiet
            })
        
        return packages
        
    except Exception as e:
        print(f"Get flight services error: {str(e)}")
        return {}

def flight_to_dict(flight, loai_ghe='ECO'):
    """Convert flight object to dictionary"""
    try:
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
            'loai_ghe': loai_ghe.upper(),
            'thoi_gian_bay': (flight.ThoiGianDen - flight.ThoiGianDi).total_seconds() / 3600,
        }
    except Exception as e:
        print(f"Convert flight to dict error: {str(e)}")
        return {}

def connecting_flight_to_dict(flights: List[ChuyenBay], loai_ghe='ECO') -> dict:
    """Convert danh sách chuyến bay thành dictionary"""
    try:
        # Nếu không có điểm dừng (chỉ 1 chuyến bay), return None
        if len(flights) <= 1:
            return None
            
        flight_dicts = []
        layover_times = []
        tong_gia = 0
        
        for i, flight in enumerate(flights):
            flight_dict = flight_to_dict(flight, loai_ghe)
            flight_dicts.append(flight_dict)
            
            # Tính giá vé
            if loai_ghe == 'ECO':
                gia_ve = flight_dict.get('gia_ve_eco', 0) or 0
            else:
                gia_ve = flight_dict.get('gia_ve_bus', 0) or 0
            tong_gia += gia_ve
            
            # Tính thời gian chờ giữa các chuyến
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

@chuyenbay.route('/api/flights/<ma_chuyen_bay>/luggage-services', methods=['GET'])
def get_luggage_services(ma_chuyen_bay):
    """API lấy danh sách dịch vụ hành lý của chuyến bay"""
    try:
        services = DichVuHanhLy.query.filter_by(MaCB=ma_chuyen_bay).all()
        
        return jsonify({
            'dich_vu_hanh_ly': [{
                'ma_dich_vu': dv.MaDichVu,
                'so_ky': dv.SoKy,
                'gia': float(dv.Gia),
                'mo_ta': dv.MoTa
            } for dv in services]
        })
    except Exception as e:
        print(f"Get luggage services error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# @chuyenbay.route('/api/flights/<ma_chuyen_bay>/booking', methods=['POST'])
# def create_booking(ma_chuyen_bay):
#     """API đặt chỗ cho chuyến bay (không bao gồm hành lý)"""
#     try:
#         data = request.get_json()
        
#         # Validate dữ liệu người liên hệ
#         required_contact = ['ho_nlh', 'ten_nlh', 'email', 'sdt']
#         for field in required_contact:
#             if field not in data['nguoi_lien_he']:
#                 return jsonify({'error': f'Thiếu thông tin người liên hệ: {field}'}), 400

#         # Validate dữ liệu hành khách
#         required_passenger = ['ho_hk', 'ten_hk', 'danh_xung', 'cccd', 'ngay_sinh', 'quoc_tich', 'loai_hk']
#         for passenger in data['hanh_khach']:
#             for field in required_passenger:
#                 if field not in passenger:
#                     return jsonify({'error': f'Thiếu thông tin hành khách: {field}'}), 400

#         # Kiểm tra chuyến bay
#         flight = ChuyenBay.query.get(ma_chuyen_bay)
#         if not flight:
#             return jsonify({'error': 'Không tìm thấy chuyến bay'}), 404

#         # Kiểm tra số lượng ghế
#         so_ghe_bus = data.get('so_ghe_bus', 0)
#         so_ghe_eco = data.get('so_ghe_eco', 0)
        
#         if flight.SLBusConLai < so_ghe_bus:
#             return jsonify({'error': 'Không đủ ghế Business'}), 400
#         if flight.SLEcoConLai < so_ghe_eco:
#             return jsonify({'error': 'Không đủ ghế Economy'}), 400

#         # Thêm người liên hệ
#         nguoi_lien_he = NguoiLienHe(
#             HoNLH=data['nguoi_lien_he']['ho_nlh'],
#             TenNLH=data['nguoi_lien_he']['ten_nlh'],
#             Email=data['nguoi_lien_he']['email'],
#             SDT=data['nguoi_lien_he']['sdt']
#         )
#         db.session.add(nguoi_lien_he)
#         db.session.flush()

#         # Tạo đặt chỗ
#         dat_cho = DatCho(
#             MaCB=ma_chuyen_bay,
#             MaNLH=nguoi_lien_he.MaNLH,
#             SoLuongGheBus=so_ghe_bus,
#             SoLuongGheEco=so_ghe_eco,
#             TrangThai='Đang thanh toán',
#             MaND=data['ma_nd']
#         )
#         db.session.add(dat_cho)
#         db.session.flush()

#         # Thêm hành khách (không bao gồm dịch vụ hành lý)
#         added_passengers = []
#         for passenger_data in data['hanh_khach']:
#             hanh_khach = HanhKhach(
#                 HoHK=passenger_data['ho_hk'],
#                 TenHK=passenger_data['ten_hk'],
#                 DanhXung=passenger_data['danh_xung'],
#                 CCCD=passenger_data['cccd'],
#                 NgaySinh=datetime.strptime(passenger_data['ngay_sinh'], '%d-%m-%Y').date(),
#                 QuocTich=passenger_data['quoc_tich'],
#                 LoaiHK=passenger_data['loai_hk']
#             )
#             db.session.add(hanh_khach)
#             db.session.flush()
#             added_passengers.append(hanh_khach)

#             # Tạo chi tiết đặt chỗ (chưa có dịch vụ hành lý)
#             chi_tiet = ChiTietDatCho(
#                 MaDatCho=dat_cho.MaDatCho,
#                 MaHK=hanh_khach.MaHanhKhach
#             )
#             db.session.add(chi_tiet)

#         # Cập nhật số ghế còn lại
#         flight.SLBusConLai -= so_ghe_bus
#         flight.SLEcoConLai -= so_ghe_eco

#         db.session.commit()

#         return jsonify({
#             'ma_dat_cho': dat_cho.MaDatCho,
#             'nguoi_lien_he': {
#                 'ma_nlh': nguoi_lien_he.MaNLH,
#                 'ho_ten': f"{nguoi_lien_he.HoNLH} {nguoi_lien_he.TenNLH}",
#                 'email': nguoi_lien_he.Email,
#                 'sdt': nguoi_lien_he.SDT
#             },
#             'hanh_khach': [{
#                 'ma_hk': hk.MaHanhKhach,
#                 'ho_ten': f"{hk.HoHK} {hk.TenHK}",
#                 'cccd': hk.CCCD,
#                 'loai_hk': hk.LoaiHK
#             } for hk in added_passengers],
#             'thong_tin_chuyen_bay': {
#                 'ma_chuyen_bay': flight.MaChuyenBay,
#                 'so_ghe_bus': so_ghe_bus,
#                 'so_ghe_eco': so_ghe_eco,
#                 'trang_thai': dat_cho.TrangThai
#             }
#         })

#     except Exception as e:
#         db.session.rollback()
#         print(f"Booking error: {str(e)}")
#         return jsonify({'error': str(e)}), 500

@chuyenbay.route('/api/booking/<ma_dat_cho>/luggage', methods=['POST'])
def add_luggage_services(ma_dat_cho):
    """API thêm dịch vụ hành lý cho đặt chỗ"""
    try:
        data = request.get_json()
        
        # Kiểm tra đặt chỗ
        booking = DatCho.query.get(ma_dat_cho)
        if not booking:
            return jsonify({'error': 'Không tìm thấy đặt chỗ'}), 404
            
        if booking.TrangThai != 'Đang thanh toán':
            return jsonify({'error': 'Không thể thêm dịch vụ cho đặt chỗ này'}), 400

        # Format dữ liệu: [{ ma_hanh_khach: 1, ma_dich_vu: 2 }, ...]
        for luggage_data in data['dich_vu_hanh_ly']:
            ma_hk = luggage_data.get('ma_hanh_khach')
            ma_dv = luggage_data.get('ma_dich_vu')
            
            if not ma_hk or not ma_dv:
                continue
                
            # Kiểm tra dịch vụ hành lý tồn tại và thuộc chuyến bay
            dich_vu = DichVuHanhLy.query.filter_by(
                MaDichVu=ma_dv,
                MaCB=booking.MaCB
            ).first()
            
            if not dich_vu:
                return jsonify({'error': f'Dịch vụ hành lý không hợp lệ: {ma_dv}'}), 400

            # Cập nhật chi tiết đặt chỗ
            chi_tiet = ChiTietDatCho.query.filter_by(
                MaDatCho=ma_dat_cho,
                MaHK=ma_hk
            ).first()
            
            if chi_tiet:
                chi_tiet.MaDichVu = ma_dv

        db.session.commit()
        
        # Lấy thông tin đã cập nhật
        updated_services = db.session.query(
            HanhKhach, DichVuHanhLy
        ).join(
            ChiTietDatCho, HanhKhach.MaHanhKhach == ChiTietDatCho.MaHK
        ).outerjoin(
            DichVuHanhLy, ChiTietDatCho.MaDichVu == DichVuHanhLy.MaDichVu
        ).filter(
            ChiTietDatCho.MaDatCho == ma_dat_cho
        ).all()

        return jsonify({
            'hanh_khach': [{
                'ma_hk': hk.MaHanhKhach,
                'ho_ten': f"{hk.HoHK} {hk.TenHK}",
                'dich_vu_hanh_ly': {
                    'ma_dich_vu': dv.MaDichVu,
                    'so_ky': dv.SoKy,
                    'gia': float(dv.Gia),
                    'mo_ta': dv.MoTa
                } if dv else None
            } for hk, dv in updated_services]
        })

    except Exception as e:
        db.session.rollback()
        print(f"Add luggage services error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chuyenbay.route('/api/flights/filter', methods=['POST'])
def filter_flights():
    try:
        data = request.get_json()
        flights_data = data.get('flights', {})
        filter_params = data.get('filters', {})

        # Lấy các tham số lọc
        flight_type = filter_params.get('flight_type')  # 'direct' hoặc '1stop'
        departure_time_range = filter_params.get('departure_time', [])  # List các khoảng thời gian
        arrival_time_range = filter_params.get('arrival_time', [])  # List các khoảng thời gian
        airlines = filter_params.get('airlines', [])  # List mã hãng hàng không
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
                
                # Xử lý trường hợp khoảng thời gian qua nửa đêm
                if range_start <= range_end:
                    if range_start <= flight_time <= range_end:
                        return True
                else:
                    if flight_time >= range_start or flight_time <= range_end:
                        return True
            return False

        def filter_flight(flight):
            """Áp dụng các điều kiện lọc cho một chuyến bay"""
            # Lọc theo hãng hàng không
            if airlines and flight['ma_hhk'] not in airlines:
                return False

            # Lọc theo giờ khởi hành
            if not time_in_ranges(flight['thoi_gian_di'], departure_time_range):
                return False

            # Lọc theo giờ đến
            if not time_in_ranges(flight['thoi_gian_den'], arrival_time_range):
                return False

            # Lọc theo giá
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

        # Lọc chuyến bay theo loại
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


@chuyenbay.route('/api/packages/<int:ma_goi>/luggage', methods=['GET'])  
def get_package_luggage(ma_goi):
    """
    API lấy thông tin hành lý của gói dịch vụ.
    Tham số:
        - ma_goi (path): Mã gói dịch vụ (1-4)
        - hang_hang_khong (query): Tên hãng hàng không (Vietnam Airlines, VietJet Air...)
        - loai_ve (query): Loại vé (ECO/BUS)
    """
    try:
        hang_hang_khong = request.args.get('hang_hang_khong')
        loai_ve = request.args.get('loai_ve')

        # Validate input
        if not hang_hang_khong or not loai_ve:
            return jsonify({
                'error': 'Thiếu thông tin hãng hàng không hoặc loại vé'
            }), 400

        # Validate loai_ve
        if loai_ve not in ['ECO', 'BUS']:
            return jsonify({
                'error': 'Loại vé không hợp lệ. Chỉ chấp nhận ECO hoặc BUS'
            }), 400

        # Map loại vé
        loai_ve_mapping = {
            'ECO': 'Economy',
            'BUS': 'Business'
        }
        loai_ve_query = loai_ve_mapping.get(loai_ve)

        # Lấy mã hãng hàng không từ tên
        hang_hk = HangHangKhong.query.filter(
            (HangHangKhong.TenHHK == hang_hang_khong) | 
            (HangHangKhong.MaHHK == hang_hang_khong)
        ).first()
        
        if not hang_hk:
            return jsonify({
                'error': f'Không tìm thấy hãng hàng không: {hang_hang_khong}'
            }), 404

        # Get luggage info from database
        goi_dv = GoiDichVu.query.get(ma_goi)
        if not goi_dv:
            return jsonify({'error': f'Không tìm thấy gói dịch vụ với mã {ma_goi}'}), 404

        # Query lấy thông tin hành lý
        luggage_info = db.session.query(
            DichVu.MaDV,
            DichVu.TenDichVu,
            DichVuVe.ThamSo,
            HangHangKhong.TenHHK
        ).join(
            DichVuVe, 
            DichVu.MaDV == DichVuVe.MaDV
        ).join(
            HangHangKhong,
            DichVuVe.MaHHK == HangHangKhong.MaHHK
        ).filter(
            DichVuVe.MaGoi == ma_goi,
            DichVuVe.MaHHK == hang_hk.MaHHK, 
            DichVuVe.LoaiVeApDung == loai_ve_query,
            DichVu.TenDichVu.in_(['Hành lý xách tay', 'Hành lý ký gửi'])
        ).all()

        if not luggage_info:
            return jsonify({
                'error': f'Không tìm thấy thông tin hành lý cho gói {ma_goi}, ' + 
                        f'hãng {hang_hang_khong}, loại vé {loai_ve}'
            }), 404

        # Format response
        luggage_details = {}
        total_weight = 0
        ten_hang = None
        
        for item in luggage_info:
            weight = float(item.ThamSo) if item.ThamSo else 0
            luggage_details[item.TenDichVu] = weight
            total_weight += weight
            if not ten_hang:
                ten_hang = item.TenHHK

        return jsonify({
            'ma_goi': ma_goi,
            'ten_goi': goi_dv.TenGoi,
            'hang_hang_khong': ten_hang,
            'loai_ve': loai_ve,  # Trả về ECO/BUS như input
            'tong_hanh_ly': total_weight,
            'chi_tiet': {
                'hanh_ly_xach_tay': luggage_details.get('Hành lý xách tay', 0),
                'hanh_ly_ky_gui': luggage_details.get('Hành lý ký gửi', 0)
            }
        })

    except Exception as e:
        print(f"Error getting luggage info: {str(e)}")
        return jsonify({'error': 'Lỗi hệ thống'}), 500

import random
@chuyenbay.route('/api/booking', methods=['POST'])
def create_booking():
    """API đặt chỗ cho danh sách chuyến bay (bao gồm hành lý)"""
    try:
        # Dọn dẹp các booking hết hạn
        BookingTamThoi.cleanup_expired()
        
        data = request.get_json()
        
        # Validate dữ liệu người liên hệ
        required_contact = ['ho_nlh', 'ten_nlh', 'email', 'sdt']
        for field in required_contact:
            if field not in data['nguoi_lien_he']:
                return jsonify({'error': f'Thiếu thông tin người liên hệ: {field}'}), 400

        # Validate dữ liệu hành khách và hành lý
        required_passenger = ['ho_hk', 'ten_hk', 'danh_xung', 'cccd', 'ngay_sinh', 'quoc_tich', 'loai_hk']
        for passenger in data['hanh_khach']:
            for field in required_passenger:
                if field not in passenger:
                    return jsonify({'error': f'Thiếu thông tin hành khách: {field}'}), 400
            
            # Kiểm tra dịch vụ hành lý cho mỗi chuyến bay
            if 'dich_vu_hanh_ly' in passenger:
                for flight_luggage in passenger['dich_vu_hanh_ly']:
                    ma_chuyen_bay = flight_luggage.get('ma_chuyen_bay')
                    ma_dich_vu = flight_luggage.get('ma_dich_vu_hanh_ly')
                    
                    if ma_dich_vu:
                        dich_vu = DichVuHanhLy.query.get(ma_dich_vu)
                        if not dich_vu or dich_vu.MaCB != ma_chuyen_bay:
                            return jsonify({'error': f'Dịch vụ hành lý không hợp lệ cho chuyến bay {ma_chuyen_bay}'}), 400

        flight_updates = {}
        first_flight = None
        for flight_info in data['chuyen_bay']:
            ma_chuyen_bay = flight_info['ma_chuyen_bay']
            so_ghe_bus = flight_info.get('so_ghe_bus', 0) 
            so_ghe_eco = flight_info.get('so_ghe_eco', 0)
            
            flight = ChuyenBay.query.get(ma_chuyen_bay)
            if not flight:
                return jsonify({'error': f'Không tìm thấy chuyến bay {ma_chuyen_bay}'}), 404
            
            if first_flight is None:
                first_flight = flight
                
            if flight.SLBusConLai < so_ghe_bus:
                return jsonify({'error': f'Không đủ ghế Business cho chuyến bay {ma_chuyen_bay}'}), 400
            if flight.SLEcoConLai < so_ghe_eco:
                return jsonify({'error': f'Không đủ ghế Economy cho chuyến bay {ma_chuyen_bay}'}), 400
                
            # Chỉ lưu các giá trị scalar trong flight_updates
            flight_updates[ma_chuyen_bay] = {
                'ma_hhk': flight.may_bay.MaHHK,  # Thêm mã hãng hàng không
                'SLBusConLai': flight.SLBusConLai - so_ghe_bus,
                'SLEcoConLai': flight.SLEcoConLai - so_ghe_eco
            }

        # booking_code = f"BK{datetime.now().year % 100}{str(random.randint(1, 999999)).zfill(6)}"
        # Tạo mã đặt chỗ bằng cách kết hợp mã từ generate_booking_code và thời gian
        ma_hhk = first_flight.may_bay.MaHHK if first_flight else "unknown" # Lấy mã hãng hàng không từ chuyến bay đầu tiên
        generated_code = ChuyenBay.generate_flight_code(ma_hhk)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Định dạng thời gian: YYYYMMDDHHMMSS
        booking_code = f"{generated_code}-{timestamp}"

        print("flight-update: ", flight_updates)
        # Chuẩn bị thông tin phản hồi
        response_data = {
            'booking_id': booking_code,
            'expires_in': 600,
            'thong_tin_dat_cho': {
                'nguoi_lien_he': {
                    'ho_ten': f"{data['nguoi_lien_he']['ho_nlh']} {data['nguoi_lien_he']['ten_nlh']}",
                    'email': data['nguoi_lien_he']['email'],
                    'sdt': data['nguoi_lien_he']['sdt']
                },
                'hanh_khach': [{
                    'ho_ten': f"{p['ho_hk']} {p['ten_hk']}",
                    'cccd': p['cccd'],
                    'danh_xung': p['danh_xung'],
                    'ngay_sinh': p['ngay_sinh'],
                    'quoc_tich': p['quoc_tich'],
                    'loai_hk': p['loai_hk'],
                    'dich_vu_hanh_ly': p.get('dich_vu_hanh_ly', [])
                } for p in data['hanh_khach']],
                'chuyen_bay': [{
                    'ma_chuyen_bay': flight['ma_chuyen_bay'],
                    'so_ghe_bus': flight.get('so_ghe_bus', 0),
                    'so_ghe_eco': flight.get('so_ghe_eco', 0)
                } for flight in data['chuyen_bay']],
                'flight_updates': flight_updates
            }
        }

        # Lưu booking tạm thời vào database
        temp_booking = BookingTamThoi(
            BookingId=booking_code,
            Data=response_data,
            CreatedAt=datetime.utcnow(),
            ExpiresAt=datetime.utcnow() + timedelta(minutes=10)
        )

        db.session.add(temp_booking)
        db.session.commit()
        return jsonify(response_data)

    except Exception as e:
        db.session.rollback()
        print(f"Booking error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@chuyenbay.route('/api/bookings/<booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    """API xác nhận và lưu đặt chỗ vào database sau khi thanh toán và áp dụng mã giảm giá"""
    try:
        BookingTamThoi.cleanup_expired()
        # Lấy thông tin booking tạm thời
        temp_booking = BookingTamThoi.query.get(booking_id)
        if not temp_booking or temp_booking.ExpiresAt < datetime.utcnow():
            return jsonify({'error': 'Đặt chỗ đã hết hạn hoặc không tồn tại'}), 404

        booking_data = temp_booking.Data
        thong_tin = booking_data['thong_tin_dat_cho']
        flight_updates = thong_tin.get('flight_updates', {})
        data = request.get_json()
        # Áp dụng mã khuyến mãi nếu có
        tien_giam = 0
        ma_khuyen_mai = None
        tong_tien = data.get('tong_tien', 0)  # Lấy tổng tiền từ JSON payload
        if 'ma_khuyen_mai' in data:  # Lấy mã khuyến mãi từ JSON payload
            ma_khuyen_mai = data['ma_khuyen_mai']
            khuyen_mai = KhuyenMai.query.get(ma_khuyen_mai)
            if khuyen_mai and khuyen_mai.is_valid():
                tien_giam = khuyen_mai.calculate_discount(tong_tien)
                print("tien_giam: ", tien_giam)
            else:
                return jsonify({'error': 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn'}), 400


        # Kiểm tra và cập nhật/lưu thông tin người liên hệ
        email = thong_tin['nguoi_lien_he']['email']
        nguoi_lien_he = NguoiLienHe.query.filter_by(Email=email).first()
        if nguoi_lien_he:
            # Cập nhật thông tin nếu đã tồn tại
            nguoi_lien_he.HoNLH = " ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1])
            nguoi_lien_he.TenNLH = thong_tin['nguoi_lien_he']['ho_ten'].split()[-1]
            nguoi_lien_he.SDT = thong_tin['nguoi_lien_he']['sdt']
        else:
            # Thêm mới nếu chưa tồn tại
            nguoi_lien_he = NguoiLienHe(
                HoNLH=" ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1]),
                TenNLH=thong_tin['nguoi_lien_he']['ho_ten'].split()[-1],
                Email=email,
                SDT=thong_tin['nguoi_lien_he']['sdt']
            )
            db.session.add(nguoi_lien_he)
        db.session.flush()


        # Tạo các đặt chỗ cho chuyến bay
        danh_sach_dat_cho = []
        for i, chuyen_bay in enumerate(thong_tin['chuyen_bay']):
            ma_chuyen_bay = chuyen_bay['ma_chuyen_bay']
            so_ghe_bus = chuyen_bay['so_ghe_bus']
            so_ghe_eco = chuyen_bay['so_ghe_eco']

            # Tạo bản ghi đặt chỗ
            dat_cho = DatCho(
                MaCB=ma_chuyen_bay,
                MaNLH=nguoi_lien_he.MaNLH,
                SoLuongGheBus=so_ghe_bus,
                SoLuongGheEco=so_ghe_eco,
                TrangThai='Đã thanh toán',
                NgayMua=datetime.utcnow(),
                MaND=2
            )
            db.session.add(dat_cho)
            db.session.flush()  
            danh_sach_dat_cho.append(dat_cho)


        # Lưu thông tin hành khách
        for hanh_khach_data in thong_tin['hanh_khach']:
            cccd = hanh_khach_data['cccd']
            hanh_khach = HanhKhach.query.filter_by(CCCD=cccd).first()
            if hanh_khach:
                # Cập nhật thông tin nếu đã tồn tại
                hanh_khach.HoHK = " ".join(hanh_khach_data['ho_ten'].split()[:-1])
                hanh_khach.TenHK = hanh_khach_data['ho_ten'].split()[-1]
                hanh_khach.DanhXung = hanh_khach_data.get('danh_xung', '')
                hanh_khach.NgaySinh = datetime.strptime(hanh_khach_data['ngay_sinh'], '%d-%m-%Y').date()
                hanh_khach.QuocTich = hanh_khach_data.get('quoc_tich', 'Việt Nam')
                hanh_khach.LoaiHK = hanh_khach_data['loai_hk']
            else:
                # Thêm mới nếu chưa tồn tại
                hanh_khach = HanhKhach(
                    HoHK=" ".join(hanh_khach_data['ho_ten'].split()[:-1]),
                    TenHK=hanh_khach_data['ho_ten'].split()[-1],
                    DanhXung=hanh_khach_data.get('danh_xung', ''),
                    CCCD=cccd,
                    NgaySinh=datetime.strptime(hanh_khach_data['ngay_sinh'], '%d-%m-%Y').date(),
                    QuocTich=hanh_khach_data.get('quoc_tich', 'Việt Nam'),
                    LoaiHK=hanh_khach_data['loai_hk']
                )
                db.session.add(hanh_khach)
            db.session.flush()

            # Tạo chi tiết đặt chỗ
            for dat_cho in danh_sach_dat_cho:
                chi_tiet = ChiTietDatCho(
                    MaDatCho=dat_cho.MaDatCho,
                    MaHK=hanh_khach.MaHanhKhach
                )
                db.session.add(chi_tiet)
                # Cập nhật thông tin số ghế còn lại từ flight_updates
        for ma_chuyen_bay, update_data in flight_updates.items():
            flight = ChuyenBay.query.get(ma_chuyen_bay)
            if flight:
                flight.SLBusConLai = update_data['SLBusConLai']
                flight.SLEcoConLai = update_data['SLEcoConLai']
                db.session.add(flight)
        # Tạo thanh toán
        thanh_toan = ThanhToan(
            MaDatCho=danh_sach_dat_cho[0].MaDatCho,
            MaKhuyenMai=ma_khuyen_mai,
            TienGiam=tien_giam,
            Thue=0,
            SoTien=tong_tien - tien_giam,
            NgayThanhToan=datetime.utcnow(),
            PhuongThuc='Trực tiếp'
        )
        db.session.add(thanh_toan)

        # Xóa booking tạm thời
        db.session.delete(temp_booking)
        db.session.commit()

        # Phản hồi
        return jsonify({
            'success': True,
            'ma_dat_cho': [dat_cho.MaDatCho for dat_cho in danh_sach_dat_cho],
            'tien_giam': tien_giam,
            'tong_tien': thanh_toan.SoTien,
            'message': 'Đặt chỗ thành công'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



def calculate_booking_amount(dat_cho, chi_tiet_dat_cho):
    total = 0
    
    chuyen_bay = dat_cho.chuyen_bay
    total += chuyen_bay.GiaVeBus * dat_cho.SoLuongGheBus
    total += chuyen_bay.GiaVeEco * dat_cho.SoLuongGheEco
    
    for ctdc in chi_tiet_dat_cho:
        if ctdc.dich_vu_hanh_ly:
            total += ctdc.dich_vu_hanh_ly.Gia
            
    return total

# # LẤY THÔNG TIN KHUYẾN MÃI CHO MÃ ĐĂT CHỖ
# @chuyenbay.route('/api/bookings/<int:ma_dat_cho>/promotions', methods=['GET'])
# def get_booking_promotions(ma_dat_cho):
#     try:
        
#         dat_cho = DatCho.query.get(ma_dat_cho)
#         if not dat_cho:
#             return jsonify({'error': 'Không tìm thấy đặt chỗ'}), 404
            
#         chi_tiet_dat_cho = ChiTietDatCho.query.filter_by(MaDatCho=ma_dat_cho).all()
#         total_amount = calculate_booking_amount(dat_cho, chi_tiet_dat_cho)
        
#         chuyen_bay = dat_cho.chuyen_bay  
#         if not chuyen_bay:
#             return jsonify({'error': 'Không tìm thấy chuyến bay'}), 404
    
#         may_bay = chuyen_bay.may_bay 
#         if not may_bay:
#             return jsonify({'error': 'Không tìm thấy máy bay'}), 404
            
#         hang_hang_khong = may_bay.hang_hang_khong  
#         if not hang_hang_khong:
#             return jsonify({'error': 'Không tìm thấy hãng hàng không'}), 404
       
#         current_date = datetime.now().date()
        
#         all_promotions = KhuyenMai.query.filter(
#             KhuyenMai.NgayBatDau <= current_date,
#             KhuyenMai.NgayKetThuc >= current_date
#         ).all()

#         promotions_result = {
#             'HANG_HANG_KHONG': [],
#             'CHUYEN_BAY': []
#         }

#         for km in all_promotions:
#             if km.ds_hang_hang_khong:
#                 for hhk in km.ds_hang_hang_khong:
#                     if hhk.MaHHK == hang_hang_khong.MaHHK:
#                         tien_giam = km.calculate_discount(total_amount)
#                         promotions_result['HANG_HANG_KHONG'].append({
#                             'ma_khuyen_mai': km.MaKhuyenMai,
#                             'ten_khuyen_mai': km.TenKhuyenMai,
#                             'mo_ta': km.MoTa,
#                             'loai_khuyen_mai': km.LoaiKhuyenMai,
#                             'gia_tri': float(km.GiaTri),
#                             'tien_giam': float(tien_giam),
#                             'ap_dung_cho': hhk.MaHHK
#                         })
#                         break
                        
#             if km.ds_chuyen_bay:
#                 for cb in km.ds_chuyen_bay:
#                     if cb.MaChuyenBay == chuyen_bay.MaChuyenBay:
#                         tien_giam = km.calculate_discount(total_amount)
#                         promotions_result['CHUYEN_BAY'].append({
#                             'ma_khuyen_mai': km.MaKhuyenMai,
#                             'ten_khuyen_mai': km.TenKhuyenMai,
#                             'mo_ta': km.MoTa,
#                             'loai_khuyen_mai': km.LoaiKhuyenMai,
#                             'gia_tri': float(km.GiaTri),
#                             'tien_giam': float(tien_giam),
#                             'ap_dung_cho': cb.MaChuyenBay
#                         })
#                         break

#         return jsonify({
#             'tong_tien': float(total_amount),
#             'khuyen_mai': promotions_result
#         })


#     except Exception as e:
#         print(f"Error getting promotions: {str(e)}")
#         print(f"Error type: {type(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

@chuyenbay.route('/api/bookings/temp/promotions', methods=['POST'])
def get_temp_booking_promotions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Không có dữ liệu gửi lên'}), 400
            
        # Lấy thông tin từ request body
        list_hang_hang_khong = data.get('hang_hang_khong', [])  # List tên hãng hàng không
        list_ma_chuyen_bay = data.get('ma_chuyen_bay', [])
        tong_tien = data.get('tong_tien', 0)
        
        if not list_hang_hang_khong or not list_ma_chuyen_bay or not tong_tien:
            return jsonify({'error': 'Thiếu thông tin cần thiết'}), 400
            
        # Lấy thông tin các hãng hàng không
        hang_hang_khong_info = HangHangKhong.query.filter(
            HangHangKhong.TenHHK.in_(list_hang_hang_khong)
        ).all()
        
        if not hang_hang_khong_info:
            return jsonify({'error': 'Không tìm thấy hãng hàng không'}), 404
            
        ma_hhk_list = [hhk.MaHHK for hhk in hang_hang_khong_info]
        current_date = datetime.now().date()
        
        # Lấy khuyến mãi còn hiệu lực
        all_promotions = KhuyenMai.query.filter(
            KhuyenMai.NgayBatDau <= current_date,
            KhuyenMai.NgayKetThuc >= current_date
        ).all()

        promotions_result = {
            'HANG_HANG_KHONG': [],
            'CHUYEN_BAY': []
        }

        # Xử lý khuyến mãi hãng hàng không
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
