const API_BASE = '/api';

/* ---------- Manejo de tokens en localStorage ---------- */
const Auth = {
  getAccess:  () => localStorage.getItem('access'),
  getRefresh: () => localStorage.getItem('refresh'),
  setTokens(access, refresh) {
    localStorage.setItem('access', access);
    if (refresh) localStorage.setItem('refresh', refresh);
  },
  clear() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  },
  isLoggedIn() { return !!localStorage.getItem('access'); },
};

/* ---------- Utilidades ---------- */
function esc(texto) {
  const d = document.createElement('div');
  d.textContent = texto ?? '';
  return d.innerHTML;
}

function estrellas(n) {
  return '★'.repeat(n) + '☆'.repeat(5 - n);
}

function mostrarErrores(err, contenedor) {
  let html = '';
  if (err && err.data && typeof err.data === 'object') {
    for (const [campo, msgs] of Object.entries(err.data)) {
      const lista = Array.isArray(msgs) ? msgs.join(' ') : msgs;
      html += `<div><strong>${esc(campo)}:</strong> ${esc(lista)}</div>`;
    }
  } else {
    html = esc(err.message || 'Ocurrió un error inesperado.');
  }
  contenedor.className = 'alert alert-danger';
  contenedor.innerHTML = html;
}

function llenarForm(form, datos) {
  for (const [k, v] of Object.entries(datos)) {
    const campo = form.elements[k];
    if (campo && campo.type !== 'file') campo.value = v ?? '';
  }
}

/* ---------- Renovar access con refresh ---------- */
async function refrescarToken() {
  const refresh = Auth.getRefresh();
  if (!refresh) return false;
  const res = await fetch(`${API_BASE}/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });
  if (!res.ok) return false;
  const data = await res.json();
  Auth.setTokens(data.access, data.refresh);
  return true;
}

/* ---------- Función central de peticiones ---------- */
async function apiFetch(path, { method = 'GET', body = null } = {}, reintento = true) {
  const headers = {};
  const esEscritura = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method);

  // Token solo en peticiones de escritura
  if (esEscritura && Auth.getAccess()) {
    headers['Authorization'] = `Bearer ${Auth.getAccess()}`;
  }

  // JSON si no es FormData (FormData fija su propio Content-Type)
  let payload = body;
  if (body && !(body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }

  const res = await fetch(`${API_BASE}${path}`, { method, headers, body: payload });

  if (res.status === 401 && esEscritura) {
    if (reintento && await refrescarToken()) {
      return apiFetch(path, { method, body }, false);
    }
    Auth.clear();
    window.location.href = '/login/';
    return null;
  }

  if (res.status === 204) return true;

  let data = null;
  try { data = await res.json(); } catch (_) {}

  if (!res.ok) {
    const error = new Error('Error en la petición');
    error.status = res.status;
    error.data = data;
    throw error;
  }
  return data;
}

/* ---------- Login ---------- */
async function login(username, password) {
  const res = await fetch(`${API_BASE}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Usuario o contraseña incorrectos.');
  const data = await res.json();
  Auth.setTokens(data.access, data.refresh);
}

function logout() {
  Auth.clear();
  window.location.href = '/login/';
}