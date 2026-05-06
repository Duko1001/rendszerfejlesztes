import { useEffect, useMemo, useState } from 'react';
import api from '../api/api';
import Loading from '../components/Loading';
import { dateTime, money, statusLabel } from '../utils/format';

export default function StaffDashboard() {
  const [rentals, setRentals] = useState([]);
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState('');

  async function load() {
    const [rentalRes, carRes] = await Promise.all([api.get('/rental/'), api.get('/car/list')]);
    setRentals(rentalRes.data); setCars(carRes.data); setLoading(false);
  }
  useEffect(() => { load().catch(() => setLoading(false)); }, []);
  const carMap = useMemo(() => Object.fromEntries(cars.map((c) => [c.id, c])), [cars]);

  async function patch(id, action) {
    setMsg('');
    try {
      const res = await api.patch(`/rental/${id}/${action}`);
      setMsg(action === 'close' ? `Lezárva. Végösszeg: ${money(res.data.total)}` : 'Művelet sikeres.');
      await load();
    } catch (err) { setMsg(err.response?.data?.message || 'Művelet sikertelen.'); }
  }

  async function invoice(id) {
    setMsg('');
    try {
      const res = await api.get(`/invoice/rental/${id}`);
      setMsg(`Számla #${res.data.id}: ${money(res.data.amount)} | Fizetve: ${res.data.paid ? 'igen' : 'nem'}`);
    } catch (err) { setMsg(err.response?.data?.message || 'Ehhez a bérléshez még nincs számla.'); }
  }

  if (loading) return <Loading />;
  return (
    <>
      <div className="sectionHead"><h1>Ügyintézői dashboard</h1><span>{rentals.length} bérlés</span></div>
      {msg && <div className="alert info">{msg}</div>}
      <div className="tableCard">
        <table>
          <thead><tr><th>ID</th><th>Autó</th><th>Ügyfél ID</th><th>Időszak</th><th>Státusz</th><th>Műveletek</th></tr></thead>
          <tbody>
            {rentals.map((r) => {
              const car = carMap[r.car_id];
              return <tr key={r.id}>
                <td>#{r.id}</td><td>{car ? `${car.brand} ${car.model}` : `Autó #${r.car_id}`}</td><td>{r.user_id}</td>
                <td>{dateTime(r.start_time)}<br />{dateTime(r.end_time)}</td><td><span className={`status ${r.status}`}>{statusLabel(r.status)}</span></td>
                <td className="actions"><button onClick={() => patch(r.id, 'approve')}>Jóváhagy</button><button onClick={() => patch(r.id, 'reject')}>Elutasít</button><button onClick={() => patch(r.id, 'start')}>Átadás</button><button onClick={() => patch(r.id, 'close')}>Visszavétel + számla</button><button onClick={() => invoice(r.id)}>Számla</button></td>
              </tr>;
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
