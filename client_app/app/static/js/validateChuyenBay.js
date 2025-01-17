
const form = document.getElementById('flightForm');

function formatNumber(number) {
    return new Intl.NumberFormat('vi-VN').format(number);
}

function formatPriceInput(displayInput, realInputId) {
    let value = displayInput.value.replace(/[^\d]/g, '');

    document.getElementById(realInputId).value = value;

    if (value) {
        displayInput.value = formatNumber(value);
    } else {
        displayInput.value = '';
    }

    validateTicketPrices();
}

function validateTicketPrices() {
    const busPrice = document.getElementById('realBusPrice');
    const ecoPrice = document.getElementById('realEcoPrice');
    const busDisplay = document.getElementById('displayBusPrice');
    const ecoDisplay = document.getElementById('displayEcoPrice');
    const busError = document.getElementById('GiaVeBusError');
    const ecoError = document.getElementById('GiaVeEcoError');

    let isValid = true;

    busDisplay.classList.remove('is-invalid');
    ecoDisplay.classList.remove('is-invalid');

    if (busPrice.value) {
        const busPriceVal = Number(busPrice.value);
        if (busPriceVal < 0 || busPriceVal > 10000000000) {
            busDisplay.classList.add('is-invalid');
            busError.innerHTML = 'Giá vé phải từ 0 đến 10 tỷ VNĐ';
            isValid = false;
        }
    }

    if (ecoPrice.value) {
        const ecoPriceVal = Number(ecoPrice.value);
        if (ecoPriceVal < 0 || ecoPriceVal > 10000000000) {
            ecoDisplay.classList.add('is-invalid');
            ecoError.innerHTML = 'Giá vé phải từ 0 đến 10 tỷ VNĐ';
            isValid = false;
        }

        if (busPrice.value && Number(busPrice.value) <= ecoPriceVal) {
            busDisplay.classList.add('is-invalid');
            busError.innerHTML = 'Giá vé Business phải lớn hơn giá vé Economy';
            isValid = false;
        }
    }

    return isValid;
}


document.querySelector('input[name="GiaVeBus"]').addEventListener('input', validateTicketPrices);
document.querySelector('input[name="GiaVeEco"]').addEventListener('input', validateTicketPrices);

function validateFlightTimes() {
    const departureTime = document.querySelector('input[name="ThoiGianDi"]');
    const arrivalTime = document.querySelector('input[name="ThoiGianDen"]');
    const arrivalError = document.querySelector('input[name="ThoiGianDen"]').nextElementSibling;

    let isValid = true;

    departureTime.classList.remove('is-invalid');
    arrivalTime.classList.remove('is-invalid');

    if (departureTime.value && arrivalTime.value) {
        const departure = new Date(departureTime.value);
        const arrival = new Date(arrivalTime.value);
        const timeDiff = (arrival - departure) / (1000 * 60 * 60);

        if (arrival <= departure) {
            arrivalTime.classList.add('is-invalid');
            arrivalError.textContent = 'Thời gian đến phải sau thời gian đi';
            isValid = false;
        }

        if (timeDiff > 24) {
            arrivalTime.classList.add('is-invalid');
            arrivalError.textContent = 'Thời gian bay không được quá 24 giờ';
            isValid = false;
        }
    }

    return isValid;
}

function validateAirports() {
    const departureAirport = document.querySelector('select[name="MaSanBayDi"]');
    const arrivalAirport = document.querySelector('select[name="MaSanBayDen"]');
    const arrivalError = document.querySelector('select[name="MaSanBayDen"]').nextElementSibling;

    let isValid = true;

    departureAirport.classList.remove('is-invalid');
    arrivalAirport.classList.remove('is-invalid');

    if (departureAirport.value && arrivalAirport.value) {
        if (departureAirport.value === arrivalAirport.value) {
            departureAirport.classList.add('is-invalid');
            arrivalAirport.classList.add('is-invalid');
            arrivalError.textContent = 'Sân bay đến không được trùng với sân bay đi';
            isValid = false;
        }
    }

    return isValid;
}

form.addEventListener('submit', function (event) {
    if (!validateTicketPrices() || !validateFlightTimes() || !validateAirports()) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
});