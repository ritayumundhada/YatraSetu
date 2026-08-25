/* ============================================================
   session.js — who is logged in, and shared page helpers.
   ------------------------------------------------------------
   The token is kept in sessionStorage so a page refresh does not
   log you out mid-demo. It clears when the browser tab closes.

   NOTE: while CONFIG.USE_MOCK is true the token is a fake string.
   No real authentication happens until the backend is connected.
   ============================================================ */

const Session = {
  getToken() { return sessionStorage.getItem('ys_token'); },

  getUser() {
    const raw = sessionStorage.getItem('ys_user');
    return raw ? JSON.parse(raw) : null;
  },

  save(token, user) {
    sessionStorage.setItem('ys_token', token || '');
    sessionStorage.setItem('ys_user', JSON.stringify(user || {}));
  },

  // Switch between traveller and host view.
  setRole(role) {
    const user = this.getUser();
    if (!user) return;
    user.role = role;
    sessionStorage.setItem('ys_user', JSON.stringify(user));
  },

  isLoggedIn() { return !!this.getToken(); },

  clear() {
    sessionStorage.removeItem('ys_token');
    sessionStorage.removeItem('ys_user');
  },

  // Put at the top of any page that needs a logged-in user.
  requireLogin() {
    if (!this.isLoggedIn()) {
      window.location.href = 'login.html?next=' + encodeURIComponent(location.pathname.split('/').pop());
      return false;
    }
    return true;
  },
};


/* ---------- shared UI helpers used by every new page ---------- */
const UI = {

  // Toast message, bottom centre.
  toast(message, type) {
    let el = document.getElementById('ys-toast');
    if (!el) {
      el = document.createElement('div');
      el.id = 'ys-toast';
      document.body.appendChild(el);
    }
    el.textContent = message;
    el.className = 'show ' + (type || '');
    clearTimeout(el._t);
    el._t = setTimeout(() => (el.className = ''), 3800);
  },

  // Yellow strip so nobody mistakes sample data for saved data.
  demoBanner() {
    if (!CONFIG.USE_MOCK) return;
    const b = document.createElement('div');
    b.className = 'demo-banner';
    b.innerHTML = 'Demo mode — showing sample data. Nothing is saved. '
                + 'Set <code>USE_MOCK: false</code> in js/config.js once the backend is running.';
    document.body.prepend(b);
  },

  // Shared header. `active` highlights the current page.
  header(active) {
    const user = Session.getUser();
    const links = [
      ['index.html',     'Explore'],
      ['trips.html',     'Trips'],
      ['dashboard.html', 'Dashboard'],
      ['safety.html',    'Safety'],
      ['emergency.html', 'Emergency'],
    ];
    return `
      <header class="app-nav">
        <a class="app-brand" href="index.html">${CONFIG.APP_NAME}</a>
        <nav>${links.map(([href, label]) =>
          `<a href="${href}" class="${active === href ? 'on' : ''}">${label}</a>`).join('')}</nav>
        <div class="app-nav-right">
          ${user
            ? `<span class="role-pill" id="rolePill">${user.role}</span>
               <button class="btn-ghost" onclick="UI.logout()">Log out</button>`
            : `<a class="btn-solid" href="login.html">Log in</a>`}
        </div>
      </header>`;
  },

  async logout() {
    try { await api.auth.logout(); } catch (e) { /* ignore — clearing locally anyway */ }
    Session.clear();
    window.location.href = 'login.html';
  },

  // Disable a button while a request is in flight.
  busy(button, isBusy, busyLabel) {
    if (!button) return;
    if (isBusy) {
      button.dataset.label = button.textContent;
      button.textContent = busyLabel || 'Working…';
      button.disabled = true;
    } else {
      button.textContent = button.dataset.label || button.textContent;
      button.disabled = false;
    }
  },

  // Standard error display so every screen fails the same way.
  error(container, err) {
    if (!container) return UI.toast(err.message, 'alert');
    container.innerHTML = `<div class="empty error">
      <strong>Could not load this.</strong><br>${err.message}</div>`;
  },
};
