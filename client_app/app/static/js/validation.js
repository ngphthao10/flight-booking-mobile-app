// Các hàm validate helper
const isValidEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

const isValidPhone = (phone) => {
    const re = /^[0-9]{9,10}$/;
    return re.test(phone);
};

const isValidCardId = (cardId) => {
    const re = /^[0-9]{12}$/;
    return re.test(cardId);
};

const isValidName = (name) => {
    const re = /^[a-zA-Z\s]+$/;
    return re.test(name);
};

// Hiển thị lỗi
const showError = (input, message) => {
    const formGroup = input.closest('.col-md-6, .col-md-4, .col');
    // Tìm hoặc tạo div error
    let errorDiv = formGroup.querySelector('.error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message text-danger mt-1';
        // Chèn error div sau small text-muted nếu có
        const smallText = formGroup.querySelector('small.text-muted');
        if (smallText) {
            smallText.insertAdjacentElement('afterend', errorDiv);
        } else {
            formGroup.appendChild(errorDiv);
        }
    }
    errorDiv.textContent = message;
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
};

// Hiển thị thành công
const showSuccess = (input) => {
    const formGroup = input.closest('.col-md-6, .col-md-4, .col');
    const errorDiv = formGroup.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
};

// Kiểm tra tuổi
const validateAge = (birthDate, type) => {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    switch (type) {
        case 'adult': return age >= 12;
        case 'child': return age >= 2 && age < 12;
        case 'infant': return age < 2;
        default: return false;
    }
};

// Validate field
// const validateField = (input) => {
//     if (!input) return;

//     const value = input.value.trim();
//     const id = input.id;

//     // Check if field is in passenger form
//     const passengerMatch = id.match(/(adult|child|infant)_(\d+)_(\w+)/);

//     if (passengerMatch) {
//         const [_, type, index, field] = passengerMatch;

//         switch (field) {
//             case 'title':
//                 if (!value) {
//                     showError(input, 'Vui lòng chọn danh xưng');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'lastname':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập họ');
//                 } else if (!isValidName(value)) {
//                     showError(input, 'Họ không được chứa số và dấu');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'firstname':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập tên');
//                 } else if (!isValidName(value)) {
//                     showError(input, 'Tên không được chứa số và dấu');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'day':
//             case 'month':
//             case 'year':
//                 const parentRow = input.closest('.row');
//                 const daySelect = parentRow.querySelector(`#${type}_${index}_day`);
//                 const monthSelect = parentRow.querySelector(`#${type}_${index}_month`);
//                 const yearSelect = parentRow.querySelector(`#${type}_${index}_year`);

//                 if (daySelect.value && monthSelect.value && yearSelect.value) {
//                     const birthDate = new Date(
//                         yearSelect.value,
//                         monthSelect.value - 1,
//                         daySelect.value
//                     );

//                     if (isNaN(birthDate.getTime())) {
//                         showError(input, 'Ngày không hợp lệ');
//                         return;
//                     }

//                     if (!validateAge(birthDate, type)) {
//                         const ageRanges = {
//                             adult: 'từ 12 tuổi trở lên',
//                             child: 'từ 2 đến 11 tuổi',
//                             infant: 'dưới 2 tuổi'
//                         };
//                         showError(input, `Độ tuổi phải ${ageRanges[type]}`);
//                     } else {
//                         showSuccess(daySelect);
//                         showSuccess(monthSelect);
//                         showSuccess(yearSelect);
//                     }
//                 } else if (!value) {
//                     showError(input, 'Vui lòng chọn đầy đủ ngày sinh');
//                 }
//                 break;

//             case 'nationality':
//                 if (!value) {
//                     showError(input, 'Vui lòng chọn quốc tịch');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;
//         }
//     } else {
//         // Validate contact form
//         switch (id) {
//             case 'contact_lastname':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập họ');
//                 } else if (!isValidName(value)) {
//                     showError(input, 'Họ không được chứa số và dấu');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'contact_firstname':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập tên');
//                 } else if (!isValidName(value)) {
//                     showError(input, 'Tên không được chứa số và dấu');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'contact_phone':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập số điện thoại');
//                 } else if (!isValidPhone(value)) {
//                     showError(input, 'Số điện thoại không hợp lệ (9-10 số)');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'contact_email':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập email');
//                 } else if (!isValidEmail(value)) {
//                     showError(input, 'Email không hợp lệ');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;

//             case 'CardId':
//                 if (!value) {
//                     showError(input, 'Vui lòng nhập số CCCD');
//                 } else if (!isValidCardId(value)) {
//                     showError(input, 'CCCD phải có 12 số');
//                 } else {
//                     showSuccess(input);
//                 }
//                 break;
//         }
//     }
// };

