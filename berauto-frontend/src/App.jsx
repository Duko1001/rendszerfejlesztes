import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Cars from './pages/Cars';
import CarDetails from './pages/CarDetails';
import Login from './pages/Login';
import Register from './pages/Register';
import MyRentals from './pages/MyRentals';
import StaffDashboard from './pages/StaffDashboard';
import AdminCars from './pages/AdminCars';
import AdminUsers from './pages/AdminUsers';
import Profile from './pages/Profile';

export default function App() {
  return (
    <>
      <Navbar />
      <main className="page">
        <Routes>
          <Route path="/" element={<Cars />} />
          <Route path="/cars/:id" element={<CarDetails />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<ProtectedRoute roles={['USER', 'ADMIN', 'STAFF']}><Profile /></ProtectedRoute>} />
          <Route path="/my-rentals" element={<ProtectedRoute roles={['USER', 'ADMIN', 'STAFF']}><MyRentals /></ProtectedRoute>} />
          <Route path="/staff" element={<ProtectedRoute roles={['STAFF', 'ADMIN']}><StaffDashboard /></ProtectedRoute>} />
          <Route path="/admin/cars" element={<ProtectedRoute roles={['ADMIN', 'STAFF']}><AdminCars /></ProtectedRoute>} />
          <Route path="/admin/users" element={<ProtectedRoute roles={['ADMIN']}><AdminUsers /></ProtectedRoute>} />
        </Routes>
      </main>
    </>
  );
}
