from flask import Blueprint, render_template, current_app, flash, request
import requests

hanhkhach = Blueprint('hanhkhach', __name__)

@hanhkhach.route('/hanh-khach', methods=['GET'])
def get_hanh_khach():
    try:
        # Lấy tất cả các tham số query từ request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        ma_hanh_khach = request.args.get('ma_hanh_khach', '')
        ho_hk = request.args.get('ho_hk', '')
        ten_hk = request.args.get('ten_hk', '')
        danh_xung = request.args.get('danh_xung', '')
        cccd = request.args.get('cccd', '')
        ngay_sinh = request.args.get('ngay_sinh', '')
        quoc_tich = request.args.get('quoc_tich', '')
        loai_hk = request.args.get('loai_hk', '')

        sort_by_hanh_khach = request.args.get('sort_by_hanh_khach', 'MaHanhKhach')
        order_hanh_khach = request.args.get('order_hanh_khach', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_hanh_khach': ma_hanh_khach,
            'ho_hk': ho_hk,
            'ten_hk': ten_hk,
            'danh_xung': danh_xung,
            'cccd': cccd,
            'ngay_sinh': ngay_sinh,
            'quoc_tich': quoc_tich,
            'loai_hk': loai_hk,
            'sort_by_hanh_khach': sort_by_hanh_khach,
            'order_hanh_khach': order_hanh_khach
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}

        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/hanh-khach",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/hanhkhach/hanhkhach.html',
            hanh_khach=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_hanh_khach': ma_hanh_khach,
                'ho_hk': ho_hk,
                'ten_hk': ten_hk,
                'danh_xung': danh_xung,
                'cccd': cccd,
                'ngay_sinh': ngay_sinh,
                'quoc_tich': quoc_tich,
                'loai_hk': loai_hk,
                'sort_by_hanh_khach': sort_by_hanh_khach,
                'order_hanh_khach': order_hanh_khach
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
                'ma_hanh_khach': '',
                'ho_hk': '',
                'ten_hk': '',
                'danh_xung': '',
                'cccd': '',
                'ngay_sinh': '',
                'quoc_tich': '',
                'loai_hk': '',
                'sort_by_hanh_khach': sort_by_hanh_khach,
                'order_hanh_khach': order_hanh_khach
            },
            api_url=current_app.config['API_URL']
        )
