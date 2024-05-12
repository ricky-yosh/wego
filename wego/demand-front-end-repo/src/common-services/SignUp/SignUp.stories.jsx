// SignUp.stories.jsx
import React from 'react';
import SignUp from './SignUp';

export default {
    title: 'Common-Services/SignUp',
    component: SignUp,
};

const Template = (args) => <SignUp {...args} />;

export const Default = Template.bind({});
// Define props here if your component accepts any, to show in the controls panel and apply to your component
