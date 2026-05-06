import { useEffect, useMemo, useState } from 'react';
import api from '../api/api';
import CarCard from '../components/CarCard';
import Loading from '../components/Loading';

export default function Cars() {
  const [cars, setCars] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/car/list').then((res) => setCars(res.data)).finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => cars.filter((c) => `${c.brand} ${c.model} ${c.license_plate}`.toLowerCase().includes(query.toLowerCase())), [cars, query]);

  if (loading) return <Loading />;

  return (
    <>
      <section className="hero">
        <div>
          <span className="eyebrow">BérAutó rendszer</span>
          <h1>Válassz autót, add le az igényt, a többit az ügyintéző kezeli.</h1>
          <p>A frontend a feltöltött Flask backend valódi endpointjaira van kötve.</p>
        </div>
        <div className="searchPanel">
          <label>Gyors keresés</label>
          <input placeholder="Márka, modell vagy rendszám..." value={query} onChange={(e) => setQuery(e.target.value)} />
        </div>
      </section>
      <div className="sectionHead"><h2>Autóállomány</h2><span>{filtered.length} db találat</span></div>
      <div className="carGrid">{filtered.map((car) => <CarCard key={car.id} car={car} />)}</div>
    </>
  );
}
