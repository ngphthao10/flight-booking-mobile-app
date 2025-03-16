from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import ChuyenBay, HangHangKhong, KhuyenMai, HHK_KhuyenMai, CB_KhuyenMai
from math import ceil
from app import db

adminKhuyenmai = Blueprint('adminKhuyenmai', __name__)

# Helper function to convert date string to datetime
def parse_date(date_string):
    return datetime.strptime(date_string, "%d/%m/%Y") if date_string else None

@adminKhuyenmai.route('/api/khuyen-mai', methods=['GET'])
def get_all_khuyen_mai():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        ma_km = request.args.get('ma_khuyen_mai', '')
        ten_km = request.args.get('ten_khuyen_mai', '') 
        loai_km = request.args.get('loai_khuyen_mai', '')

        query = KhuyenMai.query

        # Apply filters nếu có
        if ma_km:
            query = query.filter(KhuyenMai.MaKhuyenMai.ilike(f'%{ma_km}%'))
        if ten_km:
            query = query.filter(KhuyenMai.TenKhuyenMai.ilike(f'%{ten_km}%'))
        if loai_km:
            query = query.filter(KhuyenMai.LoaiKhuyenMai.ilike(f'%{loai_km}%'))

        # Phân trang
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        data = []
        for km in pagination.items:
            # Xác định đối tượng áp dụng khuyến mãi
            applied = None
            if km.ds_hang_hang_khong and len(km.ds_hang_hang_khong) > 0:
                applied = {
                    'type': 'airlines',
                    'value': km.ds_hang_hang_khong[0].TenHHK
                }
            elif km.ds_chuyen_bay and len(km.ds_chuyen_bay) > 0:
                flight = km.ds_chuyen_bay[0]
                applied = {
                    'type': 'flights',
                    'value': f"{flight.MaChuyenBay} ({flight.MaSanBayDi} → {flight.MaSanBayDen})"
                }

            data.append({
                'MaKhuyenMai': km.MaKhuyenMai,
                'TenKhuyenMai': km.TenKhuyenMai,
                'MoTa': km.MoTa,
                'LoaiKhuyenMai': km.LoaiKhuyenMai,
                'GiaTri': km.GiaTri,
                'NgayBatDau': km.NgayBatDau.strftime("%d/%m/%Y") if km.NgayBatDau else None,
                'NgayKetThuc': km.NgayKetThuc.strftime("%d/%m/%Y") if km.NgayKetThuc else None,
                'ApDungCho': applied
            })

        return jsonify({
            'status': True,
            'message': 'Lấy danh sách khuyến mãi thành công',
            'data': data,
            'pagination': {
                'total': pagination.total,
                'pages': pagination.pages,
                'page': page,
                'per_page': per_page
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': False, 
            'message': 'Có lỗi xảy ra', 
            'error': str(e)
        }), 500


@adminKhuyenmai.route('/api/khuyen-mai', methods=['POST', 'PUT'])
def create_or_update_khuyen_mai():
    try:
        data = request.get_json()
        perPage = 10
        
        # Các trường bắt buộc
        required_fields = ['MaKhuyenMai', 'TenKhuyenMai', 'LoaiKhuyenMai', 'GiaTri', 'NgayBatDau', 'NgayKetThuc']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': False,
                'message': 'Thiếu thông tin bắt buộc'
            }), 400
        
        # Parse dates
        ngay_bat_dau = parse_date(data.get('NgayBatDau'))
        ngay_ket_thuc = parse_date(data.get('NgayKetThuc'))
        
        # Ngày bắt đầu phải nhỏ hơn ngày kết thúc
        if ngay_bat_dau >= ngay_ket_thuc:
            return jsonify({
                'status': False,
                'message': 'Ngày bắt đầu phải nhỏ hơn ngày kết thúc'
            }), 400
        
        # Kiểm tra giá trị của Loại khuyến mãi
        if data['LoaiKhuyenMai'] not in ['Trực tiếp', 'Phần trăm']:
            return jsonify({
                'status': False,
                'message': 'Loại khuyến mãi phải là "Trực tiếp" hoặc "Phần trăm"'
            }), 400

        # Nếu là PUT (Cập nhật khuyến mãi)
        if request.method == 'PUT':
            existing_km = KhuyenMai.query.filter_by(MaKhuyenMai=data['MaKhuyenMai']).first()
            if not existing_km:
                return jsonify({'status': False, 'message': 'Khuyến mãi không tồn tại'}), 404

            # Cập nhật thông tin khuyến mãi
            existing_km.TenKhuyenMai = data.get('TenKhuyenMai')
            existing_km.MoTa = data.get('MoTa')
            existing_km.LoaiKhuyenMai = data.get('LoaiKhuyenMai')
            existing_km.GiaTri = data.get('GiaTri')
            existing_km.NgayBatDau = ngay_bat_dau
            existing_km.NgayKetThuc = ngay_ket_thuc

            # Xử lý cập nhật thông tin áp dụng khuyến mãi
            apply_type = data.get('ApplyType')
            if apply_type == 'airlines':
                # Xóa dữ liệu cũ trước khi thêm mới
                HHK_KhuyenMai.query.filter_by(MaKM=existing_km.MaKhuyenMai).delete()
                if data.get('HangHangKhong'):
                    new_join = HHK_KhuyenMai(
                        MaHHK=data.get('HangHangKhong'),
                        MaKM=existing_km.MaKhuyenMai
                    )
                    db.session.add(new_join)

            elif apply_type == 'flights':
                # Xóa dữ liệu cũ trước khi thêm mới
                CB_KhuyenMai.query.filter_by(MaKM=existing_km.MaKhuyenMai).delete()
                if data.get('ChuyenBay'):
                    new_join = CB_KhuyenMai(
                        MaCB=data.get('ChuyenBay'),
                        MaKM=existing_km.MaKhuyenMai
                    )
                    db.session.add(new_join)

            db.session.commit()
            return jsonify({'status': True, 'message': 'Khuyến mãi đã được cập nhật thành công'}), 200

        # Nếu là POST (Tạo mới khuyến mãi)
        else:
            # Kiểm tra mã khuyến mãi có tồn tại không
            existing_khuyenmai = KhuyenMai.query.filter_by(MaKhuyenMai=data['MaKhuyenMai']).first()
            if existing_khuyenmai:
                return jsonify({
                    'status': False,
                    'message': f"Mã khuyến mãi '{data['MaKhuyenMai']}' đã tồn tại"
                }), 400

            # Tạo mới đối tượng KhuyenMai
            new_khuyen_mai = KhuyenMai(
                MaKhuyenMai=data.get('MaKhuyenMai'),
                TenKhuyenMai=data.get('TenKhuyenMai'),
                MoTa=data.get('MoTa'),
                LoaiKhuyenMai=data.get('LoaiKhuyenMai'),
                GiaTri=data.get('GiaTri'),
                NgayBatDau=ngay_bat_dau,
                NgayKetThuc=ngay_ket_thuc
            )
            db.session.add(new_khuyen_mai)
            db.session.flush()  # Flush để đảm bảo new_khuyen_mai có giá trị primary key

            # Xử lý thêm dữ liệu vào bảng join nếu có thông tin áp dụng
            apply_type = data.get('ApplyType')
            if apply_type == 'airlines' and data.get('HangHangKhong'):
                new_join = HHK_KhuyenMai(
                    MaHHK=data.get('HangHangKhong'),
                    MaKM=new_khuyen_mai.MaKhuyenMai
                )
                db.session.add(new_join)
            elif apply_type == 'flights' and data.get('ChuyenBay'):
                new_join = CB_KhuyenMai(
                    MaCB=data.get('ChuyenBay'),
                    MaKM=new_khuyen_mai.MaKhuyenMai
                )
                db.session.add(new_join)

            db.session.commit()

            total = KhuyenMai.query.count()
            pages = ceil(total / perPage)

            return jsonify({'status': True, 'message': 'Khuyến mãi được tạo thành công'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': False, 
            'message': 'Có lỗi xảy ra', 
            'error': str(e)
        }), 500


