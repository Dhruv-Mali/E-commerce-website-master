// Enhanced cart functionality with loading states and no page reload

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function showLoading(button) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
}

function hideLoading(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

function updateCartUI(cartData) {
    // Update cart count in navbar
    const cartCount = document.querySelector('.cart-count');
    if (cartCount && cartData.cartItems !== undefined) {
        cartCount.textContent = cartData.cartItems;
    }
    
    // Update cart total
    const cartTotal = document.querySelector('.cart-total');
    if (cartTotal && cartData.total !== undefined) {
        cartTotal.textContent = `₹${cartData.total}`;
    }
}

var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(e) {
        e.preventDefault();
        
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var button = this;
        var originalText = button.innerHTML;
        
        console.log("ProductID:", productId, "Action:", action);

        if(user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            showLoading(button);
            updateUserOrderEnhanced(productId, action, button, originalText);
        }
    });
}

function addCookieItem(productId, action) {
    console.log("Guest user - updating cookie");

    if(action == 'add') {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if(cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    showToast('Cart updated successfully');
    
    setTimeout(() => location.reload(), 500);
}

function updateUserOrderEnhanced(productId, action, button, originalText) {
    var url = '/update-item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then((data) => {
        console.log('Success:', data);
        hideLoading(button, originalText);
        
        if (data.success) {
            showToast(data.message, 'success');
            
            // Update quantity display without reload
            const quantityElement = button.closest('.cart-item')?.querySelector('.quantity');
            if (quantityElement && data.quantity) {
                quantityElement.textContent = data.quantity;
            }
            
            // Reload only if item was removed
            if (data.message.includes('removed')) {
                setTimeout(() => location.reload(), 500);
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        hideLoading(button, originalText);
        showToast(error.error || 'An error occurred', 'danger');
    });
}

// Wishlist functionality
function toggleWishlist(productId, button) {
    showLoading(button);
    
    fetch('/wishlist/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'product_id': productId})
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(button, '<i class="bi bi-heart"></i>');
        showToast(data.message, 'success');
        button.classList.toggle('btn-danger');
        button.classList.toggle('btn-outline-danger');
    })
    .catch(error => {
        hideLoading(button, '<i class="bi bi-heart"></i>');
        showToast('Error updating wishlist', 'danger');
    });
}

// Image lazy loading
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Search autocomplete
const searchInput = document.querySelector('#search-input');
if (searchInput) {
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value;
        
        if (query.length < 2) return;
        
        searchTimeout = setTimeout(() => {
            fetch(`/api/search-suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Display suggestions (implement UI as needed)
                    console.log('Suggestions:', data);
                })
                .catch(error => console.error('Search error:', error));
        }, 300);
    });
}
