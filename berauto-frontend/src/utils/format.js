export function money(value) {
  return new Intl.NumberFormat('hu-HU', { style: 'currency', currency: 'HUF', maximumFractionDigits: 0 }).format(Number(value || 0));
}

export function dateTime(value) {
  if (!value) return '-';
  return new Intl.DateTimeFormat('hu-HU', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));
}

export function toApiDateTime(value) {
  if (!value) return '';
  return new Date(value).toISOString();
}

export function statusLabel(status) {
  const map = { PENDING: 'Függőben', APPROVED: 'Jóváhagyva', REJECTED: 'Elutasítva', ACTIVE: 'Aktív', CLOSED: 'Lezárva' };
  return map[status] || status || '-';
}
