from flask import Blueprint, render_template, current_app, flash, request
import requests

nguoilienhe = Blueprint('nguoilienhe', __name__)

@nguoilienhe.route('/nguoi-lien-he', methods=['GET'])
def get_nguoi_lien_he():
    try:
        # Lấy tất cả các tham số query từ request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        ma_nlh = request.args.get('ma_nlh', '')
        ho_nlh = request.args.get('ho_nlh', '')
        ten_nlh = request.args.get('ten_nlh','')
        sdt = request.args.get('sdt', '')
        email = request.args.get('email', '')

        sort_by_nlh = request.args.get('sort_by_nlh', 'MaNLH')
        order_nlh = request.args.get('order_nlh', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_nlh': ma_nlh,
            'ho_nlh': ho_nlh,
            'ten_nlh': ten_nlh,
            'sdt': sdt,
            'email': email,
            'sort_by_nlh': sort_by_nlh,
            'order_nlh': order_nlh
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}

        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/nguoi-lien-he",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/nguoilienhe/nguoilienhe.html',
            nguoi_lien_he=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_nlh': ma_nlh,
                'ho_nlh': ho_nlh,
                'ten_nlh': ten_nlh,
                'sdt': sdt,
                'email': email,
                'sort_by_nlh': sort_by_nlh,
                'order_nlh': order_nlh
            },
            api_url=current_app.config['API_URL']
        )

    except Exception as e:
        flash(str(e), 'danger')
        return render_template(
            'admin/maybay/maybay.html',
            san_bay=[],
            pagination={'page': 1, 'pages': 1, 'total': 0, 'per_page': 10},
            filters={  # Trả về filters rỗng trong trường hợp lỗi
                'ma_nlh': '',
                'ho_nlh': '',
                'ten_nlh': '',
                'sdt': '',
                'email': '',
                'sort_by_nlh': sort_by_nlh,
                'order_nlh': order_nlh
            },
            api_url=current_app.config['API_URL']
        )
