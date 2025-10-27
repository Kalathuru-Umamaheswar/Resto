console.log('main.js is loading...');

const API_BASE = "http://127.0.0.1:5000";
let cart = [];
let currentRestaurant = null;

// Load restaurants
function fetchRestaurants() {
    console.log('Fetching restaurants...');
    fetch(`${API_BASE}/restaurants`)
        .then(res => {
            console.log('Response status:', res.status);
            return res.json();
        })
        .then(data => {
            console.log('Received restaurants:', data);
            renderRestaurants(data);
        })
        .catch(err => {
            console.error('Error fetching restaurants:', err);
        });
}

function renderRestaurants(restaurants) {
    const grid = document.getElementById('restaurantsGrid');
    grid.innerHTML = restaurants.map(r => `
        <div class="restaurant-card" onclick="showRestaurant(${r.id})">
            <div class="restaurant-image" style="background-image:url('${r.image}')"></div>
            <div class="restaurant-info">
                <h3>${r.name}</h3>
                <div class="restaurant-badges">
                    <span class="badge">${r.cuisine}</span>
                    <span class="badge">⭐ ${r.rating}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function showRestaurant(id) {
    fetch(`${API_BASE}/restaurants/${id}/menu`)
        .then(res => res.json())
        .then(menu => renderMenu(menu, id))
        .catch(err => console.error(err));
}

function renderMenu(menu, restaurantId) {
    currentRestaurant = restaurantId;
    const content = document.getElementById('restaurantContent');
    content.innerHTML = `
        <div class="menu-grid">
            ${menu.map(i => `
                <div class="menu-item">
                    <div class="menu-item-image" style="background-image:url('${i.image}')"></div>
                    <div class="menu-item-details">
                        <h4>${i.name}</h4>
                        <p>${i.description}</p>
                        <p class="price-tag">$${i.price.toFixed(2)}</p>
                        <button onclick="addToCart(${i.id})">
                            <i class="fas fa-plus"></i> Add to Cart
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    showPage('restaurant');
}

function addToCart(itemId) {
    fetch(`${API_BASE}/cart/add`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user_id:1, item_id:itemId})
    }).then(() => alert("Added to cart!"))
      .catch(err => console.error(err));
}

// Page navigation
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId+'-page').classList.add('active');
}

// Initialize
console.log('Setting up DOMContentLoaded listener...');
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM is loaded, fetching restaurants...');
    fetchRestaurants();
});
