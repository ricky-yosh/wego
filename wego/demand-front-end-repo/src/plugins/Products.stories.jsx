// Products.stories.jsx
import React from 'react';
import Products from './Products';

export default {
    title: 'Components/Products',
    component: Products,
    // You can add decorators if needed, for example, to wrap the story in a router context
};

const Template = (args) => <Products {...args} />;

export const Default = Template.bind({});
// If your component takes props, you can define them in args here
