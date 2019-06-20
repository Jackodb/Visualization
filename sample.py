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

bar_background_colors_initial = []
bar_background_colors_current = []

for i in df.Price:
    i = round(i,3)
    if i < 1:
        bar_background_colors_initial.append('rgba(58, 98, 87, 0.5)')
        bar_background_colors_current.append('rgba(51, 204, 51, 0.9)')
    else:
        if i == 1:
            bar_background_colors_initial.append('rgba(217,217,217,0.5)')
            bar_background_colors_current.append('rgba(242,242,242,0.9)')
        else:
            bar_background_colors_initial.append('rgba(230, 0, 0, 0.5)')
            bar_background_colors_current.append('rgba(255, 0, 0, 0.9)')

app.layout = html.Div(className='wrapper',children=[
    html.H1(children='Staggered Orders Overview'),
    html.H2(children='A mountain based visualisation of (base asset/quote asset)'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Current),
                    name='Current',
                    marker=go.bar.Marker(
                        color=bar_background_colors_current
                    )
                ),
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Mountain_neutral_view),
                    name='Initial',
                    marker=go.bar.Marker(
                        color=bar_background_colors_initial
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
