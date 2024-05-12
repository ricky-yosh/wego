//Navbar.test.jsx

// Tests Originally created by ChatGPT
// Modified to fit the needs of Team12
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Navigation from '../Navbar/Navbar';
import { BrowserRouter } from 'react-router-dom'; // Required for handling navigation links

describe('Navigation Component', () => {
    test('renders Navigation with links and buttons', () => {
        render(
            <BrowserRouter>
                <Navigation />
            </BrowserRouter>
        );
        expect(screen.getByText(/home/i)).toBeInTheDocument();
        expect(screen.getByText(/about us/i)).toBeInTheDocument();
        expect(screen.getByText(/products/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
    });
});
