from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
import requests

khuyenmai = Blueprint('khuyenmai', __name__)

@khuyenmai.route('/khuyen-mai', methods=['GET'])
def get_khuyen_mai():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        ma_khuyen_mai = request.args.get('ma_khuyen_mai', '')
        ten_khuyen_mai = request.args.get('ten_khuyen_mai', '')
        loai_khuyen_mai = request.args.get('loai_khuyen_mai', '')
        sort_by = request.args.get('sort_by', 'MaKhuyenMai')
        order = request.args.get('order', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_khuyen_mai': ma_khuyen_mai,
            'ten_khuyen_mai': ten_khuyen_mai,
            'loai_khuyen_mai': loai_khuyen_mai,
            'sort_by': sort_by,
            'order': order
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}
        
        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/khuyen-mai",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/khuyenmai/khuyenmai.html',
            khuyen_mai=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_khuyen_mai': ma_khuyen_mai,
                'ten_khuyen_mai': ten_khuyen_mai,
                'loai_khuyen_mai': loai_khuyen_mai,
                'sort_by': sort_by,
                'order': order
            },
            api_url=current_app.config['API_URL']
        )

    except Exception as e:
        flash(str(e), 'danger')
        return render_template(
            'admin/khuyenmai/khuyenmai.html',
            khuyen_mai=[],
            pagination={'page': 1, 'pages': 1, 'total': 0, 'per_page': 10},
            filters={  # Trả về filters rỗng trong trường hợp lỗi
                'ma_khuyen_mai': '',
                'ten_khuyen_mai': '',
                'loai_khuyen_mai': '',
                'sort_by': 'ma_khuyen_mai',
                'order': 'asc'
            },
            api_url=current_app.config['API_URL']
        )