function exportToExcel(data, sheetName, reportTitle, reportSubtitle = '') {
    // Tạo workbook mới
    const wb = XLSX.utils.book_new();

    // Chuẩn bị dữ liệu cho header của báo cáo
    const headerRows = [
        [reportTitle],
        ['Ngày xuất: ' + getCurrentDateTime()],
        reportSubtitle ? [reportSubtitle] : [],
        [], // Dòng trống
        Object.keys(data[0]) // Headers của dữ liệu
    ];

    // Chuyển đổi dữ liệu thành mảng các hàng
    const rows = data.map(item => Object.values(item));

    // Gộp header và dữ liệu
    const allRows = [...headerRows, ...rows];

    // Tạo worksheet
    const ws = XLSX.utils.aoa_to_sheet(allRows);

    // Style cho tiêu đề
    ws['!merges'] = [
        { s: { r: 0, c: 0 }, e: { r: 0, c: 5 } }, // Merge các ô cho tiêu đề chính
        { s: { r: 1, c: 0 }, e: { r: 1, c: 5 } }, // Merge cho ngày xuất
        { s: { r: 2, c: 0 }, e: { r: 2, c: 5 } }  // Merge cho người xuất
    ];

    // Set column widths
    ws['!cols'] = Array(10).fill({ wch: 15 }); // Default width 15 cho tất cả cột

    // Thêm worksheet vào workbook
    XLSX.utils.book_append_sheet(wb, ws, sheetName);

    // Xuất file
    XLSX.writeFile(wb, `${sheetName}_${new Date().toISOString().split('T')[0]}.xlsx`);
}

// Hàm xuất báo cáo thị phần
async function exportMarketShare() {
    try {
        const response = await fetch('/report/dashboard/market-share');
        const result = await response.json();
        if (result.status === 'success') {
            const exportData = result.data.map(item => ({
                'Hãng hàng không': item.airline_name,
                'Mã hãng': item.airline_code,
                'Số đơn đặt': item.total_bookings,
                'Thị phần (%)': item.market_share.toFixed(2)
            }));

            exportToExcel(
                exportData,
                'ThiPhanHangHangKhong',
                'BÁO CÁO THỐNG KÊ THỊ PHẦN HÃNG HÀNG KHÔNG'
            );
        }
    } catch (error) {
        console.error('Error exporting market share:', error);
    }
}

// Hàm xuất báo cáo doanh thu theo tuần
async function exportMonthlySales() {
    try {
        const month = document.getElementById('monthSelect').value;
        const year = document.getElementById('yearSelect').value;
        const response = await fetch(`/report/dashboard/monthly_weekly_revenue?month=${month}&year=${year}`);
        const result = await response.json();
        if (result.status === 'success') {
            const exportData = result.data.map(item => ({
                'Tuần': item.week_number,
                'Số đặt chỗ': item.total_orders,
                'Doanh thu (VNĐ)': formatCurrency(item.total_revenue).replace('₫', '').trim()
            }));

            exportToExcel(
                exportData,
                'DoanhThuTheoTuan',
                'BÁO CÁO DOANH THU THEO TUẦN',
                `Tháng ${month} năm ${year}`
            );
        }
    } catch (error) {
        console.error('Error exporting monthly sales:', error);
    }
}

// Hàm xuất báo cáo đặt chỗ
async function exportBookingStats() {
    try {
        const response = await fetch('/report/dashboard/booking-stats');
        const result = await response.json();
        if (result.status === 'success') {
            const exportData = result.data.map(item => ({
                'Trạng thái': item.status,
                'Số đặt chỗ': item.total_bookings,
                'Số hành khách': item.total_passengers
            }));

            exportToExcel(
                exportData,
                'ThongKeDatCho',
                'BÁO CÁO THỐNG KÊ ĐẶT CHỖ THEO TRẠNG THÁI'
            );
        }
    } catch (error) {
        console.error('Error exporting booking stats:', error);
    }
}

// Hàm xuất báo cáo thống kê hành khách
async function exportPassengerStats() {
    try {
        const response = await fetch('/report/dashboard/passenger-stats');
        const result = await response.json();
        if (result.status === 'success') {
            const exportData = result.data.map(item => ({
                'Loại hành khách': item.passenger_type,
                'Quốc tịch': item.nationality,
                'Số lượng': item.total_passengers,
                'Số đặt chỗ': item.total_bookings
            }));

            exportToExcel(
                exportData,
                'ThongKeHanhKhach',
                'BÁO CÁO THỐNG KÊ HÀNH KHÁCH THEO LOẠI'
            );
        }
    } catch (error) {
        console.error('Error exporting passenger stats:', error);
    }
}