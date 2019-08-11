import sys
import threading

from dexbot.config import Config
from dexbot.controllers.main_controller import MainController
from dexbot.views.worker_list import MainView
from dexbot.controllers.wallet_controller import WalletController
from dexbot.views.unlock_wallet import UnlockWalletView
from dexbot.views.create_wallet import CreateWalletView
# Todo: Remove extra and order things around here
from bitshares.bitshares import Account
from dexbot.orderengines.bitshares_engine import BitsharesOrderEngine

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

from PyQt5.QtWidgets import QApplication
from bitshares import BitShares


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        config = Config()
        bitshares_instance = BitShares(config['node'], num_retries=-1, expiration=60)

        # Wallet unlock
        unlock_ctrl = WalletController(bitshares_instance)
        if unlock_ctrl.wallet_created():
            unlock_view = UnlockWalletView(unlock_ctrl)
        else:
            unlock_view = CreateWalletView(unlock_ctrl)

        if unlock_view.exec_():
            bitshares_instance = unlock_ctrl.bitshares
            self.main_ctrl = MainController(bitshares_instance, config)
            self.main_view = MainView(self.main_ctrl)
            self.main_view.show()
        else:
            sys.exit()


def main():
    app = App(sys.argv)
    sys.exit(app.exec_())


def server():
    """ Server to provide statistical visualization of a worker
    """
    # Fixme: Include this file in the project instead of loading from external source
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    dash_app.layout = html.Div(id='wrapper', style={'height': '80vh'}, children=[
        html.H1(children='Staggered Orders Overview'),
        html.H2(children='A mountain based visualisation of (base asset/quote asset)'),
        # Todo: Button's layout is inherited in some way because it looks good in browser
        html.Button(id='submit-button', n_clicks=0, children='Switch'),
        html.Div(id='output-graph'),

        # Represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False)

    ])

    @dash_app.callback(Output('output-graph', 'children'),
                       [Input('submit-button', 'n_clicks'),
                        Input('url','pathname')])
    def display_page(n_clicks,pathname):
        # get_account_list = get_account(pathname)
        # account,base_asset,quote_asset = get_account_list[0], get_account_list[1], get_account_list[2]

        # Todo: the if pathname part needs to be moved into another function but that causes errors
        if pathname:
            # Add readable spaces to worker name if there are any
            pathname = pathname.replace("%20", " ")

            # Split the path so that the names can be extracted
            pathname = pathname.split('/')

            account_name = pathname[1]
            worker_name = pathname[2]

            # Create Bitshares Account instance using the account name
            account = Account(account_name)

            # Todo: This config stuff needs to be adjusted
            config = Config()
            worker_config = config
            # print(worker_config.workers_data)

            worker_market = worker_config.workers_data[worker_name]['market']
            worker_market = worker_market.split('/')

            base_asset = worker_market[1]
            quote_asset = worker_market[0]


            price_list, buy_orders, sell_orders, current_orders, initial_orders, bar_colors_current, bar_colors_initial = get_orders(account,base_asset)

            # Get appropriate ticks
            ticks = [i for i in range(len(price_list))]
            text = [str(i) for i in price_list]

            if n_clicks is 0 or n_clicks % 2 == 0:
                figure_dict = {}
                data = [go.Bar(x=[i for i in range(len(price_list))],
                               y=list(current_orders.values()),name='Current',
                               marker=go.bar.Marker(color=bar_colors_current)),
                        go.Bar(x=[i for i in range(len(price_list))],
                               y=list(initial_orders.values()),name='Initial',
                               marker=go.bar.Marker(color=bar_colors_initial),
                               orientation='v')]
                figure_dict['data'] = data
                xaxis_dict = {'title':quote_asset + '/' + base_asset,
                              'zerolinecolor':'rgba(153,153,153,0.2)','tickvals':ticks,
                              'ticktext':text,'showticklabels':False}
                yaxis_dict = {'title':'Order size','gridcolor':'rgba(153,153,153,0.2)',
                              'range':[buy_orders[0],buy_orders[-1]]}
                figure = get_figure(figure_dict,xaxis_dict,yaxis_dict)

                return figure

            elif n_clicks % 2 != 0: # check whether the number of clicks isn't an even number, if so, horizontal view
                figure_dict = {}
                data = [go.Bar(x=list(current_orders.values()),
                               y=[i for i in range(len(price_list))],name='Current',
                               marker=go.bar.Marker(color=bar_colors_current)),
                        go.Bar(x=list(initial_orders.values()),
                               y=[i for i in range(len(price_list))],name='Initial',
                               marker=go.bar.Marker(color=bar_colors_initial),
                               orientation='h')]
                figure_dict['data'] = data
                xaxis_dict = {'title':quote_asset + '/' + base_asset,
                              'zerolinecolor':'rgba(153,153,153,0.2)','tickvals':ticks,
                              'ticktext':text,'showticklabels':False}
                yaxis_dict = {'title':'Order size','gridcolor':'rgba(153,153,153,0.2)',
                              'range':[buy_orders[0],buy_orders[-1]]}
                figure = get_figure(figure_dict,xaxis_dict,yaxis_dict)

                return figure


    def get_orders(account,base_asset):
        sell_prices = []
        buy_prices = []
        buy_orders = []
        sell_orders = []
        for order in account.openorders:
            if order['for_sale']['symbol'] == base_asset: # if the asset that you sell is equal to base asset, it's a buy order
                buy_prices.append(round(order['price'],3))
                buy_orders.append(float(order['base']['amount']*order['price']))
            else: # otherwise it's a sell order
                price = round(float(order['quote']['amount'])/float(order['base']['amount']),3)
                sell_prices.append(price)
                sell_orders.append(float(order['base']['amount']*order['price']))

        center_price = (buy_prices[0]+sell_prices[0])/2
        center_price = round(center_price,3)
        buy_prices.append(center_price) # adding non-existing center price

        price_list = sorted(buy_prices+sell_prices)

        # Todo: need to be a better way of determining a (non-existing) center order size -> market price?
        center_order_size = (buy_orders[0]+10)
        buy_orders.append(center_order_size) # adding non-existing center order size

        buy_orders = sorted(buy_orders)
        sell_orders = sorted(sell_orders, reverse=True)

        order_size = buy_orders+sell_orders

        initial_orders = {}
        current_orders = {}
        for x, y in zip(price_list, order_size):
            initial_orders[round(x, 3)] = y
            # current_dict[round(x, 3)] = z

        bar_colors_initial,bar_colors_current = get_colors(initial_orders,center_price)

        return price_list, buy_orders, sell_orders, current_orders, initial_orders, bar_colors_current, bar_colors_initial

    def get_colors(initial_orders,center_price):

        bar_colors_initial = []
        bar_colors_current = []

        for item in initial_orders:
            item = round(item, 3) # I believe this is rudimentary since you've already done it above
            if item < center_price:
                bar_colors_initial.append('rgba(58, 98, 87, 0.5)')
                # bar_colors_current.append('rgba(51, 204, 51, 0.9)')
            else:
                if item == center_price:
                    bar_colors_initial.append('rgba(217,217,217,0.5)')
                    # bar_colors_current.append('rgba(242,242,242,0.9)')
                else:
                    bar_colors_initial.append('rgba(230, 0, 0, 0.5)')
                    # bar_colors_current.append('rgba(255, 0, 0, 0.9)')
        return bar_colors_initial,bar_colors_current


    def get_figure(figure_dict,xaxis_dict,yaxis_dict):
        data = figure_dict['data']
        return dcc.Graph(
            id='my-figure',
            figure=go.Figure(
                data=data,
                layout=go.Layout(
                    autosize=True,
                    xaxis=xaxis_dict,
                    yaxis=yaxis_dict,
                    barmode='stack',
                    plot_bgcolor='rgb(21,43,42)',
                    paper_bgcolor='rgb(21,43,42)',
                    font={
                        'color': 'white'
                    },
                    showlegend=True
                )
            ),
            config={
                'displayModeBar': False
            },
            style={'height': '100%', 'width': '80vw', 'display': 'inline-block'}
        )

    dash_app.run_server()


# Run Dash app on separate thread
# Todo: This could be possibly improved by moving most of the Dash related stuff out of this file
server_thread = threading.Thread(target=server)
server_thread.daemon = True
server_thread.start()

if __name__ == '__main__':
    main()
