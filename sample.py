import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

df = pd.read_csv('test.csv',usecols=['Price','Mountain_neutral_view','Current'])

print(list(df.Price))
print(list(df.Mountain_neutral_view))
print(list(df.Current))

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

app.layout = html.Div(className='wrapper',style={'height':'80vh'},children=[
    html.H1(children='Staggered Orders Overview'),
    html.H2(children='A mountain based visualisation of (base asset/quote asset)'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Current),
                    name='Buy',
                    marker=go.bar.Marker(
                        color=bar_background_colors_current
                    )
                ),
                go.Bar(
                    x=[i for i in range(len(list(df.Price)))],
                    y=list(df.Mountain_neutral_view),
                    name='Sell',
                    marker=go.bar.Marker(
                        color=bar_background_colors_initial
                    )
                )
            ],
            layout=go.Layout(
                autosize=True,
                xaxis=dict(
                    title='BTS/USD',
                    zerolinecolor='rgba(153,153,153,0.2)'
                ),
                yaxis=dict(
                    title='Order size',
                    gridcolor='rgba(153,153,153,0.2)'
                ),
                barmode='stack',
                plot_bgcolor='rgb(21,43,42)',
                paper_bgcolor='rgb(21,43,42)',
                font={
                    'color':'white'
                }
            )
        ),
        style={'height':'100%','width':'60vw','display':'inline-block'}
    )
])

app.run_server(debug=True)
