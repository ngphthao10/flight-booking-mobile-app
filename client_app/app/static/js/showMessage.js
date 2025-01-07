function showMessage(type, message) {
    const toastEl = document.getElementById('liveToast');
    const toastHeader = toastEl.querySelector('.toast-header');

    toastEl.className = 'toast border-' + (type === 'success' ? 'success' : 'danger');
    toastHeader.className = 'toast-header text-white ' + (type === 'success' ? 'bg-success' : 'bg-danger');

    const closeBtn = toastHeader.querySelector('.btn-close');
    closeBtn.className = 'btn-close btn-close-white';

    toastEl.querySelector('.toast-body').textContent = message;

    const toast = new bootstrap.Toast(toastEl, {
        delay: 5000
    });
    toast.show();
}

function showMessageAndRedirect(type, message, redirectUrl) {
    localStorage.setItem('toast', JSON.stringify({
        type: type,
        message: message
    }));

    window.location.href = redirectUrl;
}