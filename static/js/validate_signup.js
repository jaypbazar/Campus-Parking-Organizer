document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.querySelector('form[action="/signup"]');
    const passwordInput = document.getElementById('inputPassword');
    const confirmPasswordInput = document.getElementById('inputPassword2');
    const emailInput = document.querySelector('input[name="email"]');

    // Function to validate password match
    function validatePasswordMatch() {
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.setCustomValidity('Passwords do not match');
            return false;
        } else {
            confirmPasswordInput.setCustomValidity('');
            return true;
        }
    }

    // Function to validate CSPC email domain
    function validateEmailDomain() {
        const email = emailInput.value;
        const domain = 'cspc.edu.ph';
        
        if (!email.endsWith(domain)) {
            emailInput.setCustomValidity('Email must be a CSPC email (cspc.edu.ph domain)');
            return false;
        } else {
            emailInput.setCustomValidity('');
            return true;
        }
    }

    // Function to display validation error in a modal
    function showValidationError(message) {
        const modal = document.createElement('div');
        modal.classList.add('modal');

        const modalContent = document.createElement('div');
        modalContent.classList.add('modal-content');

        const errorMessage = document.createElement('p');
        errorMessage.textContent = message;

        const closeButton = document.createElement('button');
        closeButton.textContent = 'OK';
        closeButton.onclick = function() {
            modal.style.display = 'none';
        };

        modalContent.appendChild(errorMessage);
        modalContent.appendChild(closeButton);
        modal.appendChild(modalContent);

        document.body.appendChild(modal);
        modal.style.display = 'block';
    }

    // Add event listeners for real-time validation
    passwordInput.addEventListener('input', validatePasswordMatch);
    confirmPasswordInput.addEventListener('input', validatePasswordMatch);
    emailInput.addEventListener('input', validateEmailDomain);

    // Add form submission validation
    form.addEventListener('submit', function(event) {
        if (!validatePasswordMatch() || !validateEmailDomain()) {
            event.preventDefault(); // Prevent form submission if validation fails

            if (!validatePasswordMatch()) {
                showValidationError('Passwords do not match');
            } else if (!validateEmailDomain()) {
                showValidationError('Email must be a CSPC email.');
            }
        }
    });
});