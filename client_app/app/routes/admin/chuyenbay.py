from flask import Blueprint, render_template, session, current_app
from app.decorators import admin_required
from datetime import datetime

chuyenbay = Blueprint('chuyenbay', __name__)

@chuyenbay.route('/', methods=['GET'])
@admin_required
def get_flights():
    return render_template('admin/chuyenbay/chuyenbay.html', api_url=current_app.config['API_URL'], now=datetime.now())

@chuyenbay.route('/flights/add', methods=['GET'])
def add_flight():
    return render_template('admin/chuyenbay/themchuyenbay.html', api_url=current_app.config['API_URL'], now=datetime.now())

@chuyenbay.route('/flights/edit/<string:ma_chuyen_bay>')
def edit_flight(ma_chuyen_bay):
    return render_template('admin/chuyenbay/suachuyenbay.html', api_url=current_app.config['API_URL'], now=datetime.now())