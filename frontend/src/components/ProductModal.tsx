// ProductModal.tsx — Modal with a form to add OR edit a product
import React, { useEffect, useState } from 'react';
import type { Product, ProductCreate } from '../types/productTypes';
import type { Provider } from '../types/providerTypes';
import { providerService } from '../services/providerService';

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (product: ProductCreate) => Promise<void>;
  initialData?: Product | null;
}

const ProductModal: React.FC<ProductModalProps> = ({ isOpen, onClose, onSave, initialData }) => {
  const [formData, setFormData] = useState<ProductCreate>({
    name: '',
    price: 0,
    stock_quantity: 0,
    category: '',
    provider_id: 0,
    description: ''
  });

  const [providers, setProviders] = useState<Provider[]>([]);

  useEffect(() => {
    if (isOpen) {
      if (initialData) {
        setFormData({
          name: initialData.name,
          price: initialData.price,
          stock_quantity: initialData.stock_quantity,
          category: initialData.category,
          // Use || 0 to handle null provider_id safely
          provider_id: initialData.provider_id || 0,
          description: initialData.description || ''
        });
      } else {
        setFormData({
          name: '',
          price: 0,
          stock_quantity: 0,
          category: '',
          provider_id: providers.length > 0 ? providers[0].id : 0,
          description: ''
        });
      }
      loadProviders();
    }
  }, [isOpen, initialData]);

  const loadProviders = async () => {
    try {
      const response = await providerService.getAll(1, 100); // Get more providers for the dropdown
      if (response.success) {
        setProviders(response.data);
        if (response.data.length > 0 && formData.provider_id === 0) {
          setFormData(prev => ({ ...prev, provider_id: response.data[0].id }));
        }
      }
    } catch (err) {
      console.error("Failed to load providers", err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave(formData);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{initialData ? 'Edit Product' : 'Add New Product'}</h2>
          <button className="btn-icon" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Product Name</label>
            <input 
              type="text" 
              className="form-control" 
              required
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Category</label>
            <input 
              type="text" 
              className="form-control" 
              required
              value={formData.category}
              onChange={e => setFormData({...formData, category: e.target.value})}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label>Price ($)</label>
              <input 
                type="number" 
                step="0.01"
                className="form-control" 
                required
                value={formData.price}
                onChange={e => setFormData({...formData, price: parseFloat(e.target.value)})}
              />
            </div>
            <div className="form-group">
              <label>Stock Quantity</label>
              <input 
                type="number" 
                className="form-control" 
                required
                value={formData.stock_quantity}
                onChange={e => setFormData({...formData, stock_quantity: parseInt(e.target.value)})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Provider</label>
            <select 
              className="form-control"
              required
              value={formData.provider_id}
              onChange={e => setFormData({...formData, provider_id: parseInt(e.target.value)})}
            >
              <option value="0" disabled={!initialData}>
                {initialData && !initialData.provider_id ? "No Provider (Select One)" : "Select a provider"}
              </option>
              {providers.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Description (Optional)</label>
            <textarea 
              className="form-control"
              rows={3}
              value={formData.description}
              onChange={e => setFormData({...formData, description: e.target.value})}
            ></textarea>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary">
              {initialData ? 'Update Product' : 'Save Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductModal;
