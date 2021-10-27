import plotly.graph_objects as go
import okcoin.DataMangement as dm
from okcoin import Account

acc = Account(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
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
