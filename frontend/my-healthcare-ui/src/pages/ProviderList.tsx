// src/pages/ProviderList.tsx
import React, { useEffect, useState } from 'react';
import { getProviders } from '../api/providers';

interface Provider {
  id: number;
  name: string;
  specialty: string;
  email: string;
  phone: string;
}

const ProviderList: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProviders()
      .then((data) => {
        let arr: Provider[] = [];
        if (Array.isArray(data)) {
          arr = data.map((prov) => ({
            id: prov.id,
            name: prov.name,
            specialty: prov.specialty,
            email: prov.email ?? '',
            phone: prov.phone ?? '',
          }));
        } else if (data && Array.isArray((data as any).results)) {
          arr = ((data as { results: Provider[] }).results).map((prov) => ({
            id: prov.id,
            name: prov.name,
            specialty: prov.specialty,
            email: prov.email ?? '',
            phone: prov.phone ?? '',
          }));
        }
        setProviders(arr);
      })
      .catch((err) => {
        console.error('Error fetching providers:', err);
        setError('Failed to load providers.');
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <main role="main" className="flex-1 overflow-auto bg-app-bg p-6 main-content">
      <div className="dashboard-card">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-semibold text-card-fg">Providers</h1>
          <button className="flex items-center space-x-2 bg-btn-primary text-btn-primary hover:bg-btn-primary-hover px-3 py-1 rounded">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span className="text-sm">New Provider</span>
          </button>
        </div>

        {loading ? (
          <p className="text-muted">Loading providers…</p>
        ) : error ? (
          <p className="text-red-600">{error}</p>
        ) : providers.length === 0 ? (
          <p className="text-muted">No providers found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-card-bg divide-y divide-gray-200 table">
              <thead className="bg-app-bg">
                <tr>
                  <th className="px-4 py-2 text-left text-sm font-medium text-app-fg">ID</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-app-fg">Name</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-app-fg">Specialty</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-app-fg">Email</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-app-fg">Phone</th>
                  <th className="px-4 py-2 text-right text-sm font-medium text-app-fg">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {providers.map((prov) => (
                  <tr key={prov.id}>
                    <td className="px-4 py-2 text-sm text-card-fg">{prov.id}</td>
                    <td className="px-4 py-2 text-sm text-app-fg">{prov.name}</td>
                    <td className="px-4 py-2 text-sm text-muted">{prov.specialty}</td>
                    <td className="px-4 py-2 text-sm text-btn-primary">{prov.email}</td>
                    <td className="px-4 py-2 text-sm text-muted">{prov.phone}</td>
                    <td className="px-4 py-2 text-sm text-right space-x-2">
                      <button className="text-indigo-600 hover:underline text-sm">Edit</button>
                      <button className="text-red-600 hover:underline text-sm">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
};

export default ProviderList;
