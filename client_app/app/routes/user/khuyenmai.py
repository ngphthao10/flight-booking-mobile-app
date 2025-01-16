from flask import Blueprint, render_template, jsonify, current_app
import requests
from app.decorators import login_required

promotion = Blueprint('promotion', __name__)

@promotion.route('/')
@login_required
def get_promotions_page():
    return render_template('user/thongtinkhuyenmai.html')

@promotion.route('/get-promotions')
@login_required
def get_promotions():
    try:
        response = requests.post(
            f"{current_app.config['API_URL']}/api/promotions",
            json={} 
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Lỗi khi lấy danh sách khuyến mãi: {str(e)}"
        }), 500