const validateField = (input) => {
    if (!input) return;

    const value = input.value.trim();
    const id = input.id;

    // Check if field is in passenger form
    const passengerMatch = id.match(/(adult|child|infant)_(\d+)_(\w+)/);

    if (passengerMatch) {
        const [_, type, index, field] = passengerMatch;

        switch (field) {
            case 'title':
                if (!value) {
                    showError(input, 'Vui lòng chọn danh xưng');
                } else {
                    showSuccess(input);
                }
                break;

            case 'lastname':
                if (!value) {
                    showError(input, 'Vui lòng nhập họ');
                } else if (!isValidName(value)) {
                    showError(input, 'Họ không được chứa số và dấu');
                } else {
                    showSuccess(input);
                }
                break;

            case 'firstname':
                if (!value) {
                    showError(input, 'Vui lòng nhập tên');
                } else if (!isValidName(value)) {
                    showError(input, 'Tên không được chứa số và dấu');
                } else {
                    showSuccess(input);
                }
                break;

            case 'day':
            case 'month':
            case 'year':
                const parentRow = input.closest('.row');
                const daySelect = parentRow.querySelector(`#${type}_${index}_day`);
                const monthSelect = parentRow.querySelector(`#${type}_${index}_month`);
                const yearSelect = parentRow.querySelector(`#${type}_${index}_year`);

                if (daySelect.value && monthSelect.value && yearSelect.value) {
                    const birthDate = new Date(
                        yearSelect.value,
                        monthSelect.value - 1,
                        daySelect.value
                    );

                    if (isNaN(birthDate.getTime())) {
                        showError(input, 'Ngày không hợp lệ');
                        return;
                    }

                    if (!validateAge(birthDate, type)) {
                        const ageRanges = {
                            adult: 'từ 12 tuổi trở lên',
                            child: 'từ 2 đến 11 tuổi',
                            infant: 'dưới 2 tuổi'
                        };
                        showError(input, `Độ tuổi phải ${ageRanges[type]}`);
                    } else {
                        showSuccess(daySelect);
                        showSuccess(monthSelect);
                        showSuccess(yearSelect);
                    }
                } else if (!value) {
                    showError(input, 'Vui lòng chọn đầy đủ ngày sinh');
                }
                break;

            case 'nationality':
                if (!value) {
                    showError(input, 'Vui lòng chọn quốc tịch');
                } else {
                    showSuccess(input);
                }
                break;

            case 'cccd':
                if (!value) {
                    showError(input, 'Vui lòng nhập số CCCD');
                } else if (!isValidCardId(value)) {
                    showError(input, 'CCCD phải có 12 số');
                } else {
                    showSuccess(input);
                }
                break;
        }
    } else {
        // Validate contact form
        switch (id) {
            case 'contact_lastname':
                if (!value) {
                    showError(input, 'Vui lòng nhập họ');
                } else if (!isValidName(value)) {
                    showError(input, 'Họ không được chứa số và dấu');
                } else {
                    showSuccess(input);
                }
                break;

            case 'contact_firstname':
                if (!value) {
                    showError(input, 'Vui lòng nhập tên');
                } else if (!isValidName(value)) {
                    showError(input, 'Tên không được chứa số và dấu');
                } else {
                    showSuccess(input);
                }
                break;

            case 'contact_phone':
                if (!value) {
                    showError(input, 'Vui lòng nhập số điện thoại');
                } else if (!isValidPhone(value)) {
                    showError(input, 'Số điện thoại không hợp lệ (9-10 số)');
                } else {
                    showSuccess(input);
                }
                break;

            case 'contact_email':
                if (!value) {
                    showError(input, 'Vui lòng nhập email');
                } else if (!isValidEmail(value)) {
                    showError(input, 'Email không hợp lệ');
                } else {
                    showSuccess(input);
                }
                break;

            case 'CardId':
                if (!value) {
                    showError(input, 'Vui lòng nhập số CCCD');
                } else if (!isValidCardId(value)) {
                    showError(input, 'CCCD phải có 12 số');
                } else {
                    showSuccess(input);
                }
                break;
        }
    }
};


// Set up event listeners using event delegation
document.addEventListener('DOMContentLoaded', () => {
    // Event delegation cho form hành khách
    const passengersForm = document.getElementById('passengersForm');
    if (passengersForm) {
        passengersForm.addEventListener('input', (e) => {
            if (e.target.matches('input, select')) {
                validateField(e.target);
            }
        });

        passengersForm.addEventListener('blur', (e) => {
            if (e.target.matches('input, select')) {
                validateField(e.target);
            }
        }, true);

        passengersForm.addEventListener('change', (e) => {
            if (e.target.matches('select')) {
                validateField(e.target);
            }
        });
    }

    // Event listeners cho form liên hệ
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('input', (e) => {
            if (e.target.matches('input, select')) {
                validateField(e.target);
            }
        });

        contactForm.addEventListener('blur', (e) => {
            if (e.target.matches('input, select')) {
                validateField(e.target);
            }
        }, true);

        contactForm.addEventListener('change', (e) => {
            if (e.target.matches('select')) {
                validateField(e.target);
            }
        });
    }

    // Validate khi submit form
    document.querySelectorAll('#contactForm, #passengersForm').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            let isValid = true;

            this.querySelectorAll('input, select').forEach(input => {
                validateField(input);
                if (input.classList.contains('is-invalid')) {
                    isValid = false;
                }
            });

            if (isValid) {
                console.log('Form hợp lệ, có thể submit');
                // Thêm code xử lý submit form tại đây
            }
        });
    });
});