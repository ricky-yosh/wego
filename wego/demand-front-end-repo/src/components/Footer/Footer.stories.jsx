// Footer.stories.jsx
import React from 'react';
import Footer from './Footer';

export default {
    title: 'Components/Footer',
    component: Footer,
};

const Template = (args) => <Footer {...args} />;

export const Default = Template.bind({});
// You can add args here if your Footer component takes props
