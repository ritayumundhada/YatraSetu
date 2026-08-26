/* ============================================================
   config.js — one place to change app-wide settings.
   Edit this file, nothing else, when the backend goes live.
   ============================================================ */

const CONFIG = {

  // Display name. Change once here and it updates on every page.
  APP_NAME: 'YatraSetu',

  // Where the FastAPI backend lives.
  // Local FastAPI default is http://127.0.0.1:8000
  API_BASE_URL: 'http://127.0.0.1:8000',

  // MOCK MODE
  // true  = no backend needed. Screens show sample data from js/mock.js
  //         and a yellow "Demo mode" banner appears so nobody mistakes
  //         it for real saved data.
  // false = every call goes to API_BASE_URL. Flip this the day the
  //         backend teammate hands over working endpoints.
  USE_MOCK: false,

  // How long to wait for the API before giving up (milliseconds).
  TIMEOUT_MS: 8000,
};
