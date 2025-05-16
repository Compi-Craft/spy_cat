'use client';
import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Cat } from '@/types/cat';
import AddForm from './AddForm';
import CatCard from './CatCard';

export default function CatsPage() {
  const [cats, setCats] = useState<Cat[]>([]);

  const loadCats = async () => {
    const res = await api.get('/');
    setCats(res.data);
  };

  useEffect(() => {
    loadCats();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">Spy Cats Dashboard</h1>
      <AddForm onAdded={loadCats} />
      <div className="space-y-4">
        {cats.map(cat => <CatCard key={cat.id} cat={cat} onUpdated={loadCats} />)}
      </div>
    </div>
  );
}
