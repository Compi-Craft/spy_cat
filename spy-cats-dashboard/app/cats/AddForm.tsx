'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { NewCat } from '@/types/cat';

export default function AddForm({ onAdded }: { onAdded: () => void }) {
  const [formData, setFormData] = useState<NewCat>({
    name: '',
    years_experience: 0,
    breed: '',
    salary: 0,
  });

  const [error, setError] = useState<string | string[] | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]:
        e.target.name === 'years_experience' || e.target.name === 'salary'
          ? parseInt(e.target.value)
          : e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    console.log(formData);
    try {
      await api.post('/', formData);
      onAdded();
      setFormData({
        name: '',
        years_experience: 0,
        breed: '',
        salary: 0,
      });
    } catch (err: any) {
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (Array.isArray(detail)) {
          const messages = detail.map((e: any) => (typeof e === 'string' ? e : e.msg));
          setError(messages);
        } else if (typeof detail === 'string') {
          setError(detail);
        } else {
          setError('Unexpected error');
        }
      } else {
        setError('Something went wrong');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 border p-4 rounded-lg">
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={formData.name}
        onChange={handleChange}
        className="w-full border p-2"
        required
      />
      <input
        type="number"
        name="years_experience"
        placeholder="Years of Experience"
        value={formData.years_experience}
        onChange={handleChange}
        className="w-full border p-2"
        required
      />
      <input
        type="text"
        name="breed"
        placeholder="Breed"
        value={formData.breed}
        onChange={handleChange}
        className="w-full border p-2"
        required
      />
      <input
        type="number"
        name="salary"
        placeholder="Salary"
        value={formData.salary}
        onChange={handleChange}
        className="w-full border p-2"
        required
      />

      {error && (
        <div className="text-red-500">
          {Array.isArray(error) ? (
            <ul className="list-disc pl-5 space-y-1">
              {error.map((msg, i) => (
                <li key={i}>{msg}</li>
              ))}
            </ul>
          ) : (
            <p>{error}</p>
          )}
        </div>
      )}

      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Add Cat
      </button>
    </form>
  );
}
