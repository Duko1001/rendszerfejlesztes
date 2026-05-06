import { useEffect, useState } from 'react';
import api from '../api/api';
import Loading from '../components/Loading';
import { saveSession, getUser } from '../utils/auth';

const empty = {
  full_name: '',
  email: '',
  phone: '',
  address: '',
  billing_name: '',
  country: '',
  zip_code: '',
  city: '',
  street: '',
  house_number: '',
  company_name: '',
  tax_number: '',
  id_card_number: '',
  driving_license_number: ''
};

export default function Profile() {
  const [form, setForm] = useState(empty);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    api.get('/user/me')
      .then((res) => setForm({ ...empty, ...res.data }))
      .catch(() => setForm({ ...empty, ...(getUser() || {}) }))
      .finally(() => setLoading(false));
  }, []);

  function change(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function save(e) {
    e.preventDefault();
    setMsg('');
    try {
      const res = await api.put('/user/me', form);
      const oldUser = getUser() || {};
      saveSession({ ...oldUser, ...res.data, token: oldUser.token });
      setForm({ ...empty, ...res.data });
      setMsg('Profiladatok sikeresen mentve.');
    } catch (err) {
      setMsg(err.response?.data?.message || 'A profil mentése sikertelen.');
    }
  }

  if (loading) return <Loading />;

  return (
    <section className="profileShell">
      <div className="sectionHead">
        <h1>Profil / Számlázási adatok</h1>
        <span>Profil módosítása</span>
      </div>

      {msg && <div className={`alert ${msg.includes('sikeresen') ? 'success' : 'error'}`}>{msg}</div>}

      <form className="profileForm" onSubmit={save}>
        <div className="profileBlock">
          <div className="profileRow wideInput"><label>Teljes név</label><input required value={form.full_name} onChange={(e) => change('full_name', e.target.value)} /></div>
          <div className="profileRow wideInput"><label>Email</label><input required type="email" value={form.email} onChange={(e) => change('email', e.target.value)} /></div>
          <div className="profileRow wideInput"><label>Telefon</label><input value={form.phone || ''} onChange={(e) => change('phone', e.target.value)} /></div>
          <div className="profileRow wideInput"><label>Lakcím</label><input value={form.address || ''} onChange={(e) => change('address', e.target.value)} /></div>
        </div>

        <div className="profileBlock twoCol">
          <div className="profileRow span2"><label>Számlázási név</label><input placeholder="Számlázási név" value={form.billing_name || ''} onChange={(e) => change('billing_name', e.target.value)} /></div>
          <div className="profileRow"><label>Ország</label><input placeholder="Ország" value={form.country || ''} onChange={(e) => change('country', e.target.value)} /></div>
          <div className="profileRow"><label>Irányítószám</label><input placeholder="Irányítószám" value={form.zip_code || ''} onChange={(e) => change('zip_code', e.target.value)} /></div>
          <div className="profileRow"><label>Város</label><input placeholder="Város" value={form.city || ''} onChange={(e) => change('city', e.target.value)} /></div>
          <div className="profileRow"><label>Utca</label><input placeholder="Utca" value={form.street || ''} onChange={(e) => change('street', e.target.value)} /></div>
          <div className="profileRow"><label>Házszám</label><input placeholder="Házszám" value={form.house_number || ''} onChange={(e) => change('house_number', e.target.value)} /></div>
        </div>

        <div className="profileBlock twoCol">
          <div className="profileRow span2"><label>Cégnév</label><input placeholder="Cégnév (opcionális)" value={form.company_name || ''} onChange={(e) => change('company_name', e.target.value)} /></div>
          <div className="profileRow"><label>Adószám</label><input placeholder="Adószám (opcionális)" value={form.tax_number || ''} onChange={(e) => change('tax_number', e.target.value)} /></div>
          <div className="profileRow"><label>Személyi</label><input placeholder="Személyi igazolvány szám (opcionális)" value={form.id_card_number || ''} onChange={(e) => change('id_card_number', e.target.value)} /></div>
          <div className="profileRow"><label>Jogosítvány</label><input placeholder="Jogosítvány szám (opcionális)" value={form.driving_license_number || ''} onChange={(e) => change('driving_license_number', e.target.value)} /></div>
        </div>

        <div className="actions profileActions"><button className="primaryBtn">Profiladatok mentése</button></div>
      </form>
    </section>
  );
}
