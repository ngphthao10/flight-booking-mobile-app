# routes/user_routes.py
from flask import Blueprint, jsonify, request
from app.models import NguoiDung, NhomNguoiDung  # Import trực tiếp classs
from app import db
from sqlalchemy import or_

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    try:
        # 1. Lấy các tham số từ query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        trang_thai = request.args.get('trang_thai', type=int)
        ma_nhom = request.args.get('ma_nhom', type=int)
        sort_by = request.args.get('sort_by', 'MaND')  # Sắp xếp mặc định theo MaND
        sort_order = request.args.get('sort_order', 'asc')  # Thứ tự sắp xếp (asc/desc)

        # 2. Tạo base query với join
        query = db.session.query(NguoiDung, NhomNguoiDung).join(
            NhomNguoiDung, NguoiDung.MaNND == NhomNguoiDung.MaNND
        )

        # 3. Thêm các điều kiện tìm kiếm
        if search:
            # Tìm kiếm trong cả tên đăng nhập và tên nhóm người dùng
            query = query.filter(or_(
                NguoiDung.TenDangNhap.like(f'%{search}%'),
                NhomNguoiDung.TenNhomNguoiDung.like(f'%{search}%')
            ))

        if trang_thai is not None:
            query = query.filter(NguoiDung.TrangThai == trang_thai)

        if ma_nhom:
            query = query.filter(NguoiDung.MaNND == ma_nhom)

        # 4. Thêm sắp xếp
        if hasattr(NguoiDung, sort_by):  # Kiểm tra tránh SQL injection
            sort_column = getattr(NguoiDung, sort_by)
            if sort_order == 'desc':
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

        # 5. Thực hiện phân trang
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        total_items = pagination.total
        total_pages = pagination.pages
        
        # 6. Format dữ liệu trả về
        users = []
        for user, group in pagination.items:
            users.append({
                'MaND': user.MaND,
                'TenDangNhap': user.TenDangNhap,
                'TrangThai': user.TrangThai,
                'NhomNguoiDung': {
                    'MaNND': group.MaNND,
                    'TenNhomNguoiDung': group.TenNhomNguoiDung
                }
            })

        # 7. Trả về kết quả với đầy đủ thông tin phân trang
        return jsonify({
            'data': users,
            'pagination': {
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
                'next_page': pagination.next_num if pagination.has_next else None,
                'prev_page': pagination.prev_num if pagination.has_prev else None
            },
            'filters': {
                'search': search,
                'trang_thai': trang_thai,
                'ma_nhom': ma_nhom,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Có lỗi xảy ra khi lấy danh sách người dùng'
        }), 400

# Ví dụ thêm route để lấy danh sách các option cho filter
@user_bp.route('/api/users/filter-options', methods=['GET'])
def get_filter_options():
    try:
        # Lấy danh sách nhóm người dùng
        groups = NhomNguoiDung.query.all()
        group_options = [{'MaNND': g.MaNND, 'TenNhomNguoiDung': g.TenNhomNguoiDung} for g in groups]

        # Danh sách trạng thái
        status_options = [
            {'value': 0, 'label': 'Không hoạt động'},
            {'value': 1, 'label': 'Đang hoạt động'}
        ]

        # Danh sách các trường có thể sắp xếp
        sort_options = [
            {'value': 'MaND', 'label': 'Mã người dùng'},
            {'value': 'TenDangNhap', 'label': 'Tên đăng nhập'},
            {'value': 'TrangThai', 'label': 'Trạng thái'}
        ]

        return jsonify({
            'groups': group_options,
            'statuses': status_options,
            'sort_fields': sort_options
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400