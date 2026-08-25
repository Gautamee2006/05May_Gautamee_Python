// QuickCart Client Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alert messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Product Detail Gallery Switcher
    const mainImg = document.getElementById('mainProductImage');
    const thumbnails = document.querySelectorAll('.qc-thumbnail');

    if (mainImg && thumbnails.length > 0) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                mainImg.src = this.dataset.src;
                thumbnails.forEach(t => t.classList.remove('border-primary', 'active'));
                this.classList.add('border-primary', 'active');
            });
        });
    }

    // Quantity Selector Buttons
    const qtyInput = document.getElementById('productQtyInput');
    const btnMinus = document.getElementById('btnQtyMinus');
    const btnPlus = document.getElementById('btnQtyPlus');

    if (qtyInput && btnMinus && btnPlus) {
        const maxStock = parseInt(qtyInput.getAttribute('max')) || 99;

        btnMinus.addEventListener('click', function() {
            let currentVal = parseInt(qtyInput.value) || 1;
            if (currentVal > 1) {
                qtyInput.value = currentVal - 1;
            }
        });

        btnPlus.addEventListener('click', function() {
            let currentVal = parseInt(qtyInput.value) || 1;
            if (currentVal < maxStock) {
                qtyInput.value = currentVal + 1;
            } else {
                alert(`Maximum available stock is ${maxStock} units.`);
            }
        });
    }
});
