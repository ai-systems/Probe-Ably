// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import React from "react";
import "react-datetime/css/react-datetime.css";
import Dashboard from "../pages/dashboard/DashboardOverview";
import "../scss/volt.scss";
import sampledata from './sample.json';

export default {
  title: "Dashboard",
  component: Dashboard,
};

const Template = (args) => <Dashboard {...args} />;

export const SingleTab = Template.bind({});

SingleTab.args = {
  aux_tasks: [
    {
      id: "1",
      name: "Task name 1",
      probings: [
        {
          model_name: "MLP",
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                    {
                      x: "boat",
                      y: 54,
                    },
                  ],
                },
              ],
            },
            {
              x_axis: "Number of Parameter",
              y_axis: "Selectivity",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 150,
                    },
                    {
                      x: "helicopter",
                      y: 200,
                    },
                    {
                      x: "boat",
                      y: 54,
                    },
                    {
                      x: "train",
                      y: 126,
                    },
                  ],
                },
                {
                  id: "china",
                  color: "hsl(12, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                    {
                      x: "boat",
                      y: 54,
                    },
                    {
                      x: "train",
                      y: 126,
                    },
                  ],
                },
              ],
            },
          ],
        },
        {
          model_name: "Linear",
          probing_types: [{ index: 0, name: "Accuracy" }],
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};

export const SingleTabValues = Template.bind({});

SingleTabValues.args = {
  aux_tasks: [
    {
      id: "1",
      name: "Task name 1",
      probings: [
        {
          model_name: "MLP",
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: 100000000,
                      y: 175,
                    },
                    {
                      x: 110000000,
                      y: 295,
                    },
                    {
                      x: 120000000,
                      y: 54,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};

export const MultipleTask = Template.bind({});

MultipleTask.args = {
  aux_tasks: [
    {
      id: "1",
      name: "Task name 1",
      probings: [
        {
          model_name: "MLP",
          probing_types: [
            { index: 0, name: "Accuracy" },
            { index: 1, name: "Selectivity" },
          ],
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                    {
                      x: "boat",
                      y: 54,
                    },
                  ],
                },
              ],
            },
            {
              x_axis: "Number of Parameter",
              y_axis: "Selectivity",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                    {
                      x: "boat",
                      y: 54,
                    },
                    {
                      x: "train",
                      y: 126,
                    },
                  ],
                },
              ],
            },
          ],
        },
        {
          model_name: "Linear",
          probing_types: [{ index: 0, name: "Accuracy" }],
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
    {
      id: "2",
      name: "Task name 2",
      probings: [
        {
          model_name: "MLP",
          probing_types: [
            { index: 0, name: "Accuracy" },
            { index: 1, name: "Selectivity" },
          ],
          probing_results: [
            {
              x_axis: "Number of Parameter",
              y_axis: "Accuracy",
              chart_data: [
                {
                  id: "japan",
                  color: "hsl(190, 70%, 50%)",
                  data: [
                    {
                      x: "plane",
                      y: 175,
                    },
                    {
                      x: "helicopter",
                      y: 295,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};



export const TaskFromJSON = Template.bind({});


TaskFromJSON.args = sampledata
