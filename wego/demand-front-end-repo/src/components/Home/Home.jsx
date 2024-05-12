import React, { useContext, useEffect } from 'react';
import './Home.css';
import AuthContext from '../../utilities/AuthContext';

function Home() {
  const { user } = useContext(AuthContext);

  return (
    <div className="home-container">
      <div className="quote-section">
        <img src="/wego_logo.png" alt="WeGo Logo" className="wego-logo" />
        <h1>You Order, We Go</h1>
        <h2>Crafting Every Delivery with Punctuality, Comfort, and Care!</h2>
        {!!user ? <button onClick={() => window.location.href = '/products'} className="view-products-btn">View Products</button> : ""}
      </div>
      <div className="image-section">
        <img src="/happy_woman_wego.png" alt="Woman Hugging Box for WeGo Homepage" className="home-image" />
        </div>
    </div>
  );
}

export default Home;