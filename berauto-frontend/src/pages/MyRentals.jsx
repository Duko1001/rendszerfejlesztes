import { useEffect, useMemo, useState } from 'react';
import api from '../api/api';
import Loading from '../components/Loading';
import { dateTime, statusLabel } from '../utils/format';

export default function MyRentals() {
  const [rentals, setRentals] = useState([]);
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [rentalRes, carRes] = await Promise.all([api.get('/rental/my'), api.get('/car/list')]);
    setRentals(rentalRes.data); setCars(carRes.data); setLoading(false);
  }

  useEffect(() => { load().catch(() => setLoading(false)); }, []);

  const carMap = useMemo(() => Object.fromEntries(cars.map((c) => [c.id, c])), [cars]);
  if (loading) return <Loading />;

  return (
    <>
      <div className="sectionHead"><h1>Bérléseim</h1><span>{rentals.length} db</span></div>
      <div className="tableCard">
        <table>
          <thead><tr><th>Autó</th><th>Kezdés</th><th>Befejezés</th><th>Státusz</th></tr></thead>
          <tbody>
            {rentals.map((r) => {
              const car = carMap[r.car_id];
              return <tr key={r.id}><td>{car ? `${car.brand} ${car.model}` : `#${r.car_id}`}</td><td>{dateTime(r.start_time)}</td><td>{dateTime(r.end_time)}</td><td><span className={`status ${r.status}`}>{statusLabel(r.status)}</span></td></tr>;
            })}
            {!rentals.length && <tr><td colSpan="4" className="empty">Még nincs bérlési előzmény.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
