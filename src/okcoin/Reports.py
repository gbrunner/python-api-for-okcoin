import datetime
import pandas as pd
import plotly.graph_objects as go
import okcoin.DataMangement as dm
from okcoin import Fiat
from okcoin import Account
from okcoin import ticker

acc = Account(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
fiat = Fiat(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
azure_config = r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\azure.config"


def get_ledger_history():
    return dm.dataframe_from_azure_storage(azure_config)


def plot_stx_staking():
    df = get_ledger_history()
    chart = dm.plot_staking_history(df, 'BTC')
    chart.write_html('test.html', auto_open=True)


def plot_mia_staking():
    mia_df = get_mia_returns()
    fig = go.Figure(data=[go.Bar(x=mia_df['timestamp'], y=mia_df['amount'])])
    fig.update_layout(
        title='STX from MiamiCoin Staking',
        xaxis_title="Date",
        yaxis_title="Value in STX")
    fig.show()

    return mia_df


def plot_cumulative_mia_staking():
    mia_df = get_mia_returns()
    mia_df['cumsum'] = mia_df['amount'].cumsum()
    mia_df.drop_duplicates(keep='first', subset=['timestamp'], inplace=True)
    fig = go.Figure(data=[go.Bar(x=mia_df['timestamp'], y=mia_df['cumsum'])])
    fig.update_layout(
        title='Cumulative STX from MiamiCoin Staking',
        xaxis_title="Date",
        yaxis_title="Value in STX")
    fig.show()

    return mia_df


def get_mia_returns():
    df = get_ledger_history()
    return df[(df['amount']>0) & (df['amount']<26) & (df['currency']=='STX')]


def get_stx_returns():
    df = get_ledger_history()
    return df[df['currency'] == 'BTC']


def get_deposits(start_date=None, end_date=None, currency='USD'):
    if start_date == None:
        start_date = '2000-01-01'
    if end_date == None:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')

    dep = acc.get_deposit_history(currency)
    df = dep.df
    df['amount'] = pd.to_numeric(df['amount'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    mask = (df['updated_at'] > start_date) & (df['updated_at'] <= end_date)
    df = df.loc[mask]
    return df


def get_deposit_summary(start_date=None, end_date=None):
    return acc.get_total_deposit_value(start_date, end_date)

def purchase_history_chart():

    df = get_deposits()
    purchase_list = df['updated_at'].to_list()
    purchase_dict_list = []
    for purchase in purchase_list:

        purchase_dict_list.append(dict(
            x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
            line_width=2))

    asset = ticker.get_candlestick_chart('STX-USD', granularity=604800)
    chart = asset.as_chart()

    chart.update_layout(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        shapes=[dict(
            x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2016-12-09', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Increase Period Begins')]
    )