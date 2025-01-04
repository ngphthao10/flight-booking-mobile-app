from flask import Blueprint, render_template, current_app, redirect, url_for, request, session, jsonify
import requests

auth = Blueprint('auth', __name__)

import hashlib

def get_gravatar_url(email, size=200, default='identicon'):
    # Xử lý email
    email = email.strip().lower()
    # Mã hóa MD5
    hash_md5 = hashlib.md5(email.encode('utf-8')).hexdigest()
    # Ghép chuỗi để tạo link
    return f"https://www.gravatar.com/avatar/{hash_md5}?d={default}&s={size}"


@auth.route('/register/user')
def user_register():
    return render_template('user/register.html', api_url=current_app.config['API_URL'])

@auth.route('/home')
def homepage():
    return render_template('admin/admin_home.html', api_url=current_app.config['API_URL'])


@auth.route('/handle-login', methods=['POST'])
def handle_login():
    try:
        user_data = request.get_json()
        print(user_data)

        user_email = user_data['TenDangNhap']

        avatar_url = get_gravatar_url(user_email, size=200, default='identicon')
        session['user_info'] = {
            'MaND': user_data['MaND'],
            'TenDangNhap': user_data['TenDangNhap'],
            'NhomNguoiDung': user_data['NhomNguoiDung'],
            'avatar_url': avatar_url   
        }
        
        return jsonify({
            'status': True,
            'message': 'Đã lưu thông tin đăng nhập'
        })
        
    except Exception as e:
        print(f"Lỗi khi xử lý thông tin đăng nhập: {str(e)}")
        return jsonify({
            'status': False,
            'message': 'Có lỗi xảy ra'
        }), 500

@auth.route('/get-user-info')
def get_user_info():

    user_info = session.get('user_info')
    if user_info:
        return jsonify({
            'status': True,
            'data': user_info
        })
    return jsonify({
        'status': False,
        'message': 'Chưa đăng nhập'
    }), 401

@auth.route('/logout', methods=['GET'])
def logout_client():
    session.pop('user_info', None) 
    return jsonify({'status': True, 'message': 'Đăng xuất thành công'}), 200



