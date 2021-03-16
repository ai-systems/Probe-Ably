// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import React from 'react';
import "react-datetime/css/react-datetime.css";
import Dashboard from '../pages/dashboard/DashboardOverview';
import "../scss/volt.scss";





export default {
    title: 'Dashboard',
    component: Dashboard,
};

const Template = (args) => <Dashboard />;

export const Primary = Template.bind({});


