// setupTests.js
import "@testing-library/jest-dom";

jest.mock('./src/constants', () => ({
    API_BASE_URL: 'http://localhost:8000', // Mocked value for testing
    // Mock other constants as needed
}));