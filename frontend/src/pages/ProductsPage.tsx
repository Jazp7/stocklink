// ProductsPage.tsx — Restoring CSS import
import React, { useEffect, useState } from 'react';
import { productService } from '../services/productService';
import type { Product, ProductCreate } from '../types/productTypes';
import ProductModal from '../components/ProductModal';
import '../App.css'; // This was missing!

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await productService.getAll();
      if (response.success) {
        setProducts(response.data);
      } else {
        setError(response.error?.message || 'Failed to fetch products');
      }
    } catch (err) {
      setError('An error occurred while connecting to the server.');
    } finally {
      setLoading(false);
    }
  };

  const openAddModal = () => {
    setEditingProduct(null);
    setIsModalOpen(true);
  };

  const openEditModal = (product: Product) => {
    setEditingProduct(product);
    setIsModalOpen(true);
  };

  const handleSave = async (productData: ProductCreate) => {
    try {
      let response;
      if (editingProduct) {
        response = await productService.update(editingProduct.id, productData);
      } else {
        response = await productService.create(productData);
      }

      if (response.success) {
        setIsModalOpen(false);
        fetchProducts();
      } else {
        alert(response.error?.message || 'Failed to save product');
      }
    } catch (err) {
      alert('Error connecting to the server.');
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) return;
    try {
      const response = await productService.delete(id);
      if (response.success) fetchProducts();
      else alert(response.error?.message || 'Failed to delete product');
    } catch (err) {
      alert('Error connecting to the server.');
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  };

  return (
    <div className="page">
      <header className="header">
        <h1>Products</h1>
        <button className="btn-primary" onClick={openAddModal}>Add Product</button>
      </header>
      {loading ? (
        <div className="loading-state"><p>Loading products...</p></div>
      ) : error ? (
        <div className="error-state">
          <p style={{ color: '#ef4444' }}>{error}</p>
          <button className="btn-primary" onClick={fetchProducts}>Try Again</button>
        </div>
      ) : (
        <div className="table-container">
          {products.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>No products found.</div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>#{product.id}</td>
                    <td style={{ fontWeight: '500' }}>{product.name}</td>
                    <td><span className="badge">{product.category}</span></td>
                    <td>{formatCurrency(product.price)}</td>
                    <td>{product.stock_quantity}</td>
                    <td>
                      <div className="actions">
                        <button className="btn-icon" title="Edit" onClick={() => openEditModal(product)}>✏️</button>
                        <button className="btn-icon" title="Delete" onClick={() => handleDelete(product.id, product.name)}>🗑️</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
      <ProductModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSave={handleSave}
        initialData={editingProduct}
      />
    </div>
  );
};

export default ProductsPage;
