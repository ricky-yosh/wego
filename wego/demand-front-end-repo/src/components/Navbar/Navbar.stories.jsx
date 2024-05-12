// Navbar.stories.jsx
import React from 'react';
import Navbar from './Navbar';
import { MemoryRouter } from 'react-router'; // MemoryRouter is used for Storybook to handle routing

export default {
    title: 'Components/Navbar',
    component: Navbar,
    decorators: [(Story) => (
        <MemoryRouter initialEntries={['/']}>
            <Story />
        </MemoryRouter>
    )],
};

const Template = (args) => <Navbar {...args} />;

export const Default = Template.bind({});
