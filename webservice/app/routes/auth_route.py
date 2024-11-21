from flask import Blueprint, request, jsonify
from app import db
from app.models import NguoiDung, NhomNguoiDung
from werkzeug.security import check_password_hash
from flask_login import logout_user, login_required, login_user
from flask import session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'status': False,
                'message': 'Vui lòng nhập username và password'
            }), 400

        user = NguoiDung.query.filter_by(TenDangNhap=data['username']).first()

        if not user or not check_password_hash(user.MatKhau, data['password']):
            return jsonify({
                'status': False,
                'message': 'Username hoặc password không đúng'
            }), 401

        if user.TrangThai == 1:
            return jsonify({
                'status': False,
                'message': 'Tài khoản đã bị khóa'
            }), 401

        nhom = NhomNguoiDung.query.get(user.MaNND)
        login_user(user)  
        return jsonify({
            'status': True,
            'message': 'Đăng nhập thành công',
            'data': {
                'MaND': user.MaND,
                'TenDangNhap': user.TenDangNhap,
                'NhomNguoiDung': {
                    'MaNND': nhom.MaNND,
                    'TenNhomNguoiDung': nhom.TenNhomNguoiDung
                } if nhom else None
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra khi đăng nhập',
            'error': str(e)
        }), 500

@auth_bp.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()  
    return jsonify({'status': True, 'message': 'Đăng xuất thành công'}), 200
