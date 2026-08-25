/* ============================================================
   mock.js — SAMPLE DATA FOR UI DEMONSTRATION ONLY.
   ------------------------------------------------------------
   Nothing here is saved anywhere. Nothing here talks to a server.
   This file exists so the screens have something to render before
   the backend is ready.

   When CONFIG.USE_MOCK is false, this file is never used.
   Do NOT add app logic here — data only.
   ============================================================ */

const MOCK = {

  // Returned by api.auth.login / api.auth.register while in mock mode.
  user: {
    id: 'demo-1',
    name: 'Demo User',
    email: 'demo@example.com',
    role: 'traveller',            // 'traveller' or 'host'
    verified: true,
    joined: '2026-01-14',
  },

  // Traveller's trips — api.trips.list()
  trips: [
    { id: 't1', title: 'Umngot river mornings',  city: 'Shnongpdeng, Meghalaya',
      host: 'Banri Nongrum',   date: '2026-11-08', guests: 2, status: 'confirmed', price: 2100 },
    { id: 't2', title: 'Kerala sadya',            city: 'Thrissur, Kerala',
      host: 'The Nair family', date: '2026-12-01', guests: 4, status: 'pending',   price: 2800 },
    { id: 't3', title: 'Chandni Chowk food crawl', city: 'Delhi',
      host: 'Vikram Malhotra', date: '2026-09-19', guests: 2, status: 'completed', price: 1200 },
  ],

  // Browsable destinations — api.destinations.list()
  destinations: [
    { id: 'd1', name: 'Shnongpdeng', state: 'Meghalaya',   experiences: 4, tag: 'River, clear-water season' },
    { id: 'd2', name: 'Munnar',      state: 'Kerala',      experiences: 3, tag: 'Tea slopes, shola forest' },
    { id: 'd3', name: 'Varanasi',    state: 'Uttar Pradesh', experiences: 6, tag: 'Ghats, dawn rituals' },
    { id: 'd4', name: 'Jaipur',      state: 'Rajasthan',   experiences: 5, tag: 'Block printing, havelis' },
    { id: 'd5', name: 'Thrissur',    state: 'Kerala',      experiences: 2, tag: 'Sadya, Onam traditions' },
  ],

  // Host's incoming booking requests — api.hosts.requests()
  hostRequests: [
    { id: 'r1', traveller: 'Sarah Johnson', from: 'Manchester, UK',    match: 94, guests: 2, date: '2026-09-07', status: 'pending' },
    { id: 'r2', traveller: 'Kiran Bhat',    from: 'Bengaluru, India',  match: 87, guests: 1, date: '2026-09-14', status: 'pending' },
    { id: 'r3', traveller: 'Oliver Chen',   from: 'Vancouver, Canada', match: 79, guests: 4, date: '2026-10-02', status: 'pending' },
  ],

  // Previously filed incident reports — api.safety.listReports()
  reports: [
    { id: 's1', type: 'Crowding',        location: 'Chandni Chowk, Delhi',
      date: '2026-08-02', severity: 'low',    status: 'reviewed', note: 'Very heavy crowd near the main lane after 7 PM.' },
    { id: 's2', type: 'Unsafe transport', location: 'Guwahati – Shillong road',
      date: '2026-07-21', severity: 'medium', status: 'open',     note: 'Shared cab driver refused seatbelts.' },
  ],

  // Emergency contacts — api.emergency.listContacts()
  contacts: [
    { id: 'c1', name: 'Aarti Sharma', relation: 'Sister', phone: '+91 98XXXXXX21', primary: true },
    { id: 'c2', name: 'Rohan Mehta',  relation: 'Friend', phone: '+91 97XXXXXX08', primary: false },
  ],

  // Public helplines shown on the emergency page.
  // VERIFY THESE with your team before the demo — do not present
  // unverified numbers to judges.
  helplines: [
    { name: 'National emergency number', number: '112' },
    { name: 'Tourist helpline (Ministry of Tourism)', number: '1363' },
    { name: 'Police', number: '100' },
    { name: 'Ambulance', number: '108' },
    { name: 'Women helpline', number: '1091' },
  ],
};
