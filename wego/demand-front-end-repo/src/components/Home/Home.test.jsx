// Home.test.jsx

// Tests Originally created by ChatGPT
// Modified to fit the needs of Team12

import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import Home from './Home';
import { BrowserRouter } from 'react-router-dom'; // Required for handling navigation

// Helper function to wrap Home with BrowserRouter since it uses navigation
const renderWithRouter = (ui, { route = '/' } = {}) => {
    window.history.pushState({}, 'Test page', route);
    return render(ui, { wrapper: BrowserRouter });
};

test('renders Home component with welcome message, quote, and button', () => {
    renderWithRouter(<Home />);
    expect(screen.getByText('Welcome to WeGo!')).toBeInTheDocument();
    expect(screen.getByText(/redefine transportation/)).toBeInTheDocument(); // You can use regex for long text
    expect(screen.getByRole('button', { name: 'View Products' })).toBeInTheDocument();
});

test('renders an image with the correct src and alt attributes', () => {
    renderWithRouter(<Home />);
    const image = screen.getByRole('img', { name: 'Man Opening Box for WeGo Homepage' });
    expect(image).toHaveAttribute('src', '/happyman.png');
    expect(image).toHaveAttribute('alt', 'Man Opening Box for WeGo Homepage');
});