from flask_mail import Message
from app import mail 

def send_booking_confirmation_email(to_email, booking_info):

    subject = "XÁC NHẬN ĐẶT CHỖ THÀNH CÔNG"

    # Nội dung email (plaintext)
    body = f"""
    Chào bạn,

    Cảm ơn bạn đã đặt chỗ. Dưới đây là chi tiết đặt chỗ của bạn:

    Mã đặt chỗ: {booking_info.get('ma_dat_cho_goc')}
    Họ tên người liên hệ: {booking_info.get('ho_ten_lien_he')}
    Email: {booking_info.get('email_lien_he')}
    Thời gian đặt: {booking_info.get('ngay_mua')}
    Tổng tiền: {booking_info.get('tong_tien')} VND
    Giảm giá: {booking_info.get('tien_giam')} VND
    Phương thức thanh toán: {booking_info.get('phuong_thuc')}

    Trạng Thái: Đã thanh toán

    Nếu bạn muốn xem thông tin chi tiết về chuyến bay đã đặt. Vui lòng thực hiện tra cứu trên website của chúng tôi!
    Chúc bạn một ngày tốt lành!
    
    Trân trọng,
    FlightBooking team.
    """

    msg = Message(
        subject=subject,
        recipients=[to_email],
        body=body
    )

    mail.send(msg)

def send_booking_cancellation_email(to_email, cancellation_info):

    subject = "XÁC NHẬN HỦY ĐẶT CHỖ THÀNH CÔNG"

    # Tạo danh sách thông tin các vé bị hủy
    cancelled_bookings = []
    for booking in cancellation_info['ds_huy']:
        booking_detail = f"""
        Mã đặt chỗ: {booking['ma_dat_cho']}
        Mã chuyến bay: {booking['ma_chuyen_bay']}
        Tỷ lệ hoàn tiền: {booking['ty_le_hoan']}
        Số tiền hoàn: {booking['so_tien_hoan']} VND
        """
        cancelled_bookings.append(booking_detail)

    # Nội dung email
    body = f"""
    Chào bạn,

    Yêu cầu hủy đặt chỗ của bạn đã được xử lý thành công. Dưới đây là chi tiết các đặt chỗ đã hủy:

    {"".join(cancelled_bookings)}
    Thời gian duyệt hủy: {cancellation_info['ngay_duyet']}

    Nếu có số tiền hoàn, chúng tôi sẽ hoàn tiền về tài khoản/phương thức thanh toán ban đầu của bạn trong vòng 7-14 ngày làm việc.
    
    Nếu bạn cần hỗ trợ thêm, vui lòng liên hệ với chúng tôi qua website hoặc hotline.
    
    Trân trọng,
    FlightBooking team.
    """

    msg = Message(
        subject=subject,
        recipients=[to_email],
        body=body
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Lỗi gửi email: {str(e)}")
        return False

def send_booking_cancellation_rejected_email(to_email, reject_info):
    subject = "THÔNG BÁO TỪ CHỐI YÊU CẦU HỦY ĐẶT CHỖ"

    # Nội dung email
    body = f"""
    Chào anh/chị {reject_info.get('ho_ten')},

    Yêu cầu hủy đặt chỗ của anh/chị đã bị từ chối vì lý do sau:

    Mã đặt chỗ: {reject_info.get('ma_dat_cho')}
    Chuyến bay: {reject_info['thong_tin_chuyen_bay']['diem_di']} → {reject_info['thong_tin_chuyen_bay']['diem_den']}
    Thời gian khởi hành: {reject_info['thong_tin_chuyen_bay']['thoi_gian_di']}
    Lý do từ chối: {reject_info.get('ly_do')}
    Thời gian xử lý: {reject_info.get('thoi_gian')}

    Nếu anh/chị cần hỗ trợ thêm, vui lòng liên hệ với chúng tôi qua website.
    
    Trân trọng,
    FlightBooking team.
    """

    msg = Message(
        subject=subject,
        recipients=[to_email],
        body=body
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Lỗi gửi email: {str(e)}")
        return False