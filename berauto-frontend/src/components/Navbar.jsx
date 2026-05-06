import { Link, NavLink, useNavigate } from 'react-router-dom';
import { CarFront, LogOut, Menu, UserRound } from 'lucide-react';
import { getUser, hasRole, logout } from '../utils/auth';

export default function Navbar() {
  const navigate = useNavigate();
  const user = getUser();
  const roles = user?.roles?.map((r) => r.name).join(', ') || 'Vendég';

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="topbar">
      <Link to="/" className="brand">
        <span className="brandIcon"><CarFront size={23} /></span>
        <span>BérAutó</span>
      </Link>

      <nav className="navlinks">
        <NavLink to="/">Autók</NavLink>
        {user && <NavLink to="/my-rentals">Bérléseim</NavLink>}
        {hasRole(['STAFF', 'ADMIN']) && <NavLink to="/staff">Ügyintézés</NavLink>}
        {hasRole(['ADMIN', 'STAFF']) && <NavLink to="/admin/cars">Autókezelés</NavLink>}
        {hasRole(['ADMIN']) && <NavLink to="/admin/users">Felhasználók</NavLink>}
      </nav>

      <div className="navUser">
        {user ? (
          <>
            <Link to="/profile" className="userPill"><UserRound size={16} /> {user.full_name} <small>{roles}</small></Link>
            <button className="ghostBtn" onClick={handleLogout}><LogOut size={16} /> Kilépés</button>
          </>
        ) : (
          <>
            <Link className="ghostBtn" to="/login">Belépés</Link>
            <Link className="primaryBtn" to="/register">Regisztráció</Link>
          </>
        )}
      </div>
      <Menu className="mobileOnly" />
    </header>
  );
}