@adminKhuyenmai.route('/api/khuyen-mai/<string:ma_khuyen_mai>', methods=['GET'])
def get_khuyen_mai(ma_khuyen_mai):
    try:
        km = KhuyenMai.query.filter_by(MaKhuyenMai=ma_khuyen_mai).first()
        if not km:
            return jsonify({
                'status': False, 
                'message': 'Khuyến mãi không tồn tại'
            }), 404

        data = {
            'MaKhuyenMai': km.MaKhuyenMai,
            'TenKhuyenMai': km.TenKhuyenMai,
            'MoTa': km.MoTa,
            'LoaiKhuyenMai': km.LoaiKhuyenMai,
            'GiaTri': km.GiaTri,
            'NgayBatDau': km.NgayBatDau.strftime("%d/%m/%Y") if km.NgayBatDau else None,
            'NgayKetThuc': km.NgayKetThuc.strftime("%d/%m/%Y") if km.NgayKetThuc else None
        }
        return jsonify({
            'status': True, 
            'message': 'Lấy thông tin khuyến mãi thành công', 'data': data
        }), 200

    except Exception as e:
        return jsonify({
            'status': False, 'message': 'Có lỗi xảy ra khi lấy thông tin khuyến mãi', 
            'error': str(e)
        }), 500

@adminKhuyenmai.route('/api/khuyen-mai/<string:ma_khuyen_mai>', methods=['PUT'])
def update_khuyen_mai(ma_khuyen_mai):
    try:
        data = request.get_json()

        required_fields = ['TenKhuyenMai', 'LoaiKhuyenMai', 'GiaTri', 'NgayBatDau', 'NgayKetThuc']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': False,
                'message': 'Thiếu thông tin bắt buộc'
            }), 400

        km = KhuyenMai.query.filter_by(MaKhuyenMai=ma_khuyen_mai).first()
        if not km:
            return jsonify({
                'status': False, 
                'message': 'Khuyến mãi không tồn tại'
            }), 404

        if data['LoaiKhuyenMai'] not in ['Trực tiếp', 'Phần trăm']:
            return jsonify({
                'status': False,
                'message': 'Loại khuyến mãi phải là "Trực tiếp" hoặc "Phần trăm"'
            }), 400
        
        # Update fields
        km.TenKhuyenMai = data.get('TenKhuyenMai', km.TenKhuyenMai)
        km.MoTa = data.get('MoTa', km.MoTa)
        km.LoaiKhuyenMai = data.get('LoaiKhuyenMai', km.LoaiKhuyenMai)
        km.GiaTri = data.get('GiaTri', km.GiaTri)
        km.NgayBatDau = parse_date(data.get('NgayBatDau')) if data.get('NgayBatDau') else km.NgayBatDau
        km.NgayKetThuc = parse_date(data.get('NgayKetThuc')) if data.get('NgayKetThuc') else km.NgayKetThuc

        db.session.commit()

        total = KhuyenMai.query.count()
        pages = ceil(total / 10)  # Assuming perPage = 10

        return jsonify({
            'status': True, 
            'message': 'Thông tin khuyến mãi được cập nhật thành công'
        }), 200

    except Exception as e:
        return jsonify({
            'status': False, 
            'message': 'Có lỗi xảy ra khi cập nhật khuyến mãi', 'error': str(e)
        }), 500


