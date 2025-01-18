document.addEventListener('DOMContentLoaded', function () {
    const applyPromoBtn = document.getElementById('applyPromoBtn');
    const applyType = document.getElementById('applyType');
    const applyListContainer = document.getElementById('applyListContainer');
    const saveApplyBtn = document.getElementById('saveApplyBtn');
    const promoIdField = document.getElementById('maKhuyenMai');

    // Open modal and load default options
    applyPromoBtn.addEventListener('click', () => {
        const promoId = document.getElementById('maKhuyenMai').value.trim();

        if (!promoId) {
            alert('Vui lòng nhập mã khuyến mãi trước khi áp dụng.');
            return;
        }

        loadApplyList('airlines');
        new bootstrap.Modal(document.getElementById('applyPromoModal')).show();
    });

    // Change list based on type selection
    applyType.addEventListener('change', (e) => {
        loadApplyList(e.target.value);
    });

    // Fetch and display data for the selected type
    async function loadApplyList(type) {
        try {
            const promoId = promoIdField.value.trim();
            if (!promoId) {
                alert('Vui lòng nhập mã khuyến mãi trước khi áp dụng.');
                return;
            }

            let url = '';
            if (type === 'airlines') {
                url = '/api/hang-hang-khong';
            } else if (type === 'flights') {
                url = `/api/flights?after_date=${getNextDay(promoIdField.dataset.endDate)}`;
            }

            const response = await fetch(url);
            const result = await response.json();

            if (result.status !== 'success') {
                throw new Error(result.message);
            }

            const list = result.data.map((item) => `
                <div class="form-check">
                    <input class="form-check-input apply-checkbox" type="checkbox" value="${item.code || item.flight_code}" id="${item.code || item.flight_code}">
                    <label class="form-check-label" for="${item.code || item.flight_code}">
                        ${item.name || item.flight_code} - ${item.additional_info || ''}
                    </label>
                </div>
            `).join('');

            applyListContainer.innerHTML = `<form>${list}</form>`;
        } catch (error) {
            console.error('Error loading apply list:', error.message);
            alert('Có lỗi xảy ra khi tải danh sách.');
        }
    }

    // Save selected options
    saveApplyBtn.addEventListener('click', async () => {
        try {
            const promoId = promoIdField.value.trim();
            const selected = [...document.querySelectorAll('.apply-checkbox:checked')].map((cb) => cb.value);
            const type = applyType.value;

            if (!promoId || selected.length === 0) {
                alert('Vui lòng chọn ít nhất một mục.');
                return;
            }

            const payload = {
                MaKhuyenMai: promoId,
                Items: selected,
                Type: type,
            };

            const response = await fetch('/api/khuyen-mai/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (!result.status) {
                throw new Error(result.message);
            }

            alert('Áp dụng thành công.');
            document.getElementById('applyPromoModal').modal('hide');
        } catch (error) {
            console.error('Error saving applied promotions:', error.message);
            alert('Có lỗi xảy ra.');
        }
    });

    function getNextDay(dateString) {
        const date = new Date(dateString);
        date.setDate(date.getDate() + 1);
        return date.toISOString().split('T')[0];
    }
});
