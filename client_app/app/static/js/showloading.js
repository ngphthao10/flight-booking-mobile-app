function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    hideError(containerId);
    hideNoData(containerId);

    const loader = document.createElement('div');
    loader.className = 'loading-spinner position-absolute top-50 start-50 translate-middle';
    loader.innerHTML = `
<div class="spinner-border text-primary" role="status">
  <span class="visually-hidden">Loading...</span>
</div>`;

    container.appendChild(loader);
}

function hideLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const loader = container.querySelector('.loading-spinner');
    if (loader) loader.remove();
}

function showError(message, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const error = document.createElement('div');
    error.className = 'error-message text-center text-danger mt-3';
    error.textContent = message;

    container.appendChild(error);
}

function hideError(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const error = container.querySelector('.error-message');
    if (error) error.remove();
}

function showNoData(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const noData = document.createElement('div');
    noData.className = 'no-data-message text-center text-muted mt-3';
    noData.textContent = 'Không có dữ liệu';

    container.appendChild(noData);
}

function hideNoData(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const noData = container.querySelector('.no-data-message');
    if (noData) noData.remove();
}
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    hideError(containerId);
    hideNoData(containerId);

    const loader = document.createElement('div');
    loader.className = 'loading-spinner position-absolute top-50 start-50 translate-middle';
    loader.innerHTML = `
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>`;

    container.appendChild(loader);
}

function hideLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const loader = container.querySelector('.loading-spinner');
    if (loader) loader.remove();
}

function showError(message, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const error = document.createElement('div');
    error.className = 'error-message text-center text-danger mt-3';
    error.textContent = message;

    container.appendChild(error);
}

function hideError(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const error = container.querySelector('.error-message');
    if (error) error.remove();
}

// Helper functions
function getPeriodLabel(timeRange) {
    const labels = {
        'today': 'Hôm nay',
        'yesterday': 'Hôm qua',
        'last_7_days': '7 ngày qua',
        'last_14_days': '14 ngày qua',
        'last_21_days': '21 ngày qua',
        'last_month': '1 tháng trước',
        'last_3_months': '3 tháng trước'
    };
    return labels[timeRange] || timeRange;
}

function getRevenueChartTitle(month, year) {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth() + 1;
    const currentYear = currentDate.getFullYear();

    // Sử dụng giá trị mặc định nếu month hoặc year không được truyền
    const selectedMonth = month || currentMonth;
    const selectedYear = year || currentYear;

    const isAllMonth = selectedMonth === 'all';
    const isAllYear = selectedYear === 'all';

    if (!isAllMonth && !isAllYear) {
        return `Xu hướng doanh thu Tháng ${selectedMonth}/${selectedYear}`;
    } else if (isAllMonth && !isAllYear) {
        return `Xu hướng doanh thu Năm ${selectedYear}`;
    } else if (!isAllMonth && isAllYear) {
        return `Xu hướng doanh thu Tháng ${selectedMonth} (tất cả năm)`;
    } else {
        return `Xu hướng doanh thu (tất cả thời gian)`;
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit'
    });
}