# 5. Delete a KhuyenMai by MaKhuyenMai
@adminKhuyenmai.route('/api/khuyen-mai/<string:ma_khuyen_mai>', methods=['DELETE'])
def delete_khuyen_mai(ma_khuyen_mai):
    try:
        km = KhuyenMai.query.filter_by(MaKhuyenMai=ma_khuyen_mai).first()
        if not km:
            return jsonify({
                'status': False, 
                'message': f"Không tìm thấy khuyến mãi có mã '{ma_khuyen_mai}'"
            }), 404

        # xóa khuyến mãi thì xóa luôn mấy cặp cb-km và hhk-km trong 2 table đó, chắc thế
        CB_KhuyenMai.query.filter_by(MaKM=ma_khuyen_mai).delete()
        HHK_KhuyenMai.query.filter_by(MaKM=ma_khuyen_mai).delete()

        db.session.delete(km)
        db.session.commit()

        return jsonify({
            'status': True, 
            'message': 'Khuyến mãi được xóa thành công'
        }), 200

    except Exception as e:
        return jsonify({
            'status': False, 
            'message': 'Có lỗi xảy ra', 
            'error': str(e)
        }), 500
    
@adminKhuyenmai.route('/api/khuyen-mai/apply', methods=['POST'])
def apply_promotion():
    try:
        data = request.get_json()
        promo_id = data.get('MaKhuyenMai')
        items = data.get('Items', [])
        apply_type = data.get('Type')

        if not promo_id or not items or not apply_type:
            return jsonify({'status': False, 'message': 'Thiếu thông tin bắt buộc'}), 400

        if apply_type == 'airlines':
            for item in items:
                association = HHK_KhuyenMai(MaHHK=item, MaKM=promo_id)
                db.session.add(association)
        elif apply_type == 'flights':
            for item in items:
                association = CB_KhuyenMai(MaCB=item, MaKM=promo_id)
                db.session.add(association)
        else:
            return jsonify({'status': False, 'message': 'Loại áp dụng không hợp lệ'}), 400

        db.session.commit()
        return jsonify({'status': True, 'message': 'Áp dụng thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': False, 'message': 'Có lỗi xảy ra', 'error': str(e)}), 500


# Lấy danh sách các hãng hàng không không lấy pagination
@adminKhuyenmai.route('/api/list-hang-hang-khong-promotion', methods=['GET'])
def get_all_hang_hang_khong():
    try:
        query = HangHangKhong.query
    
        data = [{
            'MaHHK': hhk.MaHHK,
            'TenHHK': hhk.TenHHK
        } for hhk in query]

        return jsonify({
            'status': True,
            'message': 'Lấy danh sách hãng hàng không thành công',
            'data': data
        }), 200

    except Exception as e:
        return jsonify({'status': False, 'message': 'Có lỗi xảy ra', 'error': str(e)}), 500
    
# Lấy danh sách các chuyến bay không lấy pagination
@adminKhuyenmai.route('/api/list-chuyen-bay-promotion', methods=['GET'])
def get_all_chuyen_bay():
    try:
        # Lọc chỉ những chuyến bay còn đang hoạt động (TrangThai == 0)
        query = ChuyenBay.query.filter_by(TrangThai=0)
        
        data = [{
            'MaChuyenBay': cb.MaChuyenBay,
            'SanBayDi': cb.MaSanBayDi,
            'SanBayDen': cb.MaSanBayDen,
            'ThoiGianDi': cb.ThoiGianDi.strftime('%Y-%m-%d %H:%M:%S'),
            'ThoiGianDen': cb.ThoiGianDen.strftime('%Y-%m-%d %H:%M:%S')
        } for cb in query.all()]

        return jsonify({
            'status': True,
            'message': 'Lấy danh sách chuyến bay thành công',
            'data': data
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra',
            'error': str(e)
        }), 500
