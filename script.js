// Smart Canteen UI Logic

// Authentication Check
let currentUser = null;
if (typeof window.requireAuth === 'function') {
    currentUser = window.requireAuth();
}

// State
let cart = [];

// DOM Elements
const cartToggle = document.getElementById('cart-toggle');
const closeCart = document.getElementById('close-cart');
const cartSidebar = document.getElementById('cart-sidebar');
const cartOverlay = document.getElementById('cart-overlay');
const toastContainer = document.getElementById('toast-container');
const categoryBtns = document.querySelectorAll('.category-btn');

// Initialize User Info
function populateUserInfo() {
    const nameEl = document.getElementById('user-name');
    const roleEl = document.getElementById('user-role');
    const avatarEl = document.getElementById('user-avatar');
    
    if (currentUser && nameEl && roleEl && avatarEl) {
        nameEl.innerText = currentUser.name;
        roleEl.innerText = `${currentUser.type.toUpperCase()} • ${currentUser.email}`;
        avatarEl.innerText = currentUser.name.split(' ').map(n => n[0]).join('').toUpperCase();
    }
}

// Cart Toggle Logic
function openCartSidebar() {
    cartSidebar.classList.add('open');
    cartOverlay.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeCartSidebar() {
    cartSidebar.classList.remove('open');
    cartOverlay.classList.remove('show');
    document.body.style.overflow = '';
}

if (cartToggle) cartToggle.addEventListener('click', openCartSidebar);
if (closeCart) closeCart.addEventListener('click', closeCartSidebar);
if (cartOverlay) cartOverlay.addEventListener('click', closeCartSidebar);

// Toast Notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--success);"></i> ${message}`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideInUp 0.3s ease reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Canteen Operating Hours Logic
window.canteenHours = { open: '09:00', close: '18:00' };

async function fetchCanteenHours() {
    try {
        const res = await fetch('http://127.0.0.1:5000/api/settings');
        if (res.ok) {
            const data = await res.json();
            if (data.settings && data.settings.opening_time) {
                window.canteenHours.open = data.settings.opening_time;
                window.canteenHours.close = data.settings.closing_time;
            }
        }
    } catch (err) {
        console.error("Failed to fetch canteen hours", err);
    }
}

function isCanteenOpen() {
    if (!window.canteenHours) return true;
    const now = new Date();
    const currentMins = now.getHours() * 60 + now.getMinutes();

    const [oH, oM] = window.canteenHours.open.split(':').map(Number);
    const [cH, cM] = window.canteenHours.close.split(':').map(Number);
    const openMins = oH * 60 + oM;
    const closeMins = cH * 60 + cM;

    // Handle normal case (e.g. 09:00 to 18:00) 
    if (openMins <= closeMins) {
        return currentMins >= openMins && currentMins <= closeMins;
    } 
    // Handle overnight case (e.g. 18:00 to 02:00)
    return currentMins >= openMins || currentMins <= closeMins;
}

// Order Interaction Logic
window.addToCart = function(itemName, price, img, itemId) {
    if (!isCanteenOpen()) {
        const open12hr = new Date('1970-01-01T' + window.canteenHours.open).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const close12hr = new Date('1970-01-01T' + window.canteenHours.close).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        alert(`Sorry, the canteen is currently closed.\nOperating hours are ${open12hr} to ${close12hr}.\nWe are not taking orders right now.`);
        return;
    }

    if (window.isOutOfStock && window.isOutOfStock(itemName)) {
        alert(`${itemName} is currently Out of Stock!`);
        return;
    }

    const existingItem = cart.find(item => item.name === itemName);
    if (existingItem) {
        existingItem.qty++;
    } else {
        cart.push({ id: itemId, name: itemName, price: price, img: img, qty: 1 });
    }
    
    showToast(`Added ${itemName} to cart`);
    renderCart();
    
    // Animate badge
    const badge = document.getElementById('cart-count');
    badge.style.transform = 'scale(1.5)';
    setTimeout(() => badge.style.transform = 'scale(1)', 200);
};

function renderCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCountBadge = document.getElementById('cart-count');
    const cartFooter = document.querySelector('.cart-footer');
    
    let total = 0;
    let count = 0;
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="cart-empty" style="height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--text-light); gap: 1rem;">
                <i class="fa-solid fa-basket-shopping" style="font-size: 4rem; color: var(--border);"></i>
                <p>Your cart is empty</p>
                <button class="btn btn-outline" style="margin-top: 1rem;" onclick="closeCartSidebar()">Browse Menu</button>
            </div>
        `;
        cartFooter.innerHTML = `<div class="cart-total"><span>Total</span><span>₹0.00</span></div><button class="btn btn-primary" style="width: 100%; border-radius: var(--radius-full); margin-top: 1rem;" disabled>Place Order</button>`;
        cartCountBadge.innerText = '0';
        return;
    }

    cartItemsContainer.innerHTML = '';
    cart.forEach((item, index) => {
        total += item.price * item.qty;
        count += item.qty;
        
        const itemEl = document.createElement('div');
        itemEl.className = 'cart-item';
        itemEl.innerHTML = `
            <img src="${item.img}" alt="${item.name}" class="cart-item-img">
            <div class="cart-item-details">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">₹${item.price.toFixed(2)}</div>
                <div class="cart-item-actions">
                    <button class="qty-btn" onclick="updateCartQty(${index}, -1)"><i class="fa-solid fa-minus"></i></button>
                    <span class="qty-value">${item.qty}</span>
                    <button class="qty-btn" onclick="updateCartQty(${index}, 1)"><i class="fa-solid fa-plus"></i></button>
                    <button class="remove-item" onclick="removeFromCart(${index})"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
        `;
        cartItemsContainer.appendChild(itemEl);
    });

    cartCountBadge.innerText = count;
    cartFooter.innerHTML = `
        <div class="cart-total">
            <span>Total</span>
            <span>₹${total.toFixed(2)}</span>
        </div>
        <button class="btn btn-primary" style="width: 100%; border-radius: var(--radius-full); margin-top: 1rem;" onclick="placeOrder()">
            Place Order <i class="fa-solid fa-arrow-right"></i>
        </button>
    `;
}

window.updateCartQty = function(index, change) {
    cart[index].qty += change;
    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }
    renderCart();
};

window.removeFromCart = function(index) {
    cart.splice(index, 1);
    renderCart();
};

window.placeOrder = function() {
    if (!isCanteenOpen()) {
        const open12hr = new Date('1970-01-01T' + window.canteenHours.open).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const close12hr = new Date('1970-01-01T' + window.canteenHours.close).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        alert(`Sorry, the canteen is currently closed.\nOperating hours are ${open12hr} to ${close12hr}.\nWe are not taking orders right now.`);
        return;
    }

    if (cart.length === 0) return;
    
    // Calculate total
    const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
    
    // Show payment total in modal
    const totalEl = document.getElementById('payment-total');
    if (totalEl) totalEl.innerText = `₹${total.toFixed(2)}`;
    
    // Close cart sidebar, open payment modal
    closeCartSidebar();
    const modal = document.getElementById('payment-modal');
    if (modal) modal.style.display = 'flex';

    // Toggle UPI input visibility based on payment method
    const radios = document.querySelectorAll('input[name="payment-method"]');
    const upiSection = document.getElementById('upi-input-section');
    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (upiSection) upiSection.style.display = radio.value === 'upi' ? 'block' : 'none';
        });
    });
};

window.closePaymentModal = function() {
    const modal = document.getElementById('payment-modal');
    if (modal) modal.style.display = 'none';
};

window.confirmPayment = async function() {
    const method = document.querySelector('input[name="payment-method"]:checked');
    if (!method) return;

    // If UPI, validate UPI ID format
    if (method.value === 'upi') {
        const upiId = document.getElementById('upi-id').value.trim();
        if (!/^[\w.-]+@[\w]+$/.test(upiId)) {
            alert('❌ Please enter a valid UPI ID (e.g. name@upi or name@okaxis)');
            return;
        }
    }

    if (!currentUser || !currentUser.customer_id) {
        alert('❌ Error: Please ensure you are logged in to place an order.');
        return;
    }

    const orderItems = cart.map(item => ({
        item_id: item.id,
        quantity: item.qty,
        price: item.price
    }));

    try {
        const response = await fetch('http://127.0.0.1:5000/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                customer_id: currentUser.customer_id,
                items: orderItems
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Failed to place order');

        // Finalize the order locally for backup / UI display
        const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
        let placedOrder = null;
        
        // Ensure local list also updates with the real order ID
        if (data.order_id) {
           placedOrder = window.placeNewOrder(currentUser, total, cart, data.order_id);
        } else {
           placedOrder = window.placeNewOrder(currentUser, total, cart);
        }
        let orderId = placedOrder.id;

        // Clear cart & close modal
        closePaymentModal();
        cart = [];
        renderCart();

        const successModal = document.getElementById('order-success-modal');
        const successAnim = document.getElementById('success-animation-container');
        const successOrderId = document.getElementById('success-order-id');
        
        if (successModal && successAnim && successOrderId) {
            successOrderId.innerText = `#${orderId}`;
            successModal.style.display = 'flex';
            
            // Trigger animation
            setTimeout(() => {
                successAnim.style.opacity = '1';
                successAnim.style.transform = 'scale(1)';
            }, 50);
            
            // Auto close after 3 seconds and open tracking (optional)
            setTimeout(() => {
                successAnim.style.opacity = '0';
                successAnim.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    successModal.style.display = 'none';
                    renderOrdersList();
                }, 500);
            }, 3000);
        } else {
            // Fallback for missing DOM
            const methodLabels = { upi: 'UPI', card: 'Card', cash: 'Cash at Counter' };
            showToast(`💳 Payment via ${methodLabels[method.value]} confirmed!`);
            setTimeout(() => {
                showToast(`🎉 Order ${orderId} placed! We're preparing your food.`);
                renderOrdersList();
            }, 1500);
        }

    } catch (err) {
        console.error('Order Error:', err);
        alert('❌ Failed to place order. Please try again.');
    }
};

