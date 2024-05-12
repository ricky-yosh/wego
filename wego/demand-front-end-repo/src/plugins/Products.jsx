// import React from 'react';
import './Products.css';
import { useNavigate } from 'react-router-dom';

const products = [
  { id: 1, title: 'Lifetime Drones', image: '/LD-Dashboard.png', location: 'Lifetime_Drones/Home' },
  { id: 2, title: 'Construction Wizard', image: '/CW-Dashboard.png', location: 'Construction_Wizard/Home' },
  { id: 3, title: 'AgriConnect', image: '/Agriconnect-Dashboard.png', location: 'product3' },
  { id: 4, title: 'ClothExchange', image: '/path-to-images/clothexchange.jpg', location: 'product4' },
  { id: 5, title: 'Green Canopy', image: '/path-to-images/green-canopy.jpg', location: 'product5' },
  { id: 6, title: 'AutoTrash', image: '/path-to-images/autotrash.jpg', location: 'product6' },
  { id: 7, title: 'P2P', image: '/path-to-images/p2p.jpg', location: 'product7' },
  // Add other products similarly
];

function Products() {
  const navigate = useNavigate();

  return (
    <div className="products-grid">
      {products.map(product => (
        <div key={product.id} className="product" onClick={() => navigate(product.location)} style={{ backgroundImage: `url(${product.image})` }}>
          <div className="product-info">
            <h2>{product.title}</h2>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Products;