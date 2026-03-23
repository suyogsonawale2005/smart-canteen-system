const API_BASE = "https://smart-canteen-system-hvah.onrender.com";

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
    const page = path.split('/').pop();

    // Support both XAMPP local testing (.html) and Vercel production clean URLs
    const bypassPages = [
        'index.html', 'signup.html', 'admin.html', 'admin-signup.html', 'admin-dashboard.html', '',
        'index', 'signup', 'admin', 'admin-signup', 'admin-dashboard'
    ];
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

    const isDashboard = (page === 'admin-dashboard.html' || page === 'admin-dashboard');

    if (isAdmin !== 'true' && isDashboard) {
        window.location.href = 'admin.html';
        return false;
    }
    return isAdmin === 'true';
}

document.addEventListener('DOMContentLoaded', () => {
    initStorage();

    // ================= LOGIN =================
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            fetch(`${API_BASE}/api/login/student`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.user) {
                    data.user.type = data.user.customer_type;
                    localStorage.setItem('canteen_current_user', JSON.stringify(data.user));
                    localStorage.setItem('canteen_is_admin', 'false');
                    window.location.href = 'dashboard.html';
                } else {
                    alert(data.error || 'Invalid credentials');
                }
            })
            .catch(() => alert('Server not reachable'));
        });
    }

    // ================= SIGNUP =================
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('name').value.trim();
            const type = document.getElementById('type').value;
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            fetch(`${API_BASE}/api/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, customer_type: type, phone_no: phone, email, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    alert('Signup successful');
                    window.location.href = 'index.html';
                } else {
                    alert(data.error);
                }
            })
            .catch(() => alert('Server error'));
        });
    }

    // ================= ADMIN LOGIN =================
    const adminForm = document.getElementById('admin-form');
    if (adminForm) {
        adminForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const id = document.getElementById('admin-id').value.trim();
            const pass = document.getElementById('admin-key').value;

            fetch(`${API_BASE}/api/login/admin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: id, password: pass })
            })
            .then(res => res.json())
            .then(data => {
                if (data.admin) {
                    localStorage.setItem('canteen_is_admin', 'true');
                    localStorage.removeItem('canteen_current_user');
                    window.location.href = 'admin-dashboard.html';
                } else {
                    alert(data.error);
                }
            })
            .catch(() => alert('Server error'));
        });
    }

    // ================= ADMIN SIGNUP =================
    const adminSignupForm = document.getElementById('admin-signup-form');
    if (adminSignupForm) {
        adminSignupForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('admin-name').value.trim();
            const phone = document.getElementById('admin-phone').value.trim();
            const email = document.getElementById('admin-email').value.trim();
            const password = document.getElementById('admin-password').value;

            fetch(`${API_BASE}/api/signup/admin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, phone_no: phone, email, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    alert('Admin created');
                    window.location.href = 'admin.html';
                } else {
                    alert(data.error);
                }
            })
            .catch(() => alert('Server error'));
        });
    }
});

// Logout
window.logout = function() {
    localStorage.removeItem('canteen_current_user');
    localStorage.removeItem('canteen_is_admin');
    window.location.href = 'index.html';
};