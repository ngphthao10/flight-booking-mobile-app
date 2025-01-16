from flask import Blueprint, request, jsonify
from app.models import MayBay, HangHangKhong
from app import db

maybay = Blueprint('maybay', __name__)

# API: Lấy danh sách máy bay theo hãng hàng không
@maybay.route('/api/hang-hang-khong/<string:ma_hhk>/may-bay', methods=['GET'])
def get_may_bay_by_hang_hang_khong(ma_hhk):
    try:
        hang_hang_khong = HangHangKhong.query.get(ma_hhk)

        if not hang_hang_khong:
            return jsonify({
                'status': False,
                'message': 'Không tìm thấy hãng hàng không'
            }), 404

        may_bay_list = MayBay.query.filter_by(MaHHK=ma_hhk).all()
        result = [{
            'MaMB': mb.MaMB,
            'TenMB': mb.TenMB,
            'MaHHK': mb.MaHHK
        } for mb in may_bay_list]

        return jsonify({
            'status': True,
            'message': 'Lấy danh sách máy bay thành công',
            'data': result
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi lấy danh sách máy bay',
            'error': str(e)
        }), 500

# API: Thêm máy bay
@maybay.route('/api/may-bay', methods=['POST'])
def add_may_bay():
    try:
        data = request.get_json()

        if not data or not data.get('MaMB') or not data.get('TenMB') or not data.get('MaHHK'):
            return jsonify({
                'status': False,
                'message': 'Vui lòng cung cấp đầy đủ thông tin (MaMB, TenMB, MaHHK)'
            }), 400

        hang_hang_khong = HangHangKhong.query.get(data['MaHHK'])

        if not hang_hang_khong:
            return jsonify({
                'status': False,
                'message': 'Hãng hàng không không tồn tại'
            }), 404

        new_may_bay = MayBay(
            MaMB=data['MaMB'],
            TenMB=data['TenMB'],
            MaHHK=data['MaHHK']
        )

        db.session.add(new_may_bay)
        db.session.commit()

        return jsonify({
            'status': True,
            'message': 'Thêm máy bay thành công',
            'data': {
                'MaMB': new_may_bay.MaMB,
                'TenMB': new_may_bay.TenMB,
                'MaHHK': new_may_bay.MaHHK
            }
        }), 201

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi thêm máy bay',
            'error': str(e)
        }), 500

@maybay.route('/api/may-bay/<string:ma_mb>', methods=['PUT'])
def update_may_bay(ma_mb):
    try:
        data = request.get_json()
        may_bay = MayBay.query.get(ma_mb)

        if not may_bay:
            return jsonify({
                'status': False,
                'message': 'Không tìm thấy máy bay'
            }), 404

        if 'TenMB' in data:
            may_bay.TenMB = data['TenMB']
        if 'MaHHK' in data:
            hang_hang_khong = HangHangKhong.query.get(data['MaHHK'])
            if not hang_hang_khong:
                return jsonify({
                    'status': False,
                    'message': 'Hãng hàng không không tồn tại'
                }), 404
            may_bay.MaHHK = data['MaHHK']

        db.session.commit()

        return jsonify({
            'status': True,
            'message': 'Cập nhật máy bay thành công',
            'data': {
                'MaMB': may_bay.MaMB,
                'TenMB': may_bay.TenMB,
                'MaHHK': may_bay.MaHHK
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi cập nhật máy bay',
            'error': str(e)
        }), 500

# API: Xóa máy bay
@maybay.route('/api/may-bay/<string:ma_mb>', methods=['DELETE'])
def delete_may_bay(ma_mb):
    try:
        may_bay = MayBay.query.get(ma_mb)

        if not may_bay:
            return jsonify({
                'status': False,
                'message': 'Không tìm thấy máy bay'
            }), 404

        db.session.delete(may_bay)
        db.session.commit()

        return jsonify({
            'status': True,
            'message': 'Xóa máy bay thành công'
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi xóa máy bay',
            'error': str(e)
        }), 500
