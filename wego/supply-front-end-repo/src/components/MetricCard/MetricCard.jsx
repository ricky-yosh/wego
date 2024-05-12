import React from 'react';
import './MetricCard.css';

const MetricCard = ({ title, value, icon }) => (
  <div className="metric-card">
    <div className="metric-icon">{icon}</div>
    <div className="metric-details">
      <p className="metric-value">{value}</p>
      <p className="metric-title">{title}</p>
    </div>
  </div>
);

export default MetricCard;
