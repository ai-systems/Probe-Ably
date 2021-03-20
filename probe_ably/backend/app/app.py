from flask import Flask

app = Flask(__name__)

@app.route('/')
def serve_data():
    return {
      'aux_tasks': [
        {
          'id': "1",
          'name': "Task name 1",
          'probings': [
            {
              'model_name': "MLP",
              'probing_results': [
                {
                  'x_axis': "Number of Parameter",
                  'y_axis': "Accuracy",
                  'chart_data': [
                    {
                      'id': "japan",
                      'color': "hsl(190, 70%, 50%)",
                      'data': [
                        {
                          'x': "plane",
                          'y': 175,
                        },
                        {
                          'x': "helicopter",
                          'y': 295,
                        },
                        {
                          'x': "boat",
                          'y': 54,
                        },
                      ],
                    },
                  ],
                },
                {
                  'x_axis': "Number of Parameter",
                  'y_axis': "Selectivity",
                  'chart_data': [
                    {
                      'id': "japan",
                      'color': "hsl(190, 70%, 50%)",
                      'data': [
                        {
                          'x': "plane",
                          'y': 175,
                        },
                        {
                          'x': "helicopter",
                          'y': 295,
                        },
                        {
                          'x': "boat",
                          'y': 54,
                        },
                        {
                          'x': "train",
                          'y': 126,
                        },
                      ],
                    },
                  ],
                },
              ],
            },
            {
              'model_name': "Linear",
              'probing_types': [{ 'index': 0, 'name': "Accuracy" }],
              'probing_results': [
                {
                  'x_axis': "Number of Parameter",
                  'y_axis': "Accuracy",
                  'chart_data': [
                    {
                      'id': "japan",
                      'color': "hsl(190, 70%, 50%)",
                      'data': [
                        {
                          'x': "plane",
                          'y': 175,
                        },
                        {
                          'x': "helicopter",
                          'y': 295,
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
    }
