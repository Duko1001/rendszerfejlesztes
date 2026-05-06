import { Link } from 'react-router-dom';
import { Gauge, Calendar, BadgeCheck } from 'lucide-react';
import { money } from '../utils/format';

export default function CarCard({ car }) {
  return (
    <article className="carCard">
      <div className="carVisual">
        <span>{car.brand?.slice(0, 1)}{car.model?.slice(0, 1)}</span>
      </div>
      <div className="cardBody">
        <div className="between">
          <h3>{car.brand} {car.model}</h3>
          <span className="badge ok"><BadgeCheck size={14} /> Elérhető</span>
        </div>
        <p className="muted plate">{car.license_plate}</p>
        <div className="specs">
          <span><Calendar size={16} /> {car.year}</span>
          <span><Gauge size={16} /> {Number(car.mileage || 0).toLocaleString('hu-HU')} km</span>
        </div>
        <div className="between bottomLine">
          <strong>{money(car.daily_price)} / nap</strong>
          <Link className="primaryBtn" to={`/cars/${car.id}`}>Részletek</Link>
        </div>
      </div>
    </article>
  );
}
