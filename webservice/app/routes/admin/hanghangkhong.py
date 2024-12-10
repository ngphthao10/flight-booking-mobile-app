from flask import Blueprint, request, jsonify
from app.models import HangHangKhong, QuocGia
from app import db
from sqlalchemy import or_

hanghangkhong = Blueprint('hanghangkhong', __name__)

@hanghangkhong.route('/api/hang-hang-khong', methods=['GET'])
def get_all_hang_hang_khong():
    try:
        # Lấy tham số phân trang
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Lấy các tham số lọc từ query string
        ma_hhk = request.args.get('ma_hhk', '')
        ten_hhk = request.args.get('ten_hhk', '')
        ma_qg = request.args.get('ma_qg', '')

        # Tạo query cơ bản
        query = HangHangKhong.query

        # Thêm các điều kiện lọc nếu có
        if ma_hhk:
            query = query.filter(HangHangKhong.MaHHK.ilike(f'%{ma_hhk}%'))
        if ten_hhk:
            query = query.filter(HangHangKhong.TenHHK.ilike(f'%{ten_hhk}%'))
        if ma_qg:
            query = query.filter(HangHangKhong.MaQG.ilike(f'%{ma_qg}%'))

        # Thêm sắp xếp (nếu cần)
        sort_by = request.args.get('sort_by', 'MaHHK')  # Mặc định sắp xếp theo MaHHK
        order = request.args.get('order', 'asc')  # Mặc định tăng dần
        
        if hasattr(HangHangKhong, sort_by):
            sort_column = getattr(HangHangKhong, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        # Thực hiện phân trang
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Chuẩn bị dữ liệu trả về
        data = [{
            'MaHHK': hhk.MaHHK,
            'TenHHK': hhk.TenHHK,
            'MaQG': hhk.quoc_gia.TenQuocGia
        } for hhk in pagination.items]

        return jsonify({
            'status': True,
            'message': 'Lấy danh sách hãng hàng không thành công',
            'data': data,
            'pagination': {
                'total': pagination.total,
                'pages': pagination.pages,
                'page': page,
                'per_page': per_page
            },
            'filters': {  # Trả về thông tin filter đang áp dụng
                'ma_hhk': ma_hhk,
                'ten_hhk': ten_hhk,
                'ma_qg': ma_qg,
                'sort_by': sort_by,
                'order': order
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi lấy danh sách hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/hang-hang-khong', methods=['POST'])
def create_hang_hang_khong():
    try:
        # Lấy dữ liệu từ request JSON
        data = request.get_json()
        
        # Kiểm tra dữ liệu bắt buộc
        required_fields = ['MaHHK', 'TenHHK', 'MaQG']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': False,
                'message': 'Thiếu thông tin bắt buộc'
            }), 400

        # Kiểm tra mã hãng hàng không đã tồn tại chưa
        existing_airline = HangHangKhong.query.filter_by(MaHHK=data['MaHHK']).first()
        if existing_airline:
            return jsonify({
                'status': False,
                'message': f"Mã hãng hàng không '{data['MaHHK']}' đã tồn tại"
            }), 400

        # Tạo đối tượng HangHangKhong mới
        new_airline = HangHangKhong(
            MaHHK=data['MaHHK'],
            TenHHK=data['TenHHK'],
            MaQG=data['MaQG']
        )

        # Thêm vào database
        db.session.add(new_airline)
        db.session.commit()

        # Trả về response thành công
        return jsonify({
            'status': True,
            'message': 'Thêm hãng hàng không thành công',
            'data': {
                'MaHHK': new_airline.MaHHK,
                'TenHHK': new_airline.TenHHK,
                'MaQG': new_airline.MaQG
            }
        }), 201

    except Exception as e:
        # Rollback trong trường hợp có lỗi
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi thêm hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/quoc-gia', methods=['GET'])
def get_quoc_gia():
    try:
        # Lấy danh sách quốc gia từ database
        quoc_gia = QuocGia.query.all()
        
        # Chuyển đổi thành list dict
        data = [{
            'MaQG': qg.MaQG,
            'TenQG': qg.TenQuocGia
        } for qg in quoc_gia]
        
        return jsonify({
            'status': True,
            'message': 'Lấy danh sách quốc gia thành công',
            'data': data
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi lấy danh sách quốc gia',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/hang-hang-khong/<string:ma_hhk>', methods=['PUT'])
def update_hang_hang_khong(ma_hhk):
    try:
        # Lấy dữ liệu từ request JSON
        data = request.get_json()
        
        # Tìm hãng hàng không cần cập nhật
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()
        
        # Kiểm tra hãng hàng không tồn tại
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
        # Kiểm tra và cập nhật các trường thông tin
        if 'TenHHK' in data:
            airline.TenHHK = data['TenHHK']
            
        if 'MaQG' in data:
            airline.MaQG = data['MaQG']
            
        # Lưu các thay đổi vào database
        db.session.commit()
        
        # Trả về response thành công
        return jsonify({
            'status': True,
            'message': 'Cập nhật hãng hàng không thành công',
            'data': {
                'MaHHK': airline.MaHHK,
                'TenHHK': airline.TenHHK,
                'MaQG': airline.MaQG
            }
        }), 200
        
    except Exception as e:
        # Rollback trong trường hợp có lỗi
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi cập nhật hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/hang-hang-khong/<string:ma_hhk>', methods=['GET'])
def get_hang_hang_khong_detail(ma_hhk):
    try:
        # Tìm hãng hàng không theo mã
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()
        
        # Kiểm tra hãng hàng không tồn tại
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
        # Trả về thông tin hãng hàng không
        return jsonify({
            'status': True,
            'message': 'Lấy thông tin hãng hàng không thành công',
            'data': {
                'MaHHK': airline.MaHHK,
                'TenHHK': airline.TenHHK,
                'MaQG': airline.MaQG
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi lấy thông tin hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/hang-hang-khong/<string:ma_hhk>', methods=['DELETE'])
def delete_hang_hang_khong(ma_hhk):
    try:
        # Tìm hãng hàng không cần xóa
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()
        
        # Kiểm tra hãng hàng không tồn tại
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
        # Thực hiện xóa
        db.session.delete(airline)
        db.session.commit()
        
        # Trả về response thành công
        return jsonify({
            'status': True,
            'message': 'Xóa hãng hàng không thành công',
            'data': {
                'MaHHK': airline.MaHHK,
                'TenHHK': airline.TenHHK,
                'MaQG': airline.MaQG
            }
        }), 200
        
    except Exception as e:
        # Rollback trong trường hợp có lỗi
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi xóa hãng hàng không',
            'error': str(e)
        }), 500