// Order Tracking UI
window.toggleOrdersList = function() {
    const modal = document.getElementById('orders-modal');
    if (modal.style.display === 'none') {
        modal.style.display = 'flex';
        renderOrdersList();
    } else {
        modal.style.display = 'none';
    }
}

function renderOrdersList() {
    const container = document.getElementById('orders-list');
    if (!container) return;
    
    const orders = window.getUserOrders(currentUser.email);
    if (orders.length === 0) {
        container.innerHTML = `<div style="text-align: center; padding: 2rem;"><i class="fa-solid fa-receipt" style="font-size: 3rem; color: var(--border); margin-bottom:1rem;"></i><p>No orders yet. Start craving!</p></div>`;
        return;
    }

    container.innerHTML = orders.map(order => {
        const statusColors = {
            'pending': '#f97316',
            'preparing': '#fbbf24',
            'ready': '#10b981',
            'delivered': '#78350f'
        };
        const statusIcons = {
            'pending': 'fa-clock',
            'preparing': 'fa-fire-burner',
            'ready': 'fa-bell',
            'delivered': 'fa-circle-check',
            'cancelled': 'fa-circle-xmark'
        };

        const orderTime = new Date(order.time);
        const canCancel = (new Date() - orderTime) / 60000 <= 1 && order.status !== 'delivered' && order.status !== 'cancelled';

        return `
            <div style="background: var(--background); border-radius: var(--radius-md); padding: 1rem; margin-bottom: 1rem; border-left: 5px solid ${statusColors[order.status]}; cursor: pointer; transition: all 0.2s;" onclick="const d = document.getElementById('bill-${order.id}'); d.style.display = d.style.display === 'none' ? 'block' : 'none';">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-weight: 700;">${order.id}</span>
                    <span style="font-size: 0.8rem; color: var(--text-muted);">${orderTime.toLocaleTimeString()}</span>
                </div>
                <div style="font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--text-muted);">
                    ${order.items.map(i => `${i.qty}x ${i.name}`).join(', ')}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                    <span style="font-weight: 600; color: var(--primary);">₹${order.total.toFixed(2)}</span>
                    <span style="background: ${statusColors[order.status]}20; color: ${statusColors[order.status]}; padding: 0.25rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 700;">
                        <i class="fa-solid ${statusIcons[order.status]}"></i> ${order.status.toUpperCase()}
                    </span>
                </div>
                ${order.status === 'pending' || order.status === 'preparing' ? 
                    `<div style="font-size: 0.8rem; color: var(--text-muted); margin-top:0.5rem;">
                        Estimated Prep Time: <strong>${order.prepTime || 10} minutes</strong>
                    </div>` : ''}

                <!-- Hidden Bill Section -->
                <div id="bill-${order.id}" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px dashed var(--border);">
                    <h4 style="font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--text);">Bill Details</h4>
                    <div style="font-size: 0.85rem; color: var(--text-muted); display: grid; gap: 0.25rem;">
                        ${order.items.map(i => `
                            <div style="display: flex; justify-content: space-between;">
                                <span>${i.name} x ${i.qty}</span>
                                <span>₹${(i.price * i.qty).toFixed(2)}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--border); font-weight: 700; font-size: 0.95rem; color: var(--text);">
                        <span>Grand Total</span>
                        <span>₹${order.total.toFixed(2)}</span>
                    </div>
                </div>

                ${canCancel ? 
                    `<button class="btn btn-outline" style="margin-top:1rem; width:100%; padding: 0.5rem; color: var(--danger); border-color: var(--danger);" onclick="event.stopPropagation(); handleCancelOrder('${order.id}')">
                        <i class="fa-solid fa-xmark"></i> Cancel Order
                    </button>` : ''}
                <div style="text-align: center; margin-top: 0.75rem;"><span style="font-size: 0.75rem; color: var(--text-muted);"><i class="fa-solid fa-chevron-down"></i> Click to view bill</span></div>
            </div>
        `;
    }).join('');
}

window.handleCancelOrder = function(orderId) {
    if (confirm("Are you sure you want to cancel this order?")) {
        if (window.cancelOrder(orderId)) {
            renderOrdersList();
            showToast("Order Cancelled!");
        }
    }
}

// Theme Toggle Logic
const themeToggles = document.querySelectorAll('#theme-toggle');

function setTheme(isDark) {
    if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }
    
    // Update all toggle icons
    themeToggles.forEach(toggle => {
        const icon = toggle.querySelector('i');
        if (icon) {
            if (isDark) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        }
    });
}

// Initialize theme
const savedTheme = localStorage.getItem('theme');
const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (savedTheme === 'dark' || (!savedTheme && systemDark)) {
    setTheme(true);
} else {
    setTheme(false);
}

// Add event listeners to all toggles
themeToggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        setTheme(!isDark);
    });
});

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    fetchCanteenHours();
    populateUserInfo();
    renderCart(); // Clear hardcoded stuff
});
