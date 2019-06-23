import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('test.csv',usecols=['Price','Mountain_neutral_view','Current'])

bar_background_colors_initial = []
bar_background_colors_current = []

current = list(df.Current)
price = list(df.Price)
mountain = list(df.Mountain_neutral_view)

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div(className='wrapper',style={'height':'80vh'},children=[
    html.H1(children='Staggered Orders Overview'),
    html.H2(children='A mountain based visualisation of (base asset/quote asset)'),

    dcc.Input(id='input1', type='text',value=''),
    dcc.Input(id='input2', type='text',value=''),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-figure')

])

@app.callback(Output('output-figure','children'),
                    [Input('submit-button', 'n_clicks')],
                    [State('input1', 'value'),
                    State('input2', 'value')])

# VALUES ALSO GET SUBMITTED ON PAGE REFRESH: https://github.com/plotly/dash/issues/162
def update_figure(n_clicks, input1,input2):
    if not input1 == '': # This seems to partially prevent the above problem
        current.append(input1)
        mountain.append(input2)
    for i in price:
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
    print(current,mountain)

    return dcc.Graph(
        id='my-figure',
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[i for i in range(len(price))],
                    y=current,
                    name='Buy',
                    marker=go.bar.Marker(
                        color=bar_background_colors_current
                    )
                ),
                go.Bar(
                    x=[i for i in range(len(price))],
                    y=mountain,
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
if __name__ == '__main__':
    app.run_server(debug=True)
