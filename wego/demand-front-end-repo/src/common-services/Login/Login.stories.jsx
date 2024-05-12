// Login.stories.jsx
import React from 'react';
import Login from './Login';

export default {
    title: 'Common-Services/Login',
    component: Login,
    // Add decorators or parameters if needed
};

const Template = (args) => <Login {...args} />;

export const Default = Template.bind({});
Default.args = {
    // Define props here if your component accepts any
};
