/* ============================================================
   api.js — THE ONLY FILE THAT TALKS TO THE BACKEND.
   ------------------------------------------------------------
   No screen calls fetch() directly. Every screen calls a function
   from here. That way, when the endpoints change, one file changes.

   Endpoint paths below are PLACEHOLDERS marked TODO. Confirm each
   one with the backend teammate and edit only the path string —
   the rest of the code keeps working.
   ============================================================ */

/* ---------- low-level request helper ---------- */

async function request(path, options = {}) {
  const url = CONFIG.API_BASE_URL + path;

  // Cancel the request if the server takes too long.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), CONFIG.TIMEOUT_MS);

  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };

  // Attach the login token if we have one (FastAPI expects Bearer tokens).
  const token = Session.getToken();
  if (token) headers['Authorization'] = 'Bearer ' + token;

  try {
    const res = await fetch(url, { ...options, headers, signal: controller.signal });

    if (!res.ok) {
      // FastAPI usually sends errors as { "detail": "message" }
      let message = 'Request failed (' + res.status + ')';
      try {
        const body = await res.json();
        if (body.detail) message = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
      } catch (e) { /* response had no JSON body */ }
      throw new Error(message);
    }

    if (res.status === 204) return null;     // no content
    return await res.json();

  } catch (err) {
    if (err.name === 'AbortError') throw new Error('The server did not respond. Is the backend running?');
    if (err.message === 'Failed to fetch') throw new Error('Cannot reach the backend at ' + CONFIG.API_BASE_URL + '. Check it is running and CORS is enabled.');
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// Shorthands so the endpoint functions below stay short and readable.
const GET  = (p)       => request(p);
const POST = (p, body) => request(p, { method: 'POST',  body: JSON.stringify(body) });
const PUT  = (p, body) => request(p, { method: 'PUT',   body: JSON.stringify(body) });
const DEL  = (p)       => request(p, { method: 'DELETE' });

// Pretend network delay so mock mode feels like a real request
// (spinners and disabled buttons behave the same way).
const mockDelay = (data, ms = 500) =>
  new Promise(resolve => setTimeout(() => resolve(JSON.parse(JSON.stringify(data))), ms));


/* ============================================================
   ENDPOINTS
   Each function: if mock mode, return sample data.
   Otherwise, call the real backend.
   ============================================================ */

const api = {

  /* ---------- AUTHENTICATION ---------- */
  auth: {
    // TODO(backend): confirm path + body shape. FastAPI's OAuth2 form flow
    // may need form-encoded data instead of JSON — ask before wiring.
    async login({ email, password }) {
      if (CONFIG.USE_MOCK) {
        if (!email || !password) throw new Error('Enter your email and password.');
        return mockDelay({ token: 'mock-token', user: { ...MOCK.user, email } });
      }
      return POST('/auth/login', { email, password });
    },

    // TODO(backend): confirm path. Does register return a token, or must
    // the user log in afterwards?
    async register({ name, email, password, role }) {
      if (CONFIG.USE_MOCK) {
        return mockDelay({ token: 'mock-token', user: { ...MOCK.user, name, email, role } });
      }
      return POST('/auth/register', { name, email, password, role });
    },

    // TODO(backend): endpoint that returns the logged-in user from the token.
    async me() {
      if (CONFIG.USE_MOCK) return mockDelay(MOCK.user);
      return GET('/auth/me');
    },

    // TODO(backend): does logout need a server call, or is dropping the token enough?
    async logout() {
      if (CONFIG.USE_MOCK) return mockDelay(null, 100);
      return POST('/auth/logout', {});
    },
  },

  /* ---------- TRIPS / BOOKINGS ---------- */
  trips: {
    async list()            { if (CONFIG.USE_MOCK) return mockDelay(MOCK.trips);      return GET('/trips'); },              // TODO(backend)
    async get(id)           { if (CONFIG.USE_MOCK) return mockDelay(MOCK.trips.find(t => t.id === id)); return GET('/trips/' + id); }, // TODO(backend)
    async create(payload)   { if (CONFIG.USE_MOCK) return mockDelay({ ok: true, ...payload }); return POST('/trips', payload); },      // TODO(backend)
    async cancel(id)        { if (CONFIG.USE_MOCK) return mockDelay({ ok: true, id }); return DEL('/trips/' + id); },                  // TODO(backend)
  },

  /* ---------- DESTINATIONS / EXPERIENCES ---------- */
  destinations: {
    async list()            { if (CONFIG.USE_MOCK) return mockDelay(MOCK.destinations); return GET('/destinations'); },     // TODO(backend)
    async search(params)    {
      if (CONFIG.USE_MOCK) {
        const q = (params.q || '').toLowerCase();
        return mockDelay(MOCK.destinations.filter(d =>
          d.name.toLowerCase().includes(q) || d.state.toLowerCase().includes(q)));
      }
      return GET('/destinations?' + new URLSearchParams(params));   // TODO(backend): confirm query params
    },
  },

  /* ---------- HOST SIDE ---------- */
  hosts: {
    async requests()             { if (CONFIG.USE_MOCK) return mockDelay(MOCK.hostRequests); return GET('/host/requests'); },   // TODO(backend)
    async respond(id, accepted)  { if (CONFIG.USE_MOCK) return mockDelay({ ok: true, id, accepted }); return POST('/host/requests/' + id, { accepted }); }, // TODO(backend)
    async apply(payload)         { if (CONFIG.USE_MOCK) return mockDelay({ ok: true }); return POST('/host/apply', payload); }, // TODO(backend)
  },

  /* ---------- SAFETY / INCIDENT REPORTING ---------- */
  safety: {
    async listReports()      { if (CONFIG.USE_MOCK) return mockDelay(MOCK.reports); return GET('/safety/reports'); },        // TODO(backend)
    async submitReport(p)    { if (CONFIG.USE_MOCK) return mockDelay({ ok: true, id: 'mock', ...p }); return POST('/safety/reports', p); }, // TODO(backend)
    async checkIn(tripId)    { if (CONFIG.USE_MOCK) return mockDelay({ ok: true }); return POST('/safety/checkin', { tripId }); },          // TODO(backend)
  },

  /* ---------- EMERGENCY ---------- */
  emergency: {
    async listContacts() { 
      if (CONFIG.USE_MOCK) return mockDelay(MOCK.contacts); 
      const user = Session.getUser();
      const tourist_id = user ? user.id : 1;
      return GET('/emergency/contacts?tourist_id=' + tourist_id); 
    },

    async addContact(p) { 
      if (CONFIG.USE_MOCK) return mockDelay({ ok: true, id: 'mock', ...p }); 
      const user = Session.getUser();
      const tourist_id = user ? user.id : 1;
      return POST('/emergency/contacts', { ...p, tourist_id }); 
    },
    
    async removeContact(id) { 
      if (CONFIG.USE_MOCK) return mockDelay({ ok: true }); 
      return DEL('/emergency/contacts/' + id); 
    },
    // The most important call in the app. Ask the backend teammate what
    // this triggers server-side and what it returns.
    async sos({ lat, lng, note, tourist_id }) {
      if (CONFIG.USE_MOCK) return mockDelay({ ok: true, simulated: true });
      return POST('/emergency/sos', { lat, lng, note, tourist_id });
    },  

    async shareLocation({ lat, lng }) {
      if (CONFIG.USE_MOCK) return mockDelay({ ok: true, simulated: true });
      return POST('/emergency/location', { lat, lng });           // TODO(backend)
    },
  },
  /* ---------- IDENTITY (STAGE 2) ---------- */
  identity: {
    async create(payload) {
      if (CONFIG.USE_MOCK) {
        return mockDelay({ 
          id: 999, 
          display_name: payload.display_name || "Demo User",
          digital_id_code: "YS-2026-MOCK",
          interests: payload.interests || []
        });
      }
      return POST('/api/identity', payload);
    }
  },
};
