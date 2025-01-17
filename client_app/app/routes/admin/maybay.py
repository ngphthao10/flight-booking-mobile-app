from flask import Blueprint, render_template, current_app, flash, request
import requests

maybay = Blueprint('maybay', __name__)

@maybay.route('/may-bay', methods=['GET'])
def get_may_bay():
    try:
        # Lấy tất cả các tham số query từ request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        ma_may_bay = request.args.get('ma_may_bay', '')
        ten_may_bay = request.args.get('ten_may_bay', '')
        ma_hhk_may_bay = request.args.get('ma_hhk_may_bay','')
        # so_cho_ngoi_bus = request.args.get('so_cho_ngoi_bus','')
        # so_cho_ngoi_eco = request.args.get('so_cho_ngoi_eco','')
        loai_mb = request.args.get('loai_mb','')
        if loai_mb == 'None':
            loai_mb = None
        sort_by_may_bay = request.args.get('sort_by_may_bay', 'MaMayBay')
        order_may_bay = request.args.get('order_may_bay', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_may_bay': ma_may_bay,
            'ten_may_bay': ten_may_bay,
            'ma_hhk_may_bay': ma_hhk_may_bay,
            # 'so_cho_ngoi_bus': so_cho_ngoi_bus,
            # 'so_cho_ngoi_eco': so_cho_ngoi_eco,
            'loai_mb': loai_mb,
            'sort_by_may_bay': sort_by_may_bay,
            'order_may_bay': order_may_bay
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}

        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/may-bay",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/maybay/maybay.html',
            may_bay=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_may_bay': ma_may_bay,
                'ten_may_bay': ten_may_bay,
                'ma_hhk_may_bay': ma_hhk_may_bay,
                # 'so_cho_ngoi_bus': so_cho_ngoi_bus,
                # 'so_cho_ngoi_eco': so_cho_ngoi_eco,
                'loai_mb': loai_mb,
                'sort_by_may_bay': sort_by_may_bay,
                'order_may_bay': order_may_bay
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
                'ma_may_bay': '',
                'ten_may_bay': '',
                'ma_hhk_may_bay': '',
                'loai_mb': '',
                'sort_by_may_bay': sort_by_may_bay,
                'order_may_bay': order_may_bay
            },
            api_url=current_app.config['API_URL']
        )
