const API_BASE = "http://127.0.0.1:5000";

function fetchCart() {
    fetch(`${API_BASE}/cart/1`)
        .then(res => res.json())
        .then(renderCart)
        .catch(err => console.error(err));
}

function renderCart(items) {
    const container = document.getElementById('cartPageItems');
    container.innerHTML = items.map(i => `
        <div class="cart-item">
            <div>
                <h4>${i.name}</h4>
                <p>$${i.price} × ${i.quantity}</p>
            </div>
            <div>
                <button onclick="removeFromCart(${i.id})">🗑️</button>
            </div>
        </div>
    `).join('');
    const total = items.reduce((sum,i)=>sum+i.price*i.quantity,0);
    document.getElementById('cartPageTotal').textContent = total.toFixed(2);
}

function removeFromCart(itemId) {
    fetch(`${API_BASE}/cart/remove`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({user_id:1, item_id:itemId})
    }).then(fetchCart);
}

function checkout() {
    fetch(`${API_BASE}/checkout`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({user_id:1})
    }).then(() => { alert("Order placed!"); fetchCart(); });
}

document.addEventListener('DOMContentLoaded', fetchCart);
