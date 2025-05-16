'use client';
import { useState } from 'react';
import { Cat } from '@/types/cat';
import api from '@/lib/api';

export default function CatCard({ cat, onUpdated }: { cat: Cat, onUpdated: () => void }) {
  const [newSalary, setNewSalary] = useState(cat.salary);

  const updateSalary = async () => {
    await api.put(`/${cat.id}`, { salary: newSalary });
    onUpdated();
  };

  const deleteCat = async () => {
    await api.delete(`/${cat.id}`);
    onUpdated();
  };

  return (
    <div className="border p-4 rounded space-y-2">
      <h3 className="font-bold">{cat.name}</h3>
      <p>Breed: {cat.breed}</p>
      <p>Experience: {cat.years_experience}</p>
      <p>Salary: ${cat.salary}</p>

      <input type="number" value={newSalary} onChange={e => setNewSalary(Number(e.target.value))} className="border p-1 w-full" />
      <button onClick={updateSalary} className="bg-green-500 text-white px-2 py-1 rounded">Update Salary</button>
      <button onClick={deleteCat} className="bg-red-500 text-white px-2 py-1 rounded ml-2">Delete</button>
    </div>
  );
}
