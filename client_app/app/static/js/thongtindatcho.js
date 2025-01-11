function displayBookingInfo(bookings) {
    const result = document.getElementById('bookingResult');
    const firstBooking = bookings[0];

    // Hiển thị thông tin chung
    document.getElementById('bookingId').textContent = firstBooking.MaDatCho;
    document.getElementById('bookingDate').textContent = formatDate(firstBooking.DatCho.NgayMua);
    document.getElementById('bookingStatus').textContent = firstBooking.DatCho.TrangThai;
    document.getElementById('contactName').textContent = `${firstBooking.NguoiLienHe.Ho} ${firstBooking.NguoiLienHe.Ten}`;
    document.getElementById('contactPhone').textContent = firstBooking.NguoiLienHe.SDT;
    document.getElementById('contactEmail').textContent = firstBooking.NguoiLienHe.Email;

    const flightsList = document.getElementById('flightsList');

    flightsList.innerHTML = bookings.map((booking, index) => {
        const goidv = booking.DatCho.GoiDichVu;

        return `
    <div class="card mb-3 border-0 shadow-sm">
        <div class="card-body">
            <!-- Airline Info -->
            <div class="row align-items-center mb-3">
                <div class="col-md-3">
                    <h5 class="fw-bold mb-1">${booking.ChuyenBay.HangBay.TenHHK}</h5>
                    <div class="text-muted small">${booking.MaChuyenBay}</div>
                </div>
                
                <!-- Flight Info -->
                <div class="col-md-9">
                    <div class="row">
                        <!-- Departure -->
                        <div class="col-4 text-center">
                            <div class="fw-bold fs-4 text-primary mb-1">
                                ${formatTime(booking.ChuyenBay.ThoiGianDi)}
                            </div>
                            <div class="fw-bold">${booking.ChuyenBay.SanBayDi.ThanhPho}</div>
                            <div class="text-muted small">
                                ${formatDate(booking.ChuyenBay.ThoiGianDi)}
                            </div>
                        </div>

                        <!-- Flight Duration -->
                        <div class="col-4 text-center">
                            <div class="border-top mt-3 position-relative">
                                <i class="bi bi-airplane-fill position-absolute top-50 start-50 translate-middle"></i>
                            </div>
                            <div class="mt-3 small">
                                ${booking.ChuyenBay.ThoiGianDi, booking.ChuyenBay.ThoiGianDen}
                            </div>
                        </div>

                        <!-- Arrival -->
                        <div class="col-4 text-center">
                            <div class="fw-bold fs-4 text-primary mb-1">
                                ${formatTime(booking.ChuyenBay.ThoiGianDen)}
                            </div>
                            <div class="fw-bold">${booking.ChuyenBay.SanBayDen.ThanhPho}</div>
                            <div class="text-muted small">
                                ${formatDate(booking.ChuyenBay.ThoiGianDen)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            ${goidv ? `
            <!-- Service Package -->
            <div class="mt-3 border-top pt-3">
                <button class="btn btn-outline-primary btn-sm" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#serviceDetails${index}">
                    <i class="bi bi-info-circle me-1"></i>
                    Gói dịch vụ: ${goidv.TenGoi}
                </button>

                <div class="collapse mt-3" id="serviceDetails${index}">
                    <div class="card bg-light">
                        <div class="card-body">
                            <p class="text-muted mb-3">${goidv.MoTa}</p>
                            <div class="row">
                                ${goidv.DichVu.map(dv => `
                                <div class="col-md-6 mb-3">
                                    <div class="d-flex">
                                        <i class="bi bi-check2 text-success me-2"></i>
                                        <div>
                                            <div class="fw-bold">${dv.TenDichVu}</div>
                                            <div class="small mb-1">${dv.MoTa}</div>
                                            <div class="small text-muted">
                                                Hạng ${dv.LoaiVeApDung} | 
                                                ${dv.TenDichVu.toLowerCase().includes('bảo hiểm')
                ? `${dv.ThamSo === 1 ? 'Có' : 'Không'}`
                : `${dv.ThamSo}${dv.TenDichVu.includes('Phí') || dv.TenDichVu.includes('Hoàn') ? '%' : ' kg'}`
            }
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ` : ''}
        </div>
    </div>
    `;
    }).join('');
    // Hiển thị danh sách hành khách
    const passengersList = document.getElementById('passengersList');
    passengersList.innerHTML = firstBooking.HanhKhach.map(passenger => `
            <div class="mb-3">
                <h6>${passenger.DanhXung} ${passenger.Ho} ${passenger.Ten}</h6>
                <p class="mb-1"><strong>CCCD:</strong> ${passenger.CCCD}</p>
                <p class="mb-1"><strong>Ngày sinh:</strong> ${formatDate(passenger.NgaySinh)}</p>
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
                <p><strong>Ngày thanh toán:</strong> ${formatDate(firstBooking.ThanhToan.NgayThanhToan)}</p>
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
