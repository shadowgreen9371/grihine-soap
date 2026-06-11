/* ==========================================================================
   GRIHINE SOAP — site behaviour
   Mobile menu · smooth scroll · cart counter · WhatsApp ordering · reveal
   ========================================================================== */

/* REPLACE: put the real WhatsApp number here (country code, no + or spaces) */
const WHATSAPP_NUMBER = '91XXXXXXXXXX';

/* ---------- Mobile hamburger menu ---------- */
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open);
  });

  // close the menu after tapping a link
  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ---------- Smooth scroll for same-page anchors ---------- */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const id = anchor.getAttribute('href');
    if (id.length > 1) {
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

/* ---------- Cart (persisted in localStorage) ---------- */
const CART_KEY = 'grihineCart';

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function updateCartBadge(bump = false) {
  const badge = document.getElementById('cartCount');
  if (!badge) return;
  const count = getCart().reduce((sum, item) => sum + item.qty, 0);
  badge.textContent = count;
  if (bump) {
    badge.classList.remove('bump');
    void badge.offsetWidth; // restart animation
    badge.classList.add('bump');
  }
}

function addToCart(name, price) {
  const cart = getCart();
  const existing = cart.find((item) => item.name === name);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ name, price, qty: 1 });
  }
  saveCart(cart);
  updateCartBadge(true);
  showToast(`🧺 ${name} added to cart`);
}

document.querySelectorAll('.add-cart').forEach((btn) => {
  btn.addEventListener('click', () => {
    addToCart(btn.dataset.name, Number(btn.dataset.price));
  });
});

/* Cart button → checkout via WhatsApp with the cart contents */
const cartBtn = document.getElementById('cartBtn');
if (cartBtn) {
  cartBtn.addEventListener('click', () => {
    const cart = getCart();
    if (cart.length === 0) {
      showToast('Your cart is empty — add a soap first! 🌿');
      return;
    }
    const lines = cart.map((item) => `• ${item.name} × ${item.qty} — ₹${item.price * item.qty}`);
    const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    const message =
      'Hello Grihine Soap! I\'d like to order:\n\n' +
      lines.join('\n') +
      `\n\nTotal: ₹${total}\n\nPlease share payment & delivery details.`;
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`, '_blank');
  });
}

/* ---------- Direct "Order on WhatsApp" buttons ---------- */
document.querySelectorAll('.wa-order').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const product = btn.dataset.product || 'your soaps';
    const message = `Hello Grihine Soap! I'm interested in: ${product}. Please share details.`;
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`, '_blank');
  });
});

/* ---------- Toast ---------- */
let toastTimer;
function showToast(text) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = text;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2600);
}

/* ---------- Scroll reveal ---------- */
const revealEls = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && revealEls.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  revealEls.forEach((el) => observer.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add('visible'));
}

/* ---------- Contact form → WhatsApp ---------- */
const orderForm = document.getElementById('orderForm');
if (orderForm) {
  orderForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(orderForm);
    const message =
      'Hello Grihine Soap! New order enquiry:\n\n' +
      `Name: ${data.get('name')}\n` +
      `Phone: ${data.get('phone')}\n` +
      `Product: ${data.get('product')}\n` +
      `Quantity: ${data.get('quantity') || '—'}\n\n` +
      `Message: ${data.get('message') || '—'}`;
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`, '_blank');
    showToast('Opening WhatsApp with your order… 💬');
    orderForm.reset();
  });
}

/* ---------- Init ---------- */
updateCartBadge();
