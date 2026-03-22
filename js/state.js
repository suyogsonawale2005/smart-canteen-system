// State initialization (Orders & Inventory)
function initState() {
    if (!localStorage.getItem('canteen_orders')) {
        localStorage.setItem('canteen_orders', JSON.stringify([]));
    }
    if (!localStorage.getItem('canteen_out_of_stock')) {
        localStorage.setItem('canteen_out_of_stock', JSON.stringify([]));
    }
}

// Generate sequential order ID
function generateOrderId() {
    const orders = JSON.parse(localStorage.getItem('canteen_orders') || '[]');
    return `ORD-${1000 + orders.length}`;
}

// Global Order Placer
window.placeNewOrder = function(user, cartTotal, items, orderIdNum) {
    const orders = JSON.parse(localStorage.getItem('canteen_orders') || '[]');
    const prepTime = Math.floor(Math.random() * 5) + 8; // Random 8-12 mins
    
    // Add prefix if it's coming purely locally, otherwise use actual DB order_id
    const finalId = orderIdNum ? `ORD-${orderIdNum}` : generateOrderId();
    
    const newOrder = {
        id: finalId,
        actualId: orderIdNum, // to map to backend id!
        userId: user.email,
        userName: user.name,
        userType: user.type,
        total: cartTotal,
        items: items, 
        status: 'pending',
        prepTime: prepTime,
        time: new Date().toISOString()
    };
    
    orders.push(newOrder);
    localStorage.setItem('canteen_orders', JSON.stringify(orders));
    return newOrder;
};

// Get orders for a specific user
window.getUserOrders = function(userEmail) {
    const orders = JSON.parse(localStorage.getItem('canteen_orders') || '[]');
    return orders.filter(o => o.userId === userEmail).sort((a,b) => new Date(b.time) - new Date(a.time));
}

// Global Out Of Stock Manager
window.isOutOfStock = function(itemName) {
    const oos = JSON.parse(localStorage.getItem('canteen_out_of_stock') || '[]');
    return oos.includes(itemName);
}

window.toggleOutOfStock = function(itemName) {
    let oos = JSON.parse(localStorage.getItem('canteen_out_of_stock') || '[]');
    if (oos.includes(itemName)) {
        oos = oos.filter(i => i !== itemName);
    } else {
        oos.push(itemName);
    }
    localStorage.setItem('canteen_out_of_stock', JSON.stringify(oos));
}

// Admin API
window.getAllOrders = function() {
    return JSON.parse(localStorage.getItem('canteen_orders') || '[]').sort((a,b) => new Date(b.time) - new Date(a.time));
}

window.updateOrderStatus = function(orderId, newStatus) {
    const orders = JSON.parse(localStorage.getItem('canteen_orders') || '[]');
    const index = orders.findIndex(o => o.id === orderId);
    if (index !== -1) {
        orders[index].status = newStatus;
        localStorage.setItem('canteen_orders', JSON.stringify(orders));
        
        // Update backend if it has an actual id
        if (orders[index].actualId) {
            fetch(`https://smart-canteen-system-hvah.onrender.com/api/orders/${orders[index].actualId}/status`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: newStatus })
            }).catch(e => console.error("Failed to sync status to backend", e));
        }
        
        return true;
    }
    return false;
}

window.cancelOrder = function(orderId) {
    const orders = JSON.parse(localStorage.getItem('canteen_orders') || '[]');
    const index = orders.findIndex(o => o.id === orderId);
    if (index !== -1) {
        const orderTime = new Date(orders[index].time);
        const now = new Date();
        const diffInMins = (now - orderTime) / 60000;
        
        if (diffInMins > 1) {
            alert('Too late to cancel! Order cancellation is only allowed within 1 minute of placing.');
            return false;
        }
        
        return window.updateOrderStatus(orderId, 'cancelled');
    }
    return false;
}

// ---- Menu CRUD API ----

window.getAdminMenu = function() {
    // Rely strictly on the globally fetched active menu from the Python DB API.
    return window.menuItems || [];
};

window.addMenuItem = async function(item) {
    try {
        const res = await fetch('https://smart-canteen-system-hvah.onrender.com/api/menu', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        });
        const data = await res.json();
        if (res.ok && data.item_id) {
            item.id = data.item_id;
        } else {
            console.error('Failed to add item to DB', data);
            item.id = Date.now();
        }
    } catch(err) {
        console.error('Error adding item to backend', err);
        item.id = Date.now();
    }
    const menu = window.getAdminMenu();
    menu.push(item);
    localStorage.setItem('canteen_menu', JSON.stringify(menu));
    window.menuItems = menu;
    return item;
};

window.updateMenuItem = async function(id, updates) {
    try {
        await fetch(`https://smart-canteen-system-hvah.onrender.com/api/menu/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
    } catch(err) {
        console.error('Error updating item in backend', err);
    }
    
    const menu = window.getAdminMenu();
    const idx = menu.findIndex(i => i.id === id);
    if (idx !== -1) {
        menu[idx] = { ...menu[idx], ...updates };
        localStorage.setItem('canteen_menu', JSON.stringify(menu));
        window.menuItems = menu;
        return true;
    }
    return false;
};

window.deleteMenuItem = async function(id) {
    try {
        await fetch(`https://smart-canteen-system-hvah.onrender.com/api/menu/${id}`, {
            method: 'DELETE'
        });
    } catch(err) {
        console.error('Error deleting item from backend', err);
    }
    let menu = window.getAdminMenu();
    menu = menu.filter(i => i.id !== id);
    localStorage.setItem('canteen_menu', JSON.stringify(menu));
    window.menuItems = menu;
};

initState();
