from flask import Blueprint, request, jsonify
from app.models import HangHangKhong, QuocGia
from app import db
from sqlalchemy import or_
from math import ceil
hanghangkhong = Blueprint('hanghangkhong', __name__)

@hanghangkhong.route('/api/hang-hang-khong', methods=['GET'])
def get_all_hang_hang_khong():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        ma_hhk = request.args.get('ma_hhk', '')
        ten_hhk = request.args.get('ten_hhk', '')
        ma_qg = request.args.get('ma_qg', '')

        query = HangHangKhong.query

        if ma_hhk:
            query = query.filter(HangHangKhong.MaHHK.ilike(f'%{ma_hhk}%'))
        if ten_hhk:
            query = query.filter(HangHangKhong.TenHHK.ilike(f'%{ten_hhk}%'))
        if ma_qg:
            query = query.filter(HangHangKhong.MaQG.ilike(f'%{ma_qg}%'))

        sort_by = request.args.get('sort_by', 'MaHHK') 
        order = request.args.get('order', 'asc')
        
        if hasattr(HangHangKhong, sort_by):
            sort_column = getattr(HangHangKhong, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

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
            'filters': { 
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
        data = request.get_json()
        perPage = 10
        required_fields = ['MaHHK', 'TenHHK', 'MaQG']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': False,
                'message': 'Thiếu thông tin bắt buộc'
            }), 400

        existing_airline = HangHangKhong.query.filter_by(MaHHK=data['MaHHK']).first()
        if existing_airline:
            return jsonify({
                'status': False,
                'message': f"Mã hãng hàng không '{data['MaHHK']}' đã tồn tại"
            }), 400

        existing_airline_name = HangHangKhong.query.filter_by(TenHHK=data['TenHHK']).first()
        if existing_airline_name:
            return jsonify({
                'status': False,
                'message': f"Tên hãng hàng không '{data['TenHHK']}' đã tồn tại"
            }), 400

        new_airline = HangHangKhong(
            MaHHK=data['MaHHK'],
            TenHHK=data['TenHHK'],
            MaQG=data['MaQG']
        )

        db.session.add(new_airline)
        db.session.commit()

        total = HangHangKhong.query.count()
        pages = ceil(total / perPage) 

        return jsonify({
            'status': True,
            'message': 'Thêm hãng hàng không thành công.',
            'pagination': {
                'total': total,
                'pages': pages
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi thêm hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/quoc-gia', methods=['GET'])
def get_quoc_gia():
    try:
        quoc_gia = QuocGia.query.all()
        
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
        data = request.get_json()
        
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()

        air1 = HangHangKhong.query.filter_by(TenHHK=data['TenHHK']).first()
        print(air1)
        if air1 and air1.MaHHK != data["MaHHK"]:
            return jsonify({
                'status': False,
                'message': f"Tên hãng hàng không '{data['TenHHK']}' đã tồn tại"
            }), 400
        
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
        if 'TenHHK' in data:
            airline.TenHHK = data['TenHHK']
            
        if 'MaQG' in data:
            airline.MaQG = data['MaQG']
        
        
            
        db.session.commit()
        
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
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi cập nhật hãng hàng không',
            'error': str(e)
        }), 500

@hanghangkhong.route('/api/hang-hang-khong/<string:ma_hhk>', methods=['GET'])
def get_hang_hang_khong_detail(ma_hhk):
    try:
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
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
        airline = HangHangKhong.query.filter_by(MaHHK=ma_hhk).first()
        
        if not airline:
            return jsonify({
                'status': False,
                'message': f"Không tìm thấy hãng hàng không với mã '{ma_hhk}'"
            }), 404
            
        db.session.delete(airline)
        db.session.commit()
        
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
        db.session.rollback()
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi xóa hãng hàng không',
            'error': str(e)
        }), 500