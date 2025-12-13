/**
 * Client-side validation utilities for Bank System
 */

// Validation constants
const MIN_TRANSFER_AMOUNT = 0.01;
const MAX_TRANSFER_AMOUNT = 1000000.00;
const MIN_PASSWORD_LENGTH = 6;
const MIN_USERNAME_LENGTH = 3;
const MAX_USERNAME_LENGTH = 50;

/**
 * Validate email format
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if valid
 */
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

/**
 * Validate username format
 * @param {string} username - Username to validate
 * @returns {boolean} - True if valid
 */
function validateUsername(username) {
    const usernamePattern = /^[a-zA-Z0-9_]{3,50}$/;
    return usernamePattern.test(username);
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} - {valid: boolean, strength: string, message: string}
 */
function validatePassword(password) {
    if (!password || password.length < MIN_PASSWORD_LENGTH) {
        return {
            valid: false,
            strength: 'weak',
            message: `Password must be at least ${MIN_PASSWORD_LENGTH} characters`
        };
    }
    
    let strength = 'weak';
    let score = 0;
    
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;
    
    if (score >= 5) strength = 'strong';
    else if (score >= 3) strength = 'medium';
    
    return {
        valid: true,
        strength: strength,
        message: `Password strength: ${strength}`
    };
}

/**
 * Validate amount for transfers/transactions
 * @param {number} amount - Amount to validate
 * @param {number} maxAmount - Maximum allowed amount (e.g., balance)
 * @returns {object} - {valid: boolean, message: string}
 */
function validateAmount(amount, maxAmount = MAX_TRANSFER_AMOUNT) {
    if (isNaN(amount) || amount <= 0) {
        return {
            valid: false,
            message: 'Amount must be a positive number'
        };
    }
    
    if (amount < MIN_TRANSFER_AMOUNT) {
        return {
            valid: false,
            message: `Minimum amount is $${MIN_TRANSFER_AMOUNT}`
        };
    }
    
    if (amount > maxAmount) {
        return {
            valid: false,
            message: `Amount cannot exceed $${maxAmount.toFixed(2)}`
        };
    }
    
    return {
        valid: true,
        message: 'Valid amount'
    };
}

/**
 * Show password strength indicator
 * @param {string} passwordId - ID of password input
 * @param {string} indicatorId - ID of indicator element
 */
function showPasswordStrength(passwordId, indicatorId) {
    const passwordInput = document.getElementById(passwordId);
    const indicator = document.getElementById(indicatorId);
    
    if (!passwordInput || !indicator) return;
    
    passwordInput.addEventListener('input', function() {
        const result = validatePassword(this.value);
        
        if (this.value.length === 0) {
            indicator.textContent = '';
            indicator.className = '';
            return;
        }
        
        indicator.textContent = result.message;
        
        if (result.strength === 'strong') {
            indicator.className = 'text-success';
        } else if (result.strength === 'medium') {
            indicator.className = 'text-warning';
        } else {
            indicator.className = 'text-danger';
        }
    });
}

/**
 * Format currency for display
 * @param {number} amount - Amount to format
 * @returns {string} - Formatted currency string
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Confirm action with user
 * @param {string} message - Confirmation message
 * @returns {boolean} - True if confirmed
 */
function confirmAction(message) {
    return confirm(message);
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateEmail,
        validateUsername,
        validatePassword,
        validateAmount,
        showPasswordStrength,
        formatCurrency,
        confirmAction
    };
}
