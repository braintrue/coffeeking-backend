const API_BASE = "";
const TOKEN_KEY = "ck_token";
const LOCATION_KEY = "ck_location_code";
const DEFAULT_LOCATION_CODE = "company-12f";

function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function saveLocationCode(code) {
  if (code) {
    localStorage.setItem(LOCATION_KEY, code);
  }
}

function getLocationCode() {
  return localStorage.getItem(LOCATION_KEY) || DEFAULT_LOCATION_CODE;
}

async function request(path, { method = "GET", body, auth = true, headers = {} } = {}) {
  const finalHeaders = { ...headers };

  if (body && !(body instanceof FormData)) {
    finalHeaders["Content-Type"] = "application/json";
  }

  if (auth) {
    const token = getToken();
    if (token) {
      finalHeaders["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: finalHeaders,
    body,
  });

  const contentType = response.headers.get("content-type");
  const data = contentType && contentType.includes("application/json") ? await response.json() : await response.text();

  if (!response.ok) {
    const message = data?.detail || data?.message || response.statusText;
    throw new Error(message);
  }

  return data;
}

async function register(email, password, fullName) {
  return request(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
        full_name: fullName,
      }),
      auth: false,
    },
  );
}

async function login(email, password) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  const data = await request("/auth/login", {
    method: "POST",
    body: params,
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    auth: false,
  });

  saveToken(data.access_token);
  return data;
}

async function me() {
  return request("/auth/me");
}

async function listTables(locationCode = getLocationCode()) {
  const params = new URLSearchParams();
  if (locationCode) {
    params.append("location_code", locationCode);
  }
  const query = params.toString() ? `?${params.toString()}` : "";
  return request(`/tables${query}`);
}

async function createTable({ name, capacity, tagline, locationCode = getLocationCode() }) {
  return request("/tables", {
    method: "POST",
    body: JSON.stringify({
      name,
      capacity: Number(capacity),
      tagline: tagline || null,
      location_code: locationCode,
    }),
  });
}

async function joinTable(tableId) {
  return request(`/tables/${tableId}/join`, {
    method: "POST",
  });
}

window.apiHelper = {
  saveToken,
  getToken,
  clearToken,
  saveLocationCode,
  getLocationCode,
  register,
  login,
  me,
  listTables,
  createTable,
  joinTable,
};
