export function saveSession(user) {
  if (user?.token) localStorage.setItem('berauto_token', user.token);
  localStorage.setItem('berauto_user', JSON.stringify(user || {}));
}

export function getUser() {
  try { return JSON.parse(localStorage.getItem('berauto_user') || 'null'); }
  catch { return null; }
}

export function getRoles() {
  return getUser()?.roles?.map((r) => r.name) || [];
}

export function hasRole(roles) {
  const current = getRoles();
  return roles.some((role) => current.includes(role));
}

export function logout() {
  localStorage.removeItem('berauto_token');
  localStorage.removeItem('berauto_user');
}
