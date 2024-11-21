from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/')
def index():
    # Thêm logic kiểm tra đăng nhập nếu cần
    return render_template('index.html')