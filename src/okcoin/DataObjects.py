import pandas as pd
import plotly.graph_objects as go


class _Resp:
    def __init__(self, r, trading_pair=None):
        try:
            if type(r.json())==dict:
                self.df = pd.Series(r.json()).to_frame()
            else:
                self.df = pd.DataFrame(r.json())
        except:
            self.df = None
        self.r = r
        self.json = r.json()
        self.trading_pair = trading_pair

    def as_df(self):
        return self.df

    def as_json(self):
        return self.json

    def as_chart(self):
        fig = go.Figure(data=[go.Candlestick(x=self.df['time'],
                open=self.df['open'],
                high=self.df['high'],
                low=self.df['low'],
                close=self.df['close'])])
        return fig


class _Candlestick(_Resp):
    #def __init__(self, trading_pair):
    #    self.trading_pair = trading_pair
    def as_chart(self):
        fig = go.Figure(data=[go.Candlestick(x=self.df['time'],
                open=self.df['open'],
                high=self.df['high'],
                low=self.df['low'],
                close=self.df['close'])])

        fig.update_layout(
            title=self.trading_pair,
            yaxis_title='Price of ' + self.trading_pair.replace('-',' in '))

        return fig


class _AccountInfo(_Resp):
    def chart(self, in_dollars=False):
        if in_dollars:
            pass
        else:
            fig = go.Figure([go.Bar(x=self.df['currency'].tolist(),
                                    y=self.df['balance'].tolist())])
            fig.update_layout(
                title='Account Assets',
                yaxis_title='Asset',
                xaxis_title='Quantity')
        return fig