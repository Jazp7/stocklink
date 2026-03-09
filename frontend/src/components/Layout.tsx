// Layout.tsx — Final polished version with icons
import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, Users, Package, Boxes } from 'lucide-react';
import './Layout.css';

const Layout: React.FC = () => {
  return (
    <div className="layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="logo">
          <Boxes size={32} />
          <span style={{ marginLeft: '0.5rem' }}>Stocklink</span>
        </div>
        
        <nav className="nav-links">
          <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <LayoutDashboard size={20} style={{ marginRight: '0.75rem' }} />
            <span>Dashboard</span>
          </NavLink>
          
          <NavLink to="/providers" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Users size={20} style={{ marginRight: '0.75rem' }} />
            <span>Providers</span>
          </NavLink>
          
          <NavLink to="/products" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Package size={20} style={{ marginRight: '0.75rem' }} />
            <span>Products</span>
          </NavLink>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
