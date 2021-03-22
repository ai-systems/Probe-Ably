// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import React from "react";
import "react-datetime/css/react-datetime.css";
import ConfigurationForm from "../pages/forms/ConfigurationForm";
import "../scss/volt.scss";

export default {
  title: "ConfigurationForm",
  component: ConfigurationForm,
};

const Template = (args) => <ConfigurationForm {...args} />;

export const SimpleForm = Template.bind({});

SimpleForm.args = {};
