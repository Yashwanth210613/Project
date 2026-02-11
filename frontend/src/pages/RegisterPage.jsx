import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', password: '', role: 'patient' });
  const [error, setError] = useState('');
  const nav = useNavigate();
  const { login } = useAuth();

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post('/auth/register', form);
      login(data.access_token, data.role);
      nav(data.role === 'doctor' ? '/doctor' : '/patient');
    } catch {
      setError('Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form className="bg-white p-6 shadow rounded space-y-3 w-96" onSubmit={onSubmit}>
        <h1 className="text-xl font-bold">Register</h1>
        <input className="w-full border p-2" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="w-full border p-2" type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <select className="w-full border p-2" onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>
        {error && <p className="text-red-500">{error}</p>}
        <button className="bg-green-600 text-white w-full p-2">Create account</button>
      </form>
    </div>
  );
}
