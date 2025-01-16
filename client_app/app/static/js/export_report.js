async function exportMarketShare() {
    try {
        const timeFilter = document.getElementById('timeFilter')?.value || 'last_7_days';
        console.log(timeFilter)
        const response = await fetch(`/report/export-market-share?time=${timeFilter}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] ||
            `market_share_report_${timeFilter}_${new Date().toISOString()}.xlsx`;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('success', 'Xuất báo cáo thành công');

    } catch (error) {
        console.error('Export error:', error);
        showMessage('error', 'Lỗi: Không thể xuất báo cáo! Vui lòng thử lại sau!');
    }
}

async function exportMonthlySales() {
    try {

        const month = document.getElementById('monthSelect')?.value || 'all';
        const year = document.getElementById('yearSelect')?.value || 'all';

        const queryParams = new URLSearchParams({
            type: 'monthly',
            month: month,
            year: year
        });

        const response = await fetch(`/report/export-revenue?${queryParams}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:]/g, '');
        const monthText = month === 'all' ? 'all' : `M${month}`;
        const yearText = year === 'all' ? 'all' : year;
        const fileName = `revenue_report_${monthText}_${yearText}_${timestamp}.xlsx`;

        a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || fileName;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('success', 'Xuất báo cáo thành công');

    } catch (error) {
        console.error('Export error:', error);
        showMessage('error', 'Lỗi: Không thể xuất báo cáo! Vui lòng thử lại sau!');
    }
}

async function exportBookingStats() {
    try {
        const timeRange = document.getElementById('bookingTimeRange')?.value || 'last_7_days';

        const queryParams = new URLSearchParams({
            time_range: timeRange
        });

        const response = await fetch(`/report/export-booking-stats?${queryParams}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:]/g, '');
        const timeRangeText = timeRange.replace('last_', '').replace('_days', 'd').replace('_months', 'm');
        const fileName = `booking_stats_${timeRangeText}_${timestamp}.xlsx`;

        a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || fileName;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('success', 'Xuất báo cáo thành công');

    } catch (error) {
        console.error('Export error:', error);
        showMessage('error', 'Lỗi: Không thể xuất báo cáo! Vui lòng thử lại sau!');
    }
}

async function exportBookingStats() {
    try {
        const timeRange = document.getElementById('bookingTimeRange')?.value || 'last_7_days';

        const queryParams = new URLSearchParams({
            time_range: timeRange
        });

        const response = await fetch(`/report/export-booking-stats?${queryParams}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:]/g, '');
        const timeRangeText = timeRange.replace('last_', '').replace('_days', 'd').replace('_months', 'm');
        const fileName = `booking_stats_${timeRangeText}_${timestamp}.xlsx`;

        a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || fileName;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('success', 'Xuất báo cáo thành công');

    } catch (error) {
        console.error('Export error:', error);
        showMessage('error', 'Lỗi: Không thể xuất báo cáo! Vui lòng thử lại sau!');
    }
}

async function exportBaggageStats() {
    try {
        const timeRange = document.getElementById('baggageTimeRange')?.value || 'last_7_days';

        const queryParams = new URLSearchParams({
            time_range: timeRange
        });

        const response = await fetch(`/report/export-baggage-stats?${queryParams}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:]/g, '');
        const timeRangeText = timeRange.replace('last_', '').replace('_days', 'd').replace('_months', 'm');
        const fileName = `baggage_service_stats_${timeRangeText}_${timestamp}.xlsx`;

        a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || fileName;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('success', 'Xuất báo cáo thành công');

    } catch (error) {
        console.error('Export error:', error);
        showMessage('error', 'Lỗi: Không thể xuất báo cáo! Vui lòng thử lại sau!');
    }
}