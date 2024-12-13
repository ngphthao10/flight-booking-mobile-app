from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from app.models import ChuyenBay, DichVuHanhLy, HanhKhach, NguoiLienHe, DatCho, ChiTietDatCho, BookingTamThoi, KhuyenMai, ThanhToan
from app import db
from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy import func
import redis

datcho = Blueprint('datcho', __name__)


@datcho.route('/api/booking', methods=['POST'])
def create_booking():
    try:
        BookingTamThoi.cleanup_expired()
        
        data = request.get_json()
        
        required_contact = ['ho_nlh', 'ten_nlh', 'email', 'sdt']
        for field in required_contact:
            if field not in data['nguoi_lien_he']:
                return jsonify({'error': f'Thiếu thông tin người liên hệ: {field}'}), 400

        required_passenger = ['ho_hk', 'ten_hk', 'danh_xung', 'cccd', 'ngay_sinh', 'quoc_tich', 'loai_hk']
        for passenger in data['hanh_khach']:
            for field in required_passenger:
                if field not in passenger:
                    return jsonify({'error': f'Thiếu thông tin hành khách: {field}'}), 400
            
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
                
            flight_updates[ma_chuyen_bay] = {
                'ma_hhk': flight.may_bay.MaHHK,  
                'SLBusConLai': flight.SLBusConLai - so_ghe_bus,
                'SLEcoConLai': flight.SLEcoConLai - so_ghe_eco
            }

        ma_hhk = first_flight.may_bay.MaHHK if first_flight else "unknown" 
        generated_code = ChuyenBay.generate_flight_code(ma_hhk)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  
        booking_code = f"{generated_code}-{timestamp}"

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


# @datcho.route('/api/bookings/<booking_id>/confirm', methods=['POST'])
# def confirm_booking(booking_id):
#     try:
#         BookingTamThoi.cleanup_expired()
#         temp_booking = BookingTamThoi.query.get(booking_id)
#         if not temp_booking or temp_booking.ExpiresAt < datetime.utcnow():
#             return jsonify({'error': 'Đặt chỗ đã hết hạn hoặc không tồn tại'}), 404

#         booking_data = temp_booking.Data
#         thong_tin = booking_data['thong_tin_dat_cho']
#         flight_updates = thong_tin.get('flight_updates', {})
#         data = request.get_json()
       
#         tien_giam = 0
#         ma_khuyen_mai = data.get('ma_khuyen_mai')  
#         tong_tien = data.get('tong_tien', 0) 
#         phuong_thuc = data.get('phuong_thuc', 0)

#         if ma_khuyen_mai: 
#             khuyen_mai = KhuyenMai.query.get(ma_khuyen_mai)
#             if khuyen_mai and khuyen_mai.is_valid():
#                 tien_giam = khuyen_mai.calculate_discount(tong_tien)
#                 print("tien_giam: ", tien_giam)
#             else:
#                 return jsonify({'error': 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn'}), 400


#         email = thong_tin['nguoi_lien_he']['email']
#         nguoi_lien_he = NguoiLienHe.query.filter_by(Email=email).first()
#         if nguoi_lien_he:
#             nguoi_lien_he.HoNLH = " ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1])
#             nguoi_lien_he.TenNLH = thong_tin['nguoi_lien_he']['ho_ten'].split()[-1]
#             nguoi_lien_he.SDT = thong_tin['nguoi_lien_he']['sdt']
#         else:
#             nguoi_lien_he = NguoiLienHe(
#                 HoNLH=" ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1]),
#                 TenNLH=thong_tin['nguoi_lien_he']['ho_ten'].split()[-1],
#                 Email=email,
#                 SDT=thong_tin['nguoi_lien_he']['sdt']
#             )
#             db.session.add(nguoi_lien_he)
#         db.session.flush()


#         danh_sach_dat_cho = []
#         for i, chuyen_bay in enumerate(thong_tin['chuyen_bay']):
#             ma_chuyen_bay = chuyen_bay['ma_chuyen_bay']
#             so_ghe_bus = chuyen_bay['so_ghe_bus']
#             so_ghe_eco = chuyen_bay['so_ghe_eco']

#             dat_cho = DatCho(
#                 MaCB=ma_chuyen_bay,
#                 MaNLH=nguoi_lien_he.MaNLH,
#                 SoLuongGheBus=so_ghe_bus,
#                 SoLuongGheEco=so_ghe_eco,
#                 TrangThai='Đã thanh toán',
#                 NgayMua=datetime.utcnow(),
#                 MaND=2
#             )
#             db.session.add(dat_cho)
#             db.session.flush()  
#             danh_sach_dat_cho.append(dat_cho)


#         for hanh_khach_data in thong_tin['hanh_khach']:
#             cccd = hanh_khach_data['cccd']
#             hanh_khach = HanhKhach.query.filter_by(CCCD=cccd).first()
#             if hanh_khach:
#                 hanh_khach.HoHK = " ".join(hanh_khach_data['ho_ten'].split()[:-1])
#                 hanh_khach.TenHK = hanh_khach_data['ho_ten'].split()[-1]
#                 hanh_khach.DanhXung = hanh_khach_data.get('danh_xung', '')
#                 hanh_khach.NgaySinh = datetime.strptime(hanh_khach_data['ngay_sinh'], '%d-%m-%Y').date()
#                 hanh_khach.QuocTich = hanh_khach_data.get('quoc_tich', 'Việt Nam')
#                 hanh_khach.LoaiHK = hanh_khach_data['loai_hk']
#             else:
#                 hanh_khach = HanhKhach(
#                     HoHK=" ".join(hanh_khach_data['ho_ten'].split()[:-1]),
#                     TenHK=hanh_khach_data['ho_ten'].split()[-1],
#                     DanhXung=hanh_khach_data.get('danh_xung', ''),
#                     CCCD=cccd,
#                     NgaySinh=datetime.strptime(hanh_khach_data['ngay_sinh'], '%d-%m-%Y').date(),
#                     QuocTich=hanh_khach_data.get('quoc_tich', 'Việt Nam'),
#                     LoaiHK=hanh_khach_data['loai_hk']
#                 )
#                 db.session.add(hanh_khach)
#             db.session.flush()

#             for dat_cho in danh_sach_dat_cho:
#                 chi_tiet = ChiTietDatCho(
#                     MaDatCho=dat_cho.MaDatCho,
#                     MaHK=hanh_khach.MaHanhKhach
#                 )
#                 db.session.add(chi_tiet)
#         for ma_chuyen_bay, update_data in flight_updates.items():
#             flight = ChuyenBay.query.get(ma_chuyen_bay)
#             if flight:
#                 flight.SLBusConLai = update_data['SLBusConLai']
#                 flight.SLEcoConLai = update_data['SLEcoConLai']
#                 db.session.add(flight)

#         thanh_toan = ThanhToan(
#             MaDatCho=danh_sach_dat_cho[0].MaDatCho,
#             MaKhuyenMai=ma_khuyen_mai if ma_khuyen_mai else None,
#             TienGiam=tien_giam,
#             Thue=0,
#             SoTien=tong_tien - tien_giam,
#             NgayThanhToan=datetime.utcnow(),
#             PhuongThuc=phuong_thuc
#         )
#         db.session.add(thanh_toan)

#         db.session.delete(temp_booking)
#         db.session.commit()

#         return jsonify({
#             'success': True,
#             'ma_dat_cho': [dat_cho.MaDatCho for dat_cho in danh_sach_dat_cho],
#             'tien_giam': tien_giam,
#             'tong_tien': thanh_toan.SoTien,
#             'message': 'Đặt chỗ thành công'
#         })

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

@datcho.route('/api/bookings/<booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    try:
        BookingTamThoi.cleanup_expired()
        temp_booking = BookingTamThoi.query.get(booking_id)
        if not temp_booking or temp_booking.ExpiresAt < datetime.utcnow():
            return jsonify({'error': 'Đặt chỗ đã hết hạn hoặc không tồn tại'}), 404

        booking_data = temp_booking.Data
        thong_tin = booking_data['thong_tin_dat_cho']
        flight_updates = thong_tin.get('flight_updates', {})
        data = request.get_json()
       
        tien_giam = 0
        ma_khuyen_mai = data.get('ma_khuyen_mai')  
        tong_tien = data.get('tong_tien', 0) 
        phuong_thuc = data.get('phuong_thuc', 0)

        if ma_khuyen_mai: 
            khuyen_mai = KhuyenMai.query.get(ma_khuyen_mai)
            if khuyen_mai and khuyen_mai.is_valid():
                tien_giam = khuyen_mai.calculate_discount(tong_tien)
            else:
                return jsonify({'error': 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn'}), 400

        email = thong_tin['nguoi_lien_he']['email']
        nguoi_lien_he = NguoiLienHe.query.filter_by(Email=email).first()
        if nguoi_lien_he:
            nguoi_lien_he.HoNLH = " ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1])
            nguoi_lien_he.TenNLH = thong_tin['nguoi_lien_he']['ho_ten'].split()[-1]
            nguoi_lien_he.SDT = thong_tin['nguoi_lien_he']['sdt']
        else:
            nguoi_lien_he = NguoiLienHe(
                HoNLH=" ".join(thong_tin['nguoi_lien_he']['ho_ten'].split()[:-1]),
                TenNLH=thong_tin['nguoi_lien_he']['ho_ten'].split()[-1],
                Email=email,
                SDT=thong_tin['nguoi_lien_he']['sdt']
            )
            db.session.add(nguoi_lien_he)
        db.session.flush()

        dat_cho_goc = DatCho(
            MaCB=thong_tin['chuyen_bay'][0]['ma_chuyen_bay'],
            MaNLH=nguoi_lien_he.MaNLH,
            SoLuongGheBus=thong_tin['chuyen_bay'][0]['so_ghe_bus'],
            SoLuongGheEco=thong_tin['chuyen_bay'][0]['so_ghe_eco'],
            TrangThai='Đã thanh toán',
            NgayMua=datetime.utcnow(),
            MaND=2
        )
        db.session.add(dat_cho_goc)
        db.session.flush()

        danh_sach_dat_cho = [dat_cho_goc]

        for chuyen_bay in thong_tin['chuyen_bay'][1:]:
            dat_cho = DatCho(
                MaCB=chuyen_bay['ma_chuyen_bay'],
                MaNLH=nguoi_lien_he.MaNLH,
                SoLuongGheBus=chuyen_bay['so_ghe_bus'],
                SoLuongGheEco=chuyen_bay['so_ghe_eco'],
                TrangThai='Đã thanh toán',
                NgayMua=datetime.utcnow(),
                MaND=2,
                MaDatChoGoc=dat_cho_goc.MaDatCho 
            )
            db.session.add(dat_cho)
            db.session.flush()
            danh_sach_dat_cho.append(dat_cho)

        for hanh_khach_data in thong_tin['hanh_khach']:
            cccd = hanh_khach_data['cccd']
            hanh_khach = HanhKhach.query.filter_by(CCCD=cccd).first()
            if hanh_khach:
                hanh_khach.HoHK = " ".join(hanh_khach_data['ho_ten'].split()[:-1])
                hanh_khach.TenHK = hanh_khach_data['ho_ten'].split()[-1]
                hanh_khach.DanhXung = hanh_khach_data.get('danh_xung', '')
                hanh_khach.NgaySinh = datetime.strptime(hanh_khach_data['ngay_sinh'], '%d-%m-%Y').date()
                hanh_khach.QuocTich = hanh_khach_data.get('quoc_tich', 'Việt Nam')
                hanh_khach.LoaiHK = hanh_khach_data['loai_hk']
            else:
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

            for dat_cho in danh_sach_dat_cho:
                chi_tiet = ChiTietDatCho(
                    MaDatCho=dat_cho.MaDatCho,
                    MaHK=hanh_khach.MaHanhKhach
                )
                db.session.add(chi_tiet)

        # Cập nhật số lượng ghế còn lại
        for ma_chuyen_bay, update_data in flight_updates.items():
            flight = ChuyenBay.query.get(ma_chuyen_bay)
            if flight:
                flight.SLBusConLai = update_data['SLBusConLai']
                flight.SLEcoConLai = update_data['SLEcoConLai']
                db.session.add(flight)

        # Tạo thanh toán cho đặt chỗ gốc
        thanh_toan = ThanhToan(
            MaDatCho=dat_cho_goc.MaDatCho,  # Chỉ lưu thanh toán cho đặt chỗ gốc
            MaKhuyenMai=ma_khuyen_mai if ma_khuyen_mai else None,
            TienGiam=tien_giam,
            Thue=0,
            SoTien=tong_tien - tien_giam,
            NgayThanhToan=datetime.utcnow(),
            PhuongThuc=phuong_thuc
        )
        db.session.add(thanh_toan)

        db.session.delete(temp_booking)
        db.session.commit()

        return jsonify({
            'success': True,
            'ma_dat_cho': [dat_cho.MaDatCho for dat_cho in danh_sach_dat_cho],
            'ma_dat_cho_goc': dat_cho_goc.MaDatCho,
            'tien_giam': tien_giam,
            'tong_tien': thanh_toan.SoTien,
            'message': 'Đặt chỗ thành công'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

