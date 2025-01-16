const TIMER_KEY = 'paymentTimer';
const START_TIME_KEY = 'paymentStartTime';
const TOTAL_TIME = 600;

function getTimeLeft() {
    const startTime = parseInt(localStorage.getItem(START_TIME_KEY));

    const isFromBookingInfo = localStorage.getItem('isFromBookingInfo');

    if (!startTime || isFromBookingInfo === 'true') {
        localStorage.removeItem('isFromBookingInfo');
        const currentTime = new Date().getTime();
        localStorage.setItem(START_TIME_KEY, currentTime);
        return TOTAL_TIME;
    }

    const currentTime = new Date().getTime();
    const elapsedSeconds = Math.floor((currentTime - startTime) / 1000);
    const timeLeft = Math.max(0, TOTAL_TIME - elapsedSeconds);

    return timeLeft;
}

function updateTimer() {
    function updateDisplay() {
        const timeLeft = getTimeLeft();
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        const formattedTime = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        document.getElementById('countdown').textContent = formattedTime;

        if (timeLeft > 0) {
            setTimeout(updateDisplay, 1000);
        } else {
            document.getElementById('countdown').textContent = "0:00";
            localStorage.removeItem(START_TIME_KEY);
            showMessage('danger', 'Đã hết thời gian thanh toán!');
        }
    }

    updateDisplay();
}

document.addEventListener('DOMContentLoaded', updateTimer);