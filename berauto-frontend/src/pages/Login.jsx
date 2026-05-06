import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';
import { saveSession } from '../utils/auth';

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: 'customer@berauto.hu', password: 'hashed_pw' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      const res = await api.post('/user/login', form);
      saveSession(res.data);
      const roles = res.data.roles?.map((r) => r.name) || [];
      if (roles.includes('ADMIN')) navigate('/admin/cars');
      else if (roles.includes('STAFF')) navigate('/staff');
      else navigate('/');
    } catch (err) {
      setError(err.response?.data?.message || 'Sikertelen bejelentkezés.');
    } finally { setLoading(false); }
  }

  return (
    <section className="authShell">
      <div className="authInfo">
        <h1>Autóbérlés egyszerűen, áttekinthetően.</h1>
        <p>Jelentkezz be, adj le bérlési igényt, ügyintézőként kezeld a folyamatot, adminisztrátorként tartsd karban az autóállományt.</p>
        <div className="demoBox">
          <b>Teszt belépések az adatbázisból:</b>
          <span>admin@berauto.hu / hashed_pw</span>
          <span>staff@berauto.hu / hashed_pw</span>
          <span>customer@berauto.hu / hashed_pw</span>
        </div>
      </div>
      <form className="authCard" onSubmit={submit}>
        <h2>Belépés</h2>
        {error && <div className="alert error">{error}</div>}
        <label>Email</label>
        <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <label>Jelszó</label>
        <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <button className="primaryBtn wide" disabled={loading}>{loading ? 'Belépés...' : 'Belépés'}</button>
        <p className="center muted">Nincs fiókod? <Link to="/register">Regisztrálj</Link></p>
      </form>
    </section>
  );
}
