import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('test.csv',usecols=['Price','Mountain_neutral_view','Current'])

# current = list(df.Current)
# price = list(df.Price)
# mountain = list(df.Mountain_neutral_view)

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div(className='wrapper',style={'height':'80vh'},children=[
    html.H1(children='Staggered Orders Overview'),
    html.H2(children='A mountain based visualisation of (base asset/quote asset)'),

    dcc.Input(id='input1', type='text'), #Price
    dcc.Input(id='input2', type='text'), #Order size
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-figure')

])

@app.callback(Output('output-figure','children'),
                    [Input('submit-button', 'n_clicks')],
                    [State('input1', 'value'),
                    State('input2', 'value')])

def update_figure(n_clicks, input1,input2):
    bar_background_colors_initial = []
    bar_background_colors_current = []

    initial_dict = {}
    current_dict = {}
    for x,y,z in zip(df.Price,df.Mountain_neutral_view,df.Current):
        initial_dict[round(x,3)]=y
        current_dict[round(x,3)]=z

    if input1 is not None: # NEEDS TO BE ADDED: if not input1 == ''
        input_price = float(input1)
        if input_price in list(initial_dict.keys()):
            # print(current_dict[float(input1)])
            current_dict[input_price] += float(input2)
            initial_dict[input_price] -= float(input2)
        else:
            print('error')

    for item in initial_dict:
        item = round(item,3)
        if item < 1:
            bar_background_colors_initial.append('rgba(58, 98, 87, 0.5)')
            bar_background_colors_current.append('rgba(51, 204, 51, 0.9)')
        else:
            if item == 1:
                bar_background_colors_initial.append('rgba(217,217,217,0.5)')
                bar_background_colors_current.append('rgba(242,242,242,0.9)')
            else:
                bar_background_colors_initial.append('rgba(230, 0, 0, 0.5)')
                bar_background_colors_current.append('rgba(255, 0, 0, 0.9)')

    print(list(current_dict.values()))

    data=[
        go.Bar(
            x=[i for i in range(len(list(df.Price)))], # length of the dict (len(dict))
            y=list(current_dict.values()), # all values from current_dict
            name='Buy',
            marker=go.bar.Marker(
                color=bar_background_colors_current
            )
        ),
        go.Bar(
            x=[i for i in range(len(list(df.Price)))], # length of the dict
            y=list(initial_dict.values()), # all values from mountain_dict
            name='Sell',
            marker=go.bar.Marker(
                color=bar_background_colors_initial
            )
        )
    ]
    #print(data)

    return dcc.Graph(
        id='my-figure',
        figure=go.Figure(
            data=data,
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
