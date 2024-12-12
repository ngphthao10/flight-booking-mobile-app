from flask import Blueprint, render_template, current_app, flash, request
import requests

sanbay = Blueprint('sanbay', __name__)

@sanbay.route('/san-bay', methods=['GET'])
def get_san_bay():
    try:
        # Lấy tất cả các tham số query từ request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        ma_san_bay = request.args.get('ma_san_bay', '')
        ten_san_bay = request.args.get('ten_san_bay', '')
        thanh_pho = request.args.get('thanh_pho', '')
        ma_qg_san_bay = request.args.get('ma_qg_san_bay', '')
        sort_by_san_bay = request.args.get('sort_by_san_bay', 'MaSanBay')
        order_san_bay = request.args.get('order_san_bay', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_san_bay': ma_san_bay,
            'ten_san_bay': ten_san_bay,
            'thanh_pho': thanh_pho,
            'ma_qg_san_bay': ma_qg_san_bay,
            'sort_by_san_bay': sort_by_san_bay,
            'order_san_bay': order_san_bay
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}

        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/san-bay",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/sanbay/sanbay.html',
            san_bay=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_san_bay': ma_san_bay,
                'ten_san_bay': ten_san_bay,
                'thanh_pho': thanh_pho,
                'ma_qg_san_bay': ma_qg_san_bay,
                'sort_by_san_bay': sort_by_san_bay,
                'order_san_bay': order_san_bay
            },
            api_url=current_app.config['API_URL']
        )

    except Exception as e:
        flash(str(e), 'danger')
        return render_template(
            'admin/sanbay/sanbay.html',
            san_bay=[],
            pagination={'page': 1, 'pages': 1, 'total': 0, 'per_page': 10},
            filters={  # Trả về filters rỗng trong trường hợp lỗi
                'ma_san_bay': '',
                'ten_san_bay': '',
                'thanh_pho': '',
                'ma_qg_san_bay': '',
                'sort_by_san_bay': 'MaSanBay',
                'order_san_bay': 'asc'
            },
            api_url=current_app.config['API_URL']
        )
