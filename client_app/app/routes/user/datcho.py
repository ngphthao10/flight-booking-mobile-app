import os
from flask import Blueprint, render_template, session, current_app, jsonify, send_file
import requests
from app.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_LEFT
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

datcho = Blueprint('datcho', __name__)

@datcho.route('/passenger-info', methods=['GET', 'POST'])
def passenger_info():
    return render_template('user/thongtindatcho.html', api_url=current_app.config['API_URL'])

@datcho.route('/thanhtoan', methods=['GET', 'POST'])
def thanhtoan():
    user_info = session.get('user_info') 
    print(user_info)
    return render_template('user/thanhtoan.html', api_url=current_app.config['API_URL'], user_info=user_info)

@datcho.route('/booking-success', methods=['GET'])
def booking_success():
    return render_template('user/thanhToanThanhCong.html')

@datcho.route('/booking-info', methods=['GET'])
@login_required
def booking_info():
    return render_template('user/danhsachdatcho.html', api_url=current_app.config['API_URL'])

@datcho.route('/booking-detailed', methods=['GET'])
def booking_detailed():
    return render_template('user/ketquatracuu.html', api_url=current_app.config['API_URL'])

# @datcho.route('/generate_eticket/<int:madatcho>', methods=['GET'])
# def generate_eticket(madatcho):
#     try:
#         # Gọi API để lấy thông tin đặt chỗ
#         try:
#             response = requests.get(f"{current_app.config['API_URL']}/api/get_booking_detailed/{madatcho}")
#             if response.status_code != 200:
#                 return jsonify({
#                     "status": "error",
#                     "message": "Không tìm thấy thông tin đặt chỗ"
#                 }), response.status_code

#             booking_data = response.json().get('data', [])[0]

#         except requests.RequestException as e:
#             current_app.logger.error(f"Error fetching booking details: {str(e)}")
#             return jsonify({
#                 "status": "error",
#                 "message": "Lỗi kết nối server khi lấy thông tin đặt chỗ"
#             }), 500

#         # Tạo tên file
#         filename = f"e-ticket_{madatcho}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

#         # Tạo PDF
#         create_e_ticket(booking_data, output_path)

#         # Trả về file
#         return send_file(
#             output_path,
#             as_attachment=True,
#             download_name=filename,
#             mimetype='application/pdf'
#         )

#     except Exception as e:
#         current_app.logger.error(f"Error generating e-ticket: {str(e)}")
#         return jsonify({
#             "status": "error",
#             "message": f"Lỗi khi tạo vé điện tử: {str(e)}"
#         }), 500

@datcho.route('/generate_eticket/<int:madatcho>', methods=['GET'])
def generate_eticket(madatcho):
    try:
        # Gọi API để lấy thông tin đặt chỗ
        try:
            response = requests.get(f"{current_app.config['API_URL']}/api/get_booking_detailed/{madatcho}")
            if response.status_code != 200:
                return jsonify({
                    "status": "error",
                    "message": "Không tìm thấy thông tin đặt chỗ"
                }), response.status_code

            booking_data = response.json()

        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching booking details: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Lỗi kết nối server khi lấy thông tin đặt chỗ"
            }), 500

        # Tạo tên file PDF
        filename = f"e-ticket_{madatcho}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Tạo PDF
        success, message = create_e_ticket(booking_data, output_path)
        
        if not success:
            return jsonify({
                "status": "error",
                "message": f"Lỗi khi tạo PDF: {message}"
            }), 500

        
        # Gửi file về client
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Lỗi không xác định: {str(e)}"
        }), 500


