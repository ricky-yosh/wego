//Footer.test.jsx

// Tests Originally created by ChatGPT
// Modified to fit the needs of Team12a
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Footer from './Footer';

describe('Footer Component', () => {
    test('renders Footer with copyright text', () => {
        render(<Footer />);
        const footerElement = screen.getByText('Copyright © 2024 by WeGo. All rights reserved.');
        expect(footerElement).toBeInTheDocument();
    });
});
