//SignUp.test.jsx

// Tests Originally created by ChatGPT
// Modified to fit the needs of Team12
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import SignUp from './SignUp';
import axios from 'axios';

jest.mock('axios');

describe('SignUp Component', () => {
    test('renders SignUp form with required fields', () => {
        render(<SignUp />);
        expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
        expect(screen.getByLabelText('Password')).toBeInTheDocument();
        expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
    });

    // Passwords do not match test. It should make a non-popup window alert.
    // test('displays error when passwords do not match', () => {
    //     render(<SignUp />);
    //     fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } });
    //     fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: 'different123' } });
    //     fireEvent.click(screen.getByRole('button', { name: /sign up/i }));
    //     expect(screen.getByText(/passwords don't match/i)).toBeInTheDocument();
    // });

    // Add more tests here as needed, such as form submission, axios mocking, etc.
});
