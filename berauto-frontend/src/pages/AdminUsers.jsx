import { useEffect, useState } from 'react';
import api from '../api/api';
import Loading from '../components/Loading';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [assign, setAssign] = useState({ user_id: '', role_id: '' });
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState('');

  async function load() {
    const [u, r] = await Promise.all([api.get('/user/list'), api.get('/user/roles')]);
    setUsers(u.data); setRoles(r.data); setLoading(false);
  }
  useEffect(() => { load().catch(() => setLoading(false)); }, []);

  async function addRole(e) {
    e.preventDefault(); setMsg('');
    try { await api.post('/user/roles/add', { user_id: Number(assign.user_id), role_id: Number(assign.role_id) }); setMsg('Szerepkör hozzáadva.'); await load(); }
    catch (err) { setMsg(err.response?.data?.message || 'Nem sikerült hozzáadni.'); }
  }

  if (loading) return <Loading />;
  return <>
    <div className="sectionHead"><h1>Felhasználók és jogosultságok</h1><span>Admin</span></div>
    {msg && <div className="alert info">{msg}</div>}
    <form className="adminForm compact" onSubmit={addRole}>
      <h2>Szerepkör hozzáadása</h2>
      <div className="formGrid"><select required value={assign.user_id} onChange={(e) => setAssign({ ...assign, user_id: e.target.value })}><option value="">Felhasználó...</option>{users.map((u) => <option key={u.id} value={u.id}>{u.full_name} | {u.email}</option>)}</select><select required value={assign.role_id} onChange={(e) => setAssign({ ...assign, role_id: e.target.value })}><option value="">Szerepkör...</option>{[{ id: 1, name: 'ADMIN' }, { id: 2, name: 'USER' }, { id: 3, name: 'STAFF' }].map((role) => <option key={role.id} value={role.id}>{role.name}</option>)}</select></div>
      <button className="primaryBtn">Hozzáadás</button>
    </form>
    <div className="tableCard"><table><thead><tr><th>ID</th><th>Név</th><th>Email</th><th>Szerepkörök</th></tr></thead><tbody>{users.map((u) => <tr key={u.id}><td>#{u.id}</td><td>{u.full_name}</td><td>{u.email}</td><td>{u.roles?.map((r) => r.name).join(', ')}</td></tr>)}</tbody></table></div>
  </>;
}
