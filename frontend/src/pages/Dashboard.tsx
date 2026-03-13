// Dashboard.tsx — Application Summary View with larger icons
import React, { useEffect, useState } from 'react';
import { dashboardService } from '../services/dashboardService';
import type { DashboardStats } from '../services/dashboardService';
import { Users, Package, AlertTriangle, BadgeDollarSign, ArchiveX } from 'lucide-react';
import '../App.css';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await dashboardService.getStats();
      if (response.success) {
        setStats(response.data);
      } else {
        setError(response.error?.message || 'Failed to fetch statistics');
      }
    } catch (err) {
      setError('Error connecting to the server');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  if (loading) return <div className="loading-state"><p>Loading dashboard...</p></div>;
  if (error) return <div className="error-state"><p>{error}</p></div>;

  return (
    <div className="page">
      <header className="header">
        <h1>Dashboard Overview</h1>
      </header>
      
      <div className="dashboard-grid">
        {/* Total Products */}
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#eff6ff', color: '#3b82f6' }}>
            <Package size={32} />
          </div>
          <div className="stat-info">
            <span className="stat-label">Total Products</span>
            <span className="stat-value">{stats?.total_products}</span>
          </div>
        </div>

        {/* Total Providers */}
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#f0fdf4', color: '#22c55e' }}>
            <Users size={32} />
          </div>
          <div className="stat-info">
            <span className="stat-label">Active Providers</span>
            <span className="stat-value">{stats?.total_providers}</span>
          </div>
        </div>

        {/* Total Value */}
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#fefce8', color: '#eab308' }}>
            <BadgeDollarSign size={32} />
          </div>
          <div className="stat-info">
            <span className="stat-label">Inventory Value</span>
            <span className="stat-value">{formatCurrency(stats?.total_value || 0)}</span>
          </div>
        </div>

        {/* Low Stock */}
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#fff7ed', color: '#f97316' }}>
            <AlertTriangle size={32} />
          </div>
          <div className="stat-info">
            <span className="stat-label">Low Stock items</span>
            <span className="stat-value" style={{ color: stats?.low_stock && stats.low_stock > 0 ? '#f97316' : 'inherit' }}>
              {stats?.low_stock}
            </span>
          </div>
        </div>

        {/* Out of Stock */}
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#fef2f2', color: '#ef4444' }}>
            <ArchiveX size={32} />
          </div>
          <div className="stat-info">
            <span className="stat-label">Out of Stock</span>
            <span className="stat-value" style={{ color: stats?.out_of_stock && stats.out_of_stock > 0 ? '#ef4444' : 'inherit' }}>
              {stats?.out_of_stock}
            </span>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '2rem', padding: '2.5rem', background: 'white', borderRadius: '1.25rem', border: '1px solid #e2e8f0' }}>
        <h3 style={{ fontSize: '1.25rem' }}>Welcome back!</h3>
        <p style={{ color: '#64748b', marginTop: '0.75rem', fontSize: '1.1rem' }}>
          Here is a summary of your inventory. Use the sidebar to manage your products and providers.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