def create_e_ticket(booking_data, output_path):
    """
    Tạo vé máy bay (hỗ trợ cả vé một chiều và khứ hồi)
    Args:
        booking_data: dict chứa thông tin đặt vé (có thể là một chiều hoặc khứ hồi)
        output_path: đường dẫn file PDF output
    """
    try:
        # Đăng ký font
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        font_dir = os.path.join(project_root, 'fonts')
        
        pdfmetrics.registerFont(TTFont('DejaVuSerif', os.path.join(font_dir, 'DejaVuSerif.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', os.path.join(font_dir, 'DejaVuSerif-Bold.ttf')))
        
        # Tạo document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        # Khởi tạo styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            fontName='DejaVuSerif-Bold',
            fontSize=14,
            spaceAfter=30,
            alignment=1,
            encoding='utf-8'
        ))

        styles.add(ParagraphStyle(
            name='NormalVN',
            fontName='DejaVuSerif',
            fontSize=10,
            leading=12,
            encoding='utf-8'
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Normal'],
            fontName='DejaVuSerif-Bold',
            fontSize=12,
            spaceAfter=10,
            spaceBefore=10,
            leading=16,
            alignment=TA_LEFT,
            encoding='utf-8'
        ))
        elements = []

        bookings = booking_data.get('data', [])
        if not isinstance(bookings, list):
            bookings = [bookings]  

        for idx, booking in enumerate(bookings):
    
            trip_type = ""
            if len(bookings) > 1:
                trip_type = "CHIỀU ĐI" if idx == 0 else "CHIỀU VỀ"
            
            title = f"VÉ ĐIỆN TỬ - {booking['ChuyenBay']['HangBay']['TenHHK']}"
            if trip_type:
                title += f" ({trip_type})"
            elements.append(Paragraph(title, styles['CustomTitle']))
            
            # Thông tin chuyến bay
            flight_info = [
                ['THÔNG TIN CHUYẾN BAY', ''],
                ['Chuyến bay:', str(booking['MaChuyenBay'])],
                ['Từ:', f"{booking['ChuyenBay']['SanBayDi']['TenSanBay']} ({booking['ChuyenBay']['SanBayDi']['ThanhPho']})"],
                ['Đến:', f"{booking['ChuyenBay']['SanBayDen']['TenSanBay']} ({booking['ChuyenBay']['SanBayDen']['ThanhPho']})"],
                ['Ngày giờ khởi hành:', datetime.strptime(booking['ChuyenBay']['ThoiGianDi'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')],
                ['Ngày giờ đến:', datetime.strptime(booking['ChuyenBay']['ThoiGianDen'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')],
                ['Máy bay:', f"{booking['ChuyenBay']['MayBay']['TenMayBay']} ({booking['ChuyenBay']['MayBay']['LoaiMayBay']})"],
                ['Hạng vé:', "Business" if booking['DatCho']['SoLuongGhe']['Business'] > 0 else "Economy"]
            ]
            
            flight_table = Table(flight_info, colWidths=[4*cm, 12*cm])
            flight_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('SPAN', (0, 0), (1, 0)),
            ]))
            elements.append(flight_table)
            elements.append(Spacer(1, 20))

            # Thông tin gói dịch vụ
            if booking['DatCho'].get('GoiDichVu'):
                goi_dv = booking['DatCho']['GoiDichVu']
                service_info = [
                    ['THÔNG TIN GÓI DỊCH VỤ ĐI KÈM', ''],
                    ['Tên gói:', goi_dv['TenGoi']],
                    ['Mô tả:', goi_dv['MoTa']]
                ]
                
                for dv in goi_dv['DichVu']:
                    gia_tri = dv['ThamSo']
                    if 'bảo hiểm' in dv['TenDichVu'].lower():
                        gia_tri = "Có" if dv['ThamSo'] == 1 else "Không"
                    else:
                        gia_tri = f"{dv['ThamSo']}{' kg' if 'hành lý' in dv['TenDichVu'].lower() else '%'}"
                        
                    service_info.append([
                        f"{dv['TenDichVu']}:", 
                        f"{gia_tri}"
                    ])
                
                service_table = Table(service_info, colWidths=[4*cm, 12*cm])
                service_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
                    ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                    ('SPAN', (0, 0), (1, 0)),
                ]))
                elements.append(service_table)
                elements.append(Spacer(1, 20))

                # Thông tin hành khách
                elements.append(Paragraph("DANH SÁCH HÀNH KHÁCH", styles['CustomTitle']))

                for index, passenger in enumerate(booking['HanhKhach'], 1):
                    # Header cho mỗi hành khách
                    elements.append(Paragraph(f"Hành khách {index}: {passenger['LoaiHK']}", styles['CustomHeading2']))
                    
                    passenger_info = [
                        ['THÔNG TIN HÀNH KHÁCH', ''],
                        ['Danh xưng:', passenger['DanhXung']],
                        ['Họ tên:', f"{passenger['Ho']} {passenger['Ten']}"],
                        ['CCCD:', passenger['CCCD']],
                        ['Ngày sinh:', datetime.strptime(passenger['NgaySinh'], '%Y-%m-%d').strftime('%d/%m/%Y')],
                        ['Quốc tịch:', passenger['QuocTich']],
                        ['Hành lý:', f"{passenger['HanhLy']['SoKy']}kg - {passenger['HanhLy']['MoTa']}" if passenger.get('HanhLy') else 'Không có']
                    ]
                    
                    passenger_table = Table(passenger_info, colWidths=[4*cm, 12*cm])
                    passenger_table.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
                        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('FONTSIZE', (0, 1), (-1, -1), 10),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('BOX', (0, 0), (-1, -1), 2, colors.black),
                        ('SPAN', (0, 0), (1, 0)),
                    ]))
                    elements.append(passenger_table)
                    elements.append(Spacer(1, 20))
 
            if idx < len(bookings) - 1:
                elements.append(PageBreak())

        if len(bookings) >= 1 and bookings[0].get('ThanhToan'):
            thanh_toan = bookings[0]['ThanhToan']
            he_so_gia = booking['DatCho']['GoiDichVu']['HeSoGia']
            elements.append(PageBreak())  
            
            elements.append(Paragraph("THÔNG TIN THANH TOÁN", styles['CustomTitle']))

            basic_info = [
                ['Mã đặt chỗ:', str(bookings[0]['MaDatCho'])],
                ['Ngày thanh toán:', datetime.strptime(thanh_toan['NgayThanhToan'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')],
                ['Phương thức:', thanh_toan['PhuongThuc']],
            ]
            
            basic_table = Table(basic_info, colWidths=[4*cm, 12*cm])
            basic_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(basic_table)
            elements.append(Spacer(1, 20))

            payment_details = [
                ['CHI TIẾT THANH TOÁN', '', ''],
                ['Mô tả', 'Số lượng', 'Thành tiền'],
            ]

            # Thêm vé Business
            booking = bookings[0]
            if booking['DatCho']['SoLuongGhe']['Business'] > 0:
                so_luong = booking['DatCho']['SoLuongGhe']['Business']
                gia_ve = booking['ChuyenBay']['GiaVe']['Business']
                payment_details.append([
                    f"Vé máy bay hạng Business\n{booking['ChuyenBay']['SanBayDi']['ThanhPho']} → {booking['ChuyenBay']['SanBayDen']['ThanhPho']}",
                    str(so_luong),
                    f"{(gia_ve * he_so_gia * so_luong):,.0f} VNĐ"
                ])

            # Thêm vé Economy
            if booking['DatCho']['SoLuongGhe']['Economy'] > 0:
                so_luong = booking['DatCho']['SoLuongGhe']['Economy']
                gia_ve = booking['ChuyenBay']['GiaVe']['Economy']
                payment_details.append([
                    f"Vé máy bay hạng Economy\n{booking['ChuyenBay']['SanBayDi']['ThanhPho']} → {booking['ChuyenBay']['SanBayDen']['ThanhPho']}",
                    str(so_luong),
                    f"{(gia_ve * he_so_gia * so_luong):,.0f} VNĐ"
                ])

            # Thêm hành lý
            for passenger in booking['HanhKhach']:
                if passenger.get('HanhLy'):
                    payment_details.append([
                        f"Hành lý ký gửi {passenger['HanhLy']['SoKy']}kg\n{passenger['Ho']} {passenger['Ten']} - {passenger['CCCD']}",
                        "1",
                        f"{passenger['HanhLy']['Gia']:,.0f} VNĐ"
                    ])

            # Thêm tổng cộng
            payment_details.extend([
                ['Tổng tiền', '', f"{(thanh_toan['SoTien'] + thanh_toan['TienGiam']):,.0f} VNĐ"],
                ['Giảm giá', '', f"-{thanh_toan['TienGiam']:,.0f} VNĐ"],
                ['Thuế', '', f"{thanh_toan['Thue']:,.0f} VNĐ"],
                ['TỔNG THANH TOÁN', '', f"{(thanh_toan['SoTien'] + thanh_toan['Thue']):,.0f} VNĐ"]
            ])

            detail_table = Table(payment_details, colWidths=[8*cm, 3*cm, 5*cm])
            detail_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif-Bold'),
                ('FONTNAME', (-1, -1), (-1, -1), 'DejaVuSerif-Bold'), 
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),  
                ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'), 
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),  
                ('SPAN', (0, 0), (2, 0)),  
                ('LINEBELOW', (0, -2), (-1, -2), 2, colors.black), 
            ]))
            elements.append(detail_table)
            
        doc.build(elements)
        return True, "PDF created successfully"

    except Exception as e:
        return False, str(e)