const ADMIN_CREDS = { id: '1234', pass: 'canteen' };

// Initialize Storage on Load
function initStorage() {
    if (!localStorage.getItem('canteen_users')) {
        localStorage.setItem('canteen_users', JSON.stringify([]));
    }
}

// Redirects
function requireAuth() {
    const user = localStorage.getItem('canteen_current_user');
    const path = window.location.pathname;
    // Get just the filename, e.g. "dashboard.html" or "" for root
    const page = path.split('/').pop();

    // These pages should NEVER redirect — user is logging in here
    const bypassPages = ['index.html', 'signup.html', 'admin.html', 'admin-signup.html', 'admin-dashboard.html', ''];
    const isBypassPage = bypassPages.includes(page);

    if (!user && !isBypassPage) {
        window.location.href = 'index.html';
        return null;
    }
    return user ? JSON.parse(user) : null;
}

function requireAdmin() {
    const isAdmin = localStorage.getItem('canteen_is_admin');
    const path = window.location.pathname;
    const page = path.split('/').pop();

    if (isAdmin !== 'true' && page === 'admin-dashboard.html') {
        window.location.href = 'admin.html';
        return false;
    }
    return isAdmin === 'true';
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initStorage();
    
    // Login Form Intercept
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            fetch('http://127.0.0.1:5000/api/login/student', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.user) {
                    data.user.type = data.user.customer_type; // Map for backwards compatibility
                    localStorage.setItem('canteen_current_user', JSON.stringify(data.user));
                    localStorage.setItem('canteen_is_admin', 'false');
                    window.location.href = 'dashboard.html';
                } else {
                    alert(data.error || 'Invalid Student ID / Email or Password. Please try again or create an account.');
                }
            })
            .catch(err => {
                console.error('Error logging in:', err);
                alert('Failed to connect to server. Ensure backend is running.');
            });
        });
    }

    // Signup Form Intercept
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('name').value.trim();
            const type = document.getElementById('type').value;
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // --- Validation Rules ---
            const errors = [];

            // 1. Name: letters and spaces only, 3-50 chars
            if (!/^[A-Za-z\s]{3,50}$/.test(name)) {
                errors.push('❌ Full Name must be 3–50 characters and contain only letters.');
            }

            // 2. Email: valid email OR student-ID format (letters + digits, min 5 chars)
            const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
            const isValidStudentId = /^[A-Za-z0-9]{5,20}$/.test(email);
            if (!isValidEmail && !isValidStudentId) {
                errors.push('❌ Enter a valid Email (e.g. john@college.edu) or Student ID (5–20 alphanumeric chars).');
            }

            // 3. Phone: exactly 10 digits
            if (!/^\d{10}$/.test(phone)) {
                errors.push('❌ Phone Number must be exactly 10 digits (e.g. 9876543210).');
            }

            // 4. Password: at least 8 chars, must include at least one letter and one digit
            if (password.length < 8) {
                errors.push('❌ Password must be at least 8 characters long.');
            } else if (!/[A-Za-z]/.test(password) || !/\d/.test(password)) {
                errors.push('❌ Password must contain at least one letter and one number (e.g. pass1234).');
            }

            if (errors.length > 0) {
                alert('Please fix the following errors:\n\n' + errors.join('\n'));
                return;
            }

            fetch('http://127.0.0.1:5000/api/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, customer_type: type, phone_no: phone, email, password })
            })
            .then(async res => {
                const data = await res.json();
                if (res.ok) {
                    alert('✅ Account created successfully! You can now login.');
                    window.location.href = 'index.html';
                } else {
                    alert('❌ ' + (data.error || 'An error occurred during signup.'));
                }
            })
            .catch(err => {
                console.error('Error during signup:', err);
                alert('Failed to connect to server.');
            });
        });
    }

    // Admin Login Intercept
    const adminForm = document.getElementById('admin-form');
    if (adminForm) {
        adminForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('admin-id').value.trim();
            const pass = document.getElementById('admin-key').value;

            fetch('http://127.0.0.1:5000/api/login/admin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: id, password: pass })
            })
            .then(res => res.json())
            .then(data => {
                if (data.admin) {
                    localStorage.setItem('canteen_is_admin', 'true');
                    localStorage.removeItem('canteen_current_user'); // Clear student session
                    window.location.href = 'admin-dashboard.html';
                } else {
                    alert('Unauthorized Access: ' + (data.error || 'Bad Admin ID or Key.'));
                }
            })
            .catch(err => {
                console.error('Error in admin login:', err);
                alert('Failed to connect to server.');
            });
        });
    }

    // Admin Signup Form Intercept
    const adminSignupForm = document.getElementById('admin-signup-form');
    if (adminSignupForm) {
        adminSignupForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('admin-name').value.trim();
            const phone = document.getElementById('admin-phone').value.trim();
            const email = document.getElementById('admin-email').value.trim();
            const password = document.getElementById('admin-password').value;

            // --- Validation Rules ---
            const errors = [];

            // 1. Name: letters and spaces only, 3-50 chars
            if (!/^[A-Za-z\s]{3,50}$/.test(name)) {
                errors.push('❌ Full Name must be 3–50 characters and contain only letters.');
            }

            // 2. Email validation
            const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
            if (!isValidEmail) {
                errors.push('❌ Enter a valid Email (e.g. admin@college.edu).');
            }

            // 3. Phone: exactly 10 digits
            if (!/^\d{10}$/.test(phone)) {
                errors.push('❌ Phone Number must be exactly 10 digits (e.g. 9876543210).');
            }

            // 4. Password: at least 8 chars, must include at least one letter and one digit
            if (password.length < 8) {
                errors.push('❌ Password must be at least 8 characters long.');
            } else if (!/[A-Za-z]/.test(password) || !/\d/.test(password)) {
                errors.push('❌ Password must contain at least one letter and one number (e.g. admin123).');
            }

            if (errors.length > 0) {
                alert('Please fix the following errors:\n\n' + errors.join('\n'));
                return;
            }

            fetch('http://127.0.0.1:5000/api/signup/admin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, phone_no: phone, email, password })
            })
            .then(async res => {
                const data = await res.json();
                if (res.ok) {
                    alert('✅ Admin Account created successfully! You can now login.');
                    window.location.href = 'admin.html';
                } else {
                    alert('❌ ' + (data.error || 'An error occurred during signup.'));
                }
            })
            .catch(err => {
                console.error('Error during admin signup:', err);
                alert('Failed to connect to server.');
            });
        });
    }
});

// Logout Helper (Accessible Globally)
window.logout = function() {
    localStorage.removeItem('canteen_current_user');
    localStorage.removeItem('canteen_is_admin');
    window.location.href = 'index.html';
};
