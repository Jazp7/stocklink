// ProvidersPage.tsx — Manage Providers with Pagination
import React, { useEffect, useState } from 'react';
import { providerService } from '../services/providerService';
import type { Provider, ProviderCreate } from '../types/providerTypes';
import ProviderModal from '../components/ProviderModal';
import '../App.css';

const ProvidersPage: React.FC = () => {
  // 1. State
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const limit = 10;

  // Modal & Edit State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProvider, setEditingProvider] = useState<Provider | null>(null);

  // 2. Fetch Data
  useEffect(() => {
    fetchProviders();
  }, [currentPage]); // Re-fetch when page changes

  const fetchProviders = async () => {
    try {
      setLoading(true);
      const response = await providerService.getAll(currentPage, limit);
      if (response.success) {
        setProviders(response.data);
        if (response.pagination) {
          setTotalPages(response.pagination.total_pages);
          setTotalItems(response.pagination.total_items);
        }
      } else {
        setError(response.error?.message || 'Failed to fetch providers');
      }
    } catch (err) {
      setError('An error occurred while connecting to the server.');
    } finally {
      setLoading(false);
    }
  };

  const openAddModal = () => {
    setEditingProvider(null);
    setIsModalOpen(true);
  };

  const openEditModal = (provider: Provider) => {
    setEditingProvider(provider);
    setIsModalOpen(true);
  };

  const handleSave = async (providerData: ProviderCreate) => {
    try {
      let response;
      if (editingProvider) {
        response = await providerService.update(editingProvider.id, providerData);
      } else {
        response = await providerService.create(providerData);
      }

      if (response.success) {
        setIsModalOpen(false);
        fetchProviders();
      } else {
        alert(response.error?.message || 'Failed to save provider');
      }
    } catch (err) {
      alert('Error connecting to the server.');
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) return;
    try {
      const response = await providerService.delete(id);
      if (response.success) fetchProviders();
      else alert(response.error?.message || 'Failed to delete provider');
    } catch (err) {
      alert('Error connecting to the server.');
    }
  };

  return (
    <div className="page">
      <header className="header">
        <h1>Providers ({totalItems})</h1>
        <button className="btn-primary" onClick={openAddModal}>Add Provider</button>
      </header>

      {loading ? (
        <div className="loading-state"><p>Loading providers...</p></div>
      ) : error ? (
        <div className="error-state">
          <p style={{ color: '#ef4444' }}>{error}</p>
          <button className="btn-primary" onClick={fetchProviders}>Try Again</button>
        </div>
      ) : (
        <>
          <div className="table-container">
            {providers.length === 0 ? (
              <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>No providers found.</div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {providers.map((provider) => (
                    <tr key={provider.id}>
                      <td>#{provider.id}</td>
                      <td style={{ fontWeight: '500' }}>{provider.name}</td>
                      <td>{provider.email}</td>
                      <td>{provider.phone || 'N/A'}</td>
                      <td>
                        <div className="actions">
                          <button className="btn-icon" title="Edit" onClick={() => openEditModal(provider)}>✏️</button>
                          <button className="btn-icon" title="Delete" onClick={() => handleDelete(provider.id, provider.name)}>🗑️</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="pagination">
              <button 
                className="btn-secondary" 
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              >
                Previous
              </button>
              <span className="page-info">
                Page {currentPage} of {totalPages}
              </span>
              <button 
                className="btn-secondary" 
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      <ProviderModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSave={handleSave}
        initialData={editingProvider}
      />
    </div>
  );
};

export default ProvidersPage;
