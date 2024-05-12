// Home.stories.jsx
import React from 'react';
import Home from './Home';

// This is the default export that defines the component and its title in the Storybook sidebar
export default {
    title: 'Components/Home',
    component: Home,
};

// Template for the Home story
const Template = (args) => <Home {...args} />;

// Default Home story
export const Default = Template.bind({});
Default.args = {
    // Define props here if your component takes any, to show in the controls panel and apply to your component
};
