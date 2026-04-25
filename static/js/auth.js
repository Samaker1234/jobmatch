// ============= VALIDATION UTILITIES =============

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}

function validatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    return strength;
}

function validatePhone(phone) {
    return phone.replace(/\D/g, '').length >= 10;
}

// ============= FORM VALIDATION =============

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(fieldId + '-error');
    
    if (field) {
        field.style.borderColor = '#E74C3C';
    }
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.add('show');
    }
}

function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(fieldId + '-error');
    
    if (field) {
        field.style.borderColor = '#BDC3C7';
    }
    if (errorEl) {
        errorEl.textContent = '';
        errorEl.classList.remove('show');
    }
}

// ============= PASSWORD TOGGLE =============

function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
    }
}

// ============= LOCAL STORAGE UTILITIES =============

function saveFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    const formData = new FormData(form);
    const data = {};
    
    formData.forEach((value, key) => {
        if (key !== 'password' && key !== 'confirm-password') {
            data[key] = value;
        }
    });

    localStorage.setItem('formData_' + formId, JSON.stringify(data));
}

function loadFormData(formId) {
    const savedData = localStorage.getItem('formData_' + formId);
    if (!savedData) return;

    const data = JSON.parse(savedData);
    Object.keys(data).forEach(key => {
        const field = document.getElementById(key) || 
                     document.querySelector(`[name="${key}"]`);
        if (field) {
            field.value = data[key];
        }
    });
}

function clearFormData(formId) {
    localStorage.removeItem('formData_' + formId);
}

// ============= ANIMATION UTILITIES =============

function addShakeAnimation(element) {
    if (!element) return;
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = 'shake 0.5s ease-in-out';
    }, 10);
}

// Add CSS animation
if (!document.querySelector('style[data-animation="shake"]')) {
    const style = document.createElement('style');
    style.setAttribute('data-animation', 'shake');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
    `;
    document.head.appendChild(style);
}

// ============= LOAD FORM DATA ON PAGE LOAD =============

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('register-form')) {
        loadFormData('register-form');
    }
});

// ============= SAVE FORM DATA ON INPUT CHANGE =============

document.addEventListener('change', function(e) {
    if (e.target.form && e.target.form.id === 'register-form') {
        saveFormData('register-form');
    }
});

// ============= CLEAR ERRORS ON INPUT =============

document.addEventListener('input', function(e) {
    if (e.target.id) {
        clearFieldError(e.target.id);
    }
});

// ============= EXTERNAL SCRIPT: Add GA, Analytics, etc. =============

// Placeholder for analytics tracking
function trackEvent(eventName, eventData) {
    console.log('Event tracked:', eventName, eventData);
    // Add your analytics here (Google Analytics, Mixpanel, etc.)
}