import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const nav = useNavigate();
  const { login } = useAuth();

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post('/auth/login', form);
      login(data.access_token, data.role);
      nav(data.role === 'doctor' ? '/doctor' : '/patient');
    } catch {
      setError('Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form className="bg-white p-6 shadow rounded space-y-3 w-96" onSubmit={onSubmit}>
        <h1 className="text-xl font-bold">Login</h1>
        <input className="w-full border p-2" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="w-full border p-2" type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        {error && <p className="text-red-500">{error}</p>}
        <button className="bg-blue-600 text-white w-full p-2">Login</button>
        <p className="text-sm">No account? <Link className="text-blue-600" to="/register">Register</Link></p>
      </form>
    </div>
  );
}
