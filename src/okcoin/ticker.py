import pandas as pd
import requests

#from DataObjects import _Resp
#import DataObjects._Resp as _Resp
from okcoin.DataObjects import  _Candlestick

OKCOIN_URL = "https://www.okcoin.com"


def get_trading_pairs():
    r""" Returns snapshots of market data and is publicly
    accessible without account authentication. Retrieves
    list of trading pairs, trading limit, and unit increment.


    Returns
    -------
    trading_pairs : dict
        A dictionary of trading pairs available on Okcoin.

    Examples
    --------
    >>> from okcoin import ticker
    >>> trading_pairs = ticker.get_trading_pairs()
    >>> trading_pairs
       base_currency category  ... size_increment   tick_size
    0            BTC        1  ...         0.0001        0.01
    1            LTC        1  ...         0.0001        0.01
    2            ETH        1  ...         0.0001        0.01
    """
    request_path =  OKCOIN_URL + '/api/spot/v3/instruments'
    res = requests.get(request_path)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    else:
        return res


def get_order_book(trading_pair='BTC-USDT',
                   aggregation_depth=None):
    r""" Returns a trading pair's order book. Pagination is not
    supported here; the entire orderbook will be
    returned per request. This is publicly accessible
    without account authentication.

    Parameters
    ----------
    trading_pair : str
        The traiding pair you are interested in

    aggregation_depth : int
        Aggregation of orders within a price range


    Returns
    -------
    asks : dataframe
        The asking information from the order book

    bids : dataframe
        The bid information from the order book

    Examples
    --------
    >>> from okcoin import ticker
    >>> order_book = ticker.get_order_book('BTC-USD')
    >>> order_book[0]
        ask price ask size liquidated orders
    0    36417.66   0.0467                 1
    1    36419.84   0.0824                 1
    >>> order_book[1]
        bid price bid size liquidated orders
    0    36410.06     0.83                 1
    1    36407.01    0.055                 1
    """
    request_path = OKCOIN_URL + '/api/spot/v3/instruments/' + trading_pair.lower() + '/book'
    if aggregation_depth:
        body = {'depth': str(aggregation_depth)}
    else:
        body = ''

    res = requests.get(request_path, body)

    if res.status_code == 200:
        asks = pd.DataFrame(res.json()['asks'], columns=['ask price', 'ask size', 'liquidated orders'])
        bids = pd.DataFrame(res.json()['bids'], columns=['bid price', 'bid size', 'liquidated orders'])
    return asks, bids


def get_ticker():
    r""" Returns the latest price snapshot, best bid/ask price,
    and trading volume in the last 24 hours for all trading pairs.
    This is publicly accessible without account authentication.

    Returns
    -------
    tickers : _Resp
        A query response object that contains the query result as a dictionary and as a dataframe

    Examples
    --------
    >>> from okcoin import ticker
    >>> tick = ticker.get_ticker()
    >>> tick
    best_ask    best_bid  ...                 timestamp quote_volume_24h
    0     35736.87    35728.73  ...  2021-06-12T03:13:03.075Z     31677062.948
    1        156.2      155.99  ...  2021-06-12T03:13:03.006Z     1198588.8392
    2      2282.87     2280.84  ...  2021-06-12T03:13:03.079Z    12727166.5747
    """
    request_path = OKCOIN_URL + '/api/spot/v3/instruments/ticker'
    res = requests.get(request_path)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    else:
        return res


def get_trading_pair_info(trading_pair='BTC-USDT'):
    r""" Returns the latest price snapshot,
    best bid/ask price, and trading volume in the last 24
    hours for a particular trading pair.
    This is publicly accessible without account authentication.

    Parameters
    ----------
    trading_pair : str
        The trading pair you are interested in


    Returns
    -------
    trading_pair_info : _Resp
        A query response object that contains the query result as a dictionary and as a dataframe


    Examples
    --------
    >>> from okcoin import ticker
    >>> trading_pair_info = ticker.get_trading_pair_info('STX-BTC')
    >>> trading_pair_info
                                             0
    best_ask                           35782.9
    best_bid                           35753.1
    instrument_id                     BTC-USDT
    open_utc0                          37075.7
    open_utc8                          36806.5
    product_id                        BTC-USDT
    last                               35529.7
    last_qty                                 0
    ask                                35782.9
    best_ask_size                       0.0123
    bid                                35753.1
    best_bid_size                          0.2
    open_24h                           36771.7
    high_24h                           37448.9
    low_24h                              35525
    base_volume_24h                    13.1099
    timestamp         2021-06-12T03:14:03.036Z
    quote_volume_24h                  482993.2
    """
    request_path = OKCOIN_URL + '/api/spot/v3/instruments/' + trading_pair + '/ticker'
    res = requests.get(request_path)
    if res.status_code == 200:
        return pd.Series(res.json()).to_frame()
    else:
        return res


def get_latest_trades(trading_pair='STX-USD'):
    r""" Retrieve the latest 100 transactions of a
    trading pair.

    Parameters
    ----------
    trading_pair : str
        The trading pair you are interested in


    Returns
    -------
    latest_trades : _Resp
        A query response object that contains the query result as a dictionary and as a dataframe


    Examples
    --------
    >>> from okcoin import ticker
    >>> trades = ticker.get_latest_trades()
    >>> trades
                    time                 timestamp  ...                size  side
    0   2021-06-12T01:40:54.059Z  2021-06-12T01:40:54.059Z  ...  270.588235   buy
    1   2021-06-12T01:38:41.972Z  2021-06-12T01:38:41.972Z  ...        1000  sell
    """
    request_path = OKCOIN_URL + '/api/spot/v3/instruments/' + trading_pair + '/trades'
    res = requests.get(request_path)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    else:
        return res


def get_candlestick_chart(trading_pair='STX-USD', start=None, end=None, granularity=604800):
    r""" Returns the candlestick charts of the trading pairs.
    This API can retrieve the latest 1440 entries of data.
    Candlesticks are returned in groups based on
    requested granularity.
    Maximum of 1440 entries can be retrieved.

    Parameters
    ----------
    trading_pair : str
        The trading pair you are interested in


    Returns
    -------
    candlestick_chart : _Candlestick
        A candlestick chart

    Examples
    --------
    >>> from okcoin import ticker
    >>> candles = ticker.get_candlestick_chart('BTC-USD', granularity=604800)
    >>> candles.as_chart().write_html("test.html", auto_open = True)
    """
    request_path = OKCOIN_URL + '/api/spot/v3/instruments/' + trading_pair + '/candles'

    if start != None and end != None:
        body = {'start': str(start),
               'end':str(end),
               'granularity':str(granularity)}
    else:
        body = {
            'granularity': str(granularity)
        }

    res = _Candlestick(requests.get(request_path,params=body),trading_pair)

    if res.r.status_code ==200:
        res.df = pd.DataFrame(res.json, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

    return res


def get_granularity():
    r""" Returns a list of intervals that can be used to
    generating candlestick charts.


    Returns
    -------
    values : list
        A list of all possible granularity intervals

    Examples
    --------
    >>> from okcoin import ticker
    >>> ticker.get_granularity()
    """
    values = [60,180,300,900,1800,3600,7200,14400,21600,43200,86400,604800]
    return values
