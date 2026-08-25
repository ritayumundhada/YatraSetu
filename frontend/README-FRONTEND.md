# YatraSetu — Frontend

Plain HTML, CSS and JavaScript. No build step, no npm install, no framework.

## Run it

You must use a local server. Opening the files by double-clicking (`file://`)
will break the map tiles and the shared JS files.

```bash
cd <project folder>
python3 -m http.server 5500
```

Then open **http://localhost:5500**

(Alternative: the "Live Server" extension in VS Code — right-click `index.html`
→ Open with Live Server.)

## Pages

| File | What it is |
|---|---|
| `index.html` | Public landing / explore page — the original prototype, plus the chatbot |
| `login.html` | Log in and register, with traveller/host role choice |
| `dashboard.html` | User dashboard — switches between traveller and host view |
| `trips.html` | My trips + browse destinations |
| `safety.html` | Incident reporting form, safety check-in, past reports |
| `emergency.html` | SOS, emergency contacts, helplines, live location map |

## Folders

```
index.html          ← original prototype (only nav links were added)
login.html
dashboard.html
trips.html
safety.html
emergency.html
css/app.css         ← styles for the new pages only
js/config.js        ← API URL and mock switch — EDIT THIS ONE
js/api.js           ← all backend calls live here
js/mock.js          ← sample data for the demo, clearly separated
js/session.js       ← login state + shared UI helpers
```

## Test it

1. Open `http://localhost:5500` — landing page should look unchanged.
2. Click **Log in** → enter any email and a 6+ character password → you land on the dashboard.
3. Dashboard → switch between **Traveller view** and **Host view**.
4. Host view → **Accept** a request → row updates in place.
5. Trips → **Browse destinations** → search "Kerala".
6. Safety → submit a report with an empty form (validation should block it), then fill it in.
7. Emergency → **Add contact**, then **SOS** (asks for confirmation, then shows a simulated notice).
8. Resize the window to phone width — nav wraps, grids stack.

While `USE_MOCK` is `true`, a yellow banner appears on every app page saying
nothing is saved. That is deliberate.

## Connecting the backend

One change:

```js
// js/config.js
API_BASE_URL: 'http://127.0.0.1:8000',   // your FastAPI address
USE_MOCK: false,                          // flip this
```

Then fix the endpoint paths in `js/api.js` — every one is marked `TODO(backend)`.
No other file needs editing.

FastAPI will also need CORS enabled, or the browser will block every request:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Rules for anyone editing this

- No screen calls `fetch()` directly. Add the call to `js/api.js` instead.
- Sample data goes in `js/mock.js` only. Never in a page.
- Nothing pretends to save data. If it is not saved, the UI says so.
