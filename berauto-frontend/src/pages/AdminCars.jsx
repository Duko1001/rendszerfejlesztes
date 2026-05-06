import { useEffect, useState } from 'react';
import api from '../api/api';
import Loading from '../components/Loading';
import { money } from '../utils/format';

const empty = { brand: '', model: '', year: new Date().getFullYear(), license_plate: '', daily_price: 10000, mileage: 0 };

export default function AdminCars() {
  const [cars, setCars] = useState([]);
  const [form, setForm] = useState(empty);
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState('');

  async function load() { const res = await api.get('/car/list'); setCars(res.data); setLoading(false); }
  useEffect(() => { load(); }, []);

  function edit(car) { setEditId(car.id); setForm({ brand: car.brand, model: car.model, year: car.year, license_plate: car.license_plate, daily_price: car.daily_price, mileage: car.mileage || 0 }); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  function reset() { setEditId(null); setForm(empty); }

  async function save(e) {
    e.preventDefault(); setMsg('');
    const payload = { ...form, year: Number(form.year), daily_price: Number(form.daily_price), mileage: Number(form.mileage) };
    try {
      if (editId) await api.put(`/car/update/${editId}`, payload); else await api.post('/car/add', payload);
      setMsg(editId ? 'Autó módosítva.' : 'Új bérelhető autó hozzáadva.'); reset(); await load();
    } catch (err) { setMsg(err.response?.data?.message || 'Mentés sikertelen.'); }
  }
  async function remove(id) { if (!confirm('Biztos törlöd?')) return; await api.delete(`/car/delete/${id}`); await load(); }

  if (loading) return <Loading />;
  return <>
    <div className="sectionHead"><h1>Autókezelés</h1><span>Admin / Staff</span></div>
    {msg && <div className="alert info">{msg}</div>}
    <form className="adminForm" onSubmit={save}>
      <h2>{editId ? `Autó módosítása #${editId}` : 'Új bérelhető autó felvitele'}</h2>
      <div className="formGrid"><input required placeholder="Márka" value={form.brand} onChange={(e) => setForm({ ...form, brand: e.target.value })} /><input required placeholder="Modell" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} /><input required placeholder="Évjárat" type="number" value={form.year} onChange={(e) => setForm({ ...form, year: e.target.value })} /><input required placeholder="Rendszám" value={form.license_plate} onChange={(e) => setForm({ ...form, license_plate: e.target.value })} /><input required placeholder="Napidíj" type="number" value={form.daily_price} onChange={(e) => setForm({ ...form, daily_price: e.target.value })} /><input placeholder="Kilométeróra" type="number" value={form.mileage} onChange={(e) => setForm({ ...form, mileage: e.target.value })} /></div>
      <div className="actions"><button className="primaryBtn">{editId ? 'Módosítás mentése' : 'Hozzáadás'}</button>{editId && <button type="button" onClick={reset}>Mégse</button>}</div>
    </form>
    <div className="tableCard"><table><thead><tr><th>ID</th><th>Autó</th><th>Rendszám</th><th>Km</th><th>Napidíj</th><th></th></tr></thead><tbody>{cars.map((c) => <tr key={c.id}><td>#{c.id}</td><td>{c.brand} {c.model} ({c.year})</td><td>{c.license_plate}</td><td>{Number(c.mileage || 0).toLocaleString('hu-HU')}</td><td>{money(c.daily_price)}</td><td className="actions"><button onClick={() => edit(c)}>Szerkeszt</button><button className="danger" onClick={() => remove(c.id)}>Töröl</button></td></tr>)}</tbody></table></div>
  </>;
}
