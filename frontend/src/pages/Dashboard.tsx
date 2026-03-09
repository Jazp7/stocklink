// Dashboard.tsx — Application Summary View
import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="page">
      <header className="header">
        <h1>Dashboard</h1>
      </header>
      
      <div className="dashboard-grid">
        <p>Welcome to Stocklink! Here you can manage your products and providers.</p>
        {/* We will add summary cards here later */}
      </div>
    </div>
  );
};

export default Dashboard;
