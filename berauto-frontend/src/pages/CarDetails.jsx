import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import api from '../api/api';
import Loading from '../components/Loading';
import { money, toApiDateTime } from '../utils/format';
import { getUser } from '../utils/auth';

function dateKey(date) {
  return date.toISOString().slice(0, 10);
}

function localDateKey(year, monthIndex, day) {
  const m = String(monthIndex + 1).padStart(2, '0');
  const d = String(day).padStart(2, '0');
  return `${year}-${m}-${d}`;
}

function expandBookedDays(rentals) {
  const days = new Set();
  rentals
    .filter((r) => !['REJECTED', 'CLOSED'].includes(r.status))
    .forEach((r) => {
      const start = new Date(r.start_time);
      const end = new Date(r.end_time);
      if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return;
      const cursor = new Date(start.getFullYear(), start.getMonth(), start.getDate());
      const last = new Date(end.getFullYear(), end.getMonth(), end.getDate());
      while (cursor <= last) {
        days.add(dateKey(cursor));
        cursor.setDate(cursor.getDate() + 1);
      }
    });
  return days;
}

export default function CarDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [car, setCar] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({ start_time: '', end_time: '' });
  const [calendarMonth, setCalendarMonth] = useState(() => new Date().toISOString().slice(0, 7));

  useEffect(() => {
    api.get(`/car/${id}`).then((res) => setCar(res.data));
    api.get(`/rental/car/${id}/booked`).then((res) => setBookings(res.data)).catch(() => setBookings([]));
  }, [id]);

  useEffect(() => {
    if (form.start_time) setCalendarMonth(form.start_time.slice(0, 7));
  }, [form.start_time]);

  const bookedDays = useMemo(() => expandBookedDays(bookings), [bookings]);

  const calendarDays = useMemo(() => {
    const [year, month] = calendarMonth.split('-').map(Number);
    const monthIndex = month - 1;
    const daysInMonth = new Date(year, month, 0).getDate();
    const firstDay = new Date(year, monthIndex, 1).getDay();
    const mondayBased = firstDay === 0 ? 6 : firstDay - 1;
    const result = [];
    for (let i = 0; i < mondayBased; i++) result.push(null);
    for (let d = 1; d <= daysInMonth; d++) {
      const key = localDateKey(year, monthIndex, d);
      result.push({ day: d, key, booked: bookedDays.has(key) });
    }
    return result;
  }, [calendarMonth, bookedDays]);

  async function rent(e) {
    e.preventDefault();
    if (!getUser()) return navigate('/login');
    setMessage('');
    try {
      await api.post('/rental/', {
        car_id: Number(id),
        start_time: toApiDateTime(form.start_time),
        end_time: toApiDateTime(form.end_time)
      });
      const res = await api.get(`/rental/car/${id}/booked`);
      setBookings(res.data);
      setMessage('Bérlési igény sikeresen leadva. Státusz: függőben.');
    } catch (err) {
      setMessage(err.response?.data?.message || 'Nem sikerült leadni az igényt.');
    }
  }

  if (!car) return <Loading />;

  return (
    <section className="detailsLayout">
      <div className="detailsCard">
        <Link to="/" className="backLink">← Vissza az autókhoz</Link>
        <div className="bigCarVisual"><span>{car.brand?.[0]}{car.model?.[0]}</span></div>
        <h1>{car.brand} {car.model}</h1>
        <p className="muted">Rendszám: {car.license_plate}</p>
        <div className="detailsGrid">
          <div><small>Évjárat</small><b>{car.year}</b></div>
          <div><small>Kilométer</small><b>{Number(car.mileage || 0).toLocaleString('hu-HU')} km</b></div>
          <div><small>Napidíj</small><b>{money(car.daily_price)}</b></div>
        </div>
      </div>
      <form className="rentCard" onSubmit={rent}>
        <h2>Bérlési igény</h2>
        <p className="muted">Add meg a bérlés kezdetét és végét. A piros napokon az autó már foglalt.</p>
        {message && <div className={`alert ${message.includes('sikeresen') ? 'success' : 'error'}`}>{message}</div>}
        <label>Kezdés</label>
        <input required type="datetime-local" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })} />
        <label>Befejezés</label>
        <input required type="datetime-local" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })} />

        <div className="bookingCalendarBox">
          <div className="between calendarTitle">
            <b>Foglaltsági naptár</b>
            <input type="month" value={calendarMonth} onChange={(e) => setCalendarMonth(e.target.value)} />
          </div>
          <div className="calendarWeekdays"><span>H</span><span>K</span><span>Sze</span><span>Cs</span><span>P</span><span>Szo</span><span>V</span></div>
          <div className="bookingCalendar">
            {calendarDays.map((item, index) => item ? (
              <div key={item.key} className={`calendarDay ${item.booked ? 'booked' : ''}`}>{item.day}</div>
            ) : <div key={`empty-${index}`} className="calendarDay emptyDay" />)}
          </div>
          <div className="calendarLegend"><span className="legendRed" /> már kiberelt / foglalt időszak</div>
        </div>

        <button className="primaryBtn wide">Igény leadása</button>
      </form>
    </section>
  );
}
