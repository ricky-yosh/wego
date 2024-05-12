// Login.test.jsx

// Tests Originally created by ChatGPT
// Modified to fit the needs of Team12
// Products.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Products from '../../components/Products/Products';

// Mock products data if it's not imported in this test file
const mockProducts = [
    { id: 1, title: 'Lifetime Drones', quote: 'Product 1 Quote', buttonLabel: 'View Product 1', location: '/product1' },
    { id: 2, title: 'Construction Wizard', quote: 'Product 2 Quote', buttonLabel: 'View Product 2', location: '/product2' },
    // Add more mock products if needed
];

describe('Products Component', () => {
    test('renders products with titles, quotes, and buttons', () => {
        render(<Products />); // Ensure Products component is imported correctly
        mockProducts.forEach(product => {
            expect(screen.getByText(product.title)).toBeInTheDocument();
            expect(screen.getByText(product.quote)).toBeInTheDocument();
            expect(screen.getByText(product.buttonLabel)).toBeInTheDocument();
        });
    });

    // You can add more tests here
});
