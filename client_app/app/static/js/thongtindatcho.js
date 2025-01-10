function displayBookingInfo(bookings) {
    const result = document.getElementById('bookingResult');
    const firstBooking = bookings[0];

    // Hiển thị thông tin chung
    document.getElementById('bookingId').textContent = firstBooking.MaDatCho;
    document.getElementById('bookingDate').textContent = formatDateTime(firstBooking.DatCho.NgayMua);
    document.getElementById('bookingStatus').textContent = firstBooking.DatCho.TrangThai;
    document.getElementById('contactName').textContent = `${firstBooking.NguoiLienHe.Ho} ${firstBooking.NguoiLienHe.Ten}`;
    document.getElementById('contactPhone').textContent = firstBooking.NguoiLienHe.SDT;
    document.getElementById('contactEmail').textContent = firstBooking.NguoiLienHe.Email;

    // Hiển thị danh sách chuyến bay
    const flightsList = document.getElementById('flightsList');
    flightsList.innerHTML = bookings.map(booking => `
            <div class="card flight-card">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4">
                            <h6>${booking.ChuyenBay.HangBay.TenHHK}</h6>
                            <small class="text-muted">${booking.MaChuyenBay}</small>
                        </div>
                        <div class="col-md-8">
                            <div class="row">
                                <div class="col-md-5 text-center">
                                    <h6>${booking.ChuyenBay.SanBayDi.ThanhPho}</h6>
                                    <p class="mb-0">${formatDateTime(booking.ChuyenBay.ThoiGianDi)}</p>
                                    <small>${booking.ChuyenBay.SanBayDi.TenSanBay}</small>
                                </div>
                                <div class="col-md-2 text-center">
                                    <i class="fas fa-plane"></i>
                                </div>
                                <div class="col-md-5 text-center">
                                    <h6>${booking.ChuyenBay.SanBayDen.ThanhPho}</h6>
                                    <p class="mb-0">${formatDateTime(booking.ChuyenBay.ThoiGianDen)}</p>
                                    <small>${booking.ChuyenBay.SanBayDen.TenSanBay}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

    // Hiển thị danh sách hành khách
    const passengersList = document.getElementById('passengersList');
    passengersList.innerHTML = firstBooking.HanhKhach.map(passenger => `
            <div class="mb-3">
                <h6>${passenger.DanhXung} ${passenger.Ho} ${passenger.Ten}</h6>
                <p class="mb-1"><strong>CCCD:</strong> ${passenger.CCCD}</p>
                <p class="mb-1"><strong>Ngày sinh:</strong> ${passenger.NgaySinh}</p>
                <p class="mb-1"><strong>Loại:</strong> ${passenger.LoaiHK}</p>
                ${passenger.HanhLy ? `
                    <p class="mb-1"><strong>Hành lý:</strong> ${passenger.HanhLy.SoKy}kg - ${formatPrice(passenger.HanhLy.Gia)}</p>
                ` : ''}
            </div>
        `).join('');

    // Hiển thị thông tin thanh toán
    const paymentInfo = document.getElementById('paymentInfo');
    if (firstBooking.ThanhToan) {
        paymentInfo.innerHTML = `
                <p><strong>Ngày thanh toán:</strong> ${formatDateTime(firstBooking.ThanhToan.NgayThanhToan)}</p>
                <p><strong>Phương thức:</strong> ${firstBooking.ThanhToan.PhuongThuc}</p>
                <p><strong>Số tiền:</strong> ${formatPrice(firstBooking.ThanhToan.SoTien)}</p>
                <p><strong>Tiền giảm:</strong> ${formatPrice(firstBooking.ThanhToan.TienGiam)}</p>
            `;
    } else {
        paymentInfo.innerHTML = '<p>Chưa thanh toán</p>';
    }

    try {
        const printTicketBtn = document.getElementById('printTicketBtn');

        if (firstBooking.ThanhToan && firstBooking.DatCho.TrangThai !== 'Đã hủy') {
            printTicketBtn.style.display = 'block';
        } else {
            printTicketBtn.style.display = 'none';
        }
    } catch { }
    // Hiển thị kết quả
    result.classList.remove('d-none');

}

async function printTicket() {
    const bookingId = document.getElementById('bookingId').textContent;
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');

    try {
        loading.classList.remove('d-none');
        error.classList.add('d-none');

        const response = await fetch(`generate_eticket/${bookingId}`);

        if (!response.ok) {
            if (response.headers.get('content-type')?.includes('application/json')) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Không thể tạo vé điện tử');
            }
            throw new Error('Không thể tạo vé điện tử');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `e-ticket_${bookingId}.pdf`;
        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (err) {
        error.textContent = err.message;
        error.classList.remove('d-none');
    } finally {
        loading.classList.add('d-none');
    }
}

function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

function formatDateTime(dateStr) {
    return new Date(dateStr).toLocaleString('vi-VN');
}