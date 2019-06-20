import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

df = pd.read_csv('test.csv',usecols=['Price','Mountain_neutral_view','Current'])

# If you want to get an interval, so not all values on the x-axis, you need to
# say for example: range(9) and find the corresponding price for every value in that range

app.layout = html.Div(className='wrapper',children=[
    html.H1(children='Staggered Orders Overview'),
    html.H2(children='A mountain based visualisation of (base asset/quote asset)'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Mountain_neutral_view),
                    name='Initial',
                    marker=go.bar.Marker(
                        color='rgba(217,217,217,0.5)'
                    )
                ),
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Current),
                    name='Current',
                    marker=go.bar.Marker(
                        color='rgba(242,242,242,0.9)'
                    )
                )
            ],
            layout=go.Layout(
                xaxis={'title':'BTS/USD'},
                yaxis={'title':'Order size'},
                barmode='stack',
                plot_bgcolor='rgb(21,43,42)',
                paper_bgcolor='rgb(21,43,42)',
                font={
                    'color':'white'
                }
            )
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
