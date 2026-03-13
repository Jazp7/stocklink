// ProviderModal.tsx — Modal with a form to add OR edit a provider
import React, { useEffect, useState } from 'react';
import type { Provider, ProviderCreate } from '../types/providerTypes';

interface ProviderModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (provider: ProviderCreate) => Promise<void>;
  initialData?: Provider | null;
}

const ProviderModal: React.FC<ProviderModalProps> = ({ isOpen, onClose, onSave, initialData }) => {
  const [formData, setFormData] = useState<ProviderCreate>({
    name: '',
    email: '',
    phone: '',
    address: '',
    description: ''
  });

  useEffect(() => {
    if (isOpen) {
      if (initialData) {
        setFormData({
          name: initialData.name,
          email: initialData.email,
          phone: initialData.phone || '',
          address: initialData.address || '',
          description: initialData.description || ''
        });
      } else {
        setFormData({ name: '', email: '', phone: '', address: '', description: '' });
      }
    }
  }, [isOpen, initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave(formData);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{initialData ? 'Edit Provider' : 'Add New Provider'}</h2>
          <button className="btn-icon" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input 
              type="text" 
              className="form-control" 
              required
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input 
              type="email" 
              className="form-control" 
              required
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label>Phone (Optional)</label>
              <input 
                type="text" 
                className="form-control" 
                value={formData.phone || ''}
                onChange={e => setFormData({...formData, phone: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Address (Optional)</label>
              <input 
                type="text" 
                className="form-control" 
                value={formData.address || ''}
                onChange={e => setFormData({...formData, address: e.target.value})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Description (Optional)</label>
            <textarea 
              className="form-control"
              rows={3}
              value={formData.description || ''}
              onChange={e => setFormData({...formData, description: e.target.value})}
            ></textarea>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary">
               {initialData ? 'Update Provider' : 'Save Provider'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProviderModal;
