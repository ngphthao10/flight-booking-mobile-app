# email_utils.py
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
