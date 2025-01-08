from functools import wraps
from flask import redirect, url_for, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            flash('Bạn cần đăng nhập để sử dụng tính năng này!', 'danger')
            return redirect(url_for('homepage.home'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect(url_for('homepage.home'))
            
        user_info = session['user_info']

        if not user_info.get('NhomNguoiDung'):
            flash('Bạn không có quyền truy cập trang này!', 'danger')
            return redirect(url_for('homepage.home'))
            
        if user_info['NhomNguoiDung']['MaNND'] != 1:
            flash('Bạn không có quyền truy cập trang này!', 'danger')
            return redirect(url_for('homepage.home'))
            
        return f(*args, **kwargs)
    return decorated_function