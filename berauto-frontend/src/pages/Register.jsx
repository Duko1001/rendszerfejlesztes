import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: '', email: '', password: '' });
  const [error, setError] = useState('');

  async function submit(e) {
    e.preventDefault();
    setError('');
    try {
      await api.post('/user/register', form);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.message || 'Sikertelen regisztráció.');
    }
  }

  return (
    <section className="authShell single">
      <form className="authCard" onSubmit={submit}>
        <h2>Regisztráció</h2>
        {error && <div className="alert error">{error}</div>}
        <label>Teljes név</label>
        <input required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
        <label>Email</label>
        <input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <label>Jelszó</label>
        <input required type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <button className="primaryBtn wide">Fiók létrehozása</button>
        <p className="center muted">Van fiókod? <Link to="/login">Belépés</Link></p>
      </form>
    </section>
  );
}
