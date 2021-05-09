import requests
import getpass
import datetime
import hmac
import base64
import json
import pandas as pd
import configparser
import plotly.graph_objects as go

# import pandas as pd
# from datetime import datetime

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'
GET = 'GET'
POST = 'POST'
REST_API_URL = "https://www.okcoin.com"


class Signiture:
    def __init__(self, config_file='auth.config',
                 pass_phrase=None):

        config = configparser.ConfigParser()
        config.read(config_file)

        self.api_key = config['DEFAULT']['api_key']  # api_key
        self.secret_key = config['DEFAULT']['secret_key']  # secret_key
        self.REST_API_URL = REST_API_URL
        print("GetPass")
        print(config['DEFAULT']['pass_phrase'])
        if pass_phrase == None and config['DEFAULT']['pass_phrase'] == "":
            # print("HERE1")
            p = getpass.getpass(prompt='Enter your okcoin API pass phrase:')
            self.pass_phrase = p
        else:
            # print("HERE2")
            self.pass_phrase = config['DEFAULT']['pass_phrase']  # pass_phrase
        # self.query_result = query_result()

    def __get_timestamp(self):
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        print(timestamp)
        return timestamp

    # signature
    def __get_signature(self, t, method, request_path, body=None):
        if str(body) == '{}' or str(body) == 'None' or body == None:
            body = ''
        message = str(t) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'),
                       digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    # set request header
    def __get_header(self, sig, t):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = self.api_key
        header[OK_ACCESS_SIGN] = sig
        header[OK_ACCESS_TIMESTAMP] = t
        header[OK_ACCESS_PASSPHRASE] = self.pass_phrase
        return header

    def __parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'

        return url[0:-1]

    def query(self, type, request_path, body=''):
        # print(request_path)
        # print(type)
        # print(body)
        if body != '':
            body = self.__parse_params_to_str(body)

        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        # self.get_timestamp()
        print(body)
        signature = self.__get_signature(timestamp, type, request_path, body)
        # signature = self.__get_signature(timestamp, type, request_path, body)
        # signature = self.__get_signature(timestamp, type, request_path, '')

        header = self.__get_header(signature, timestamp)
        # do request
        response = requests.get(self.REST_API_URL + request_path + body,
                                headers=header)
        # data=body

        return response


class Account(Signiture):

    def get_account_type(self):
        # In Account API
        account_type = {
            'spot': 1,
            'margin': 5,
            'funding': 6
        }
        # return pd.DataFrame(account_type, index=[0])
        return account_type

    def get_withdrwal_status(self):
        # In Account API
        withdrawal_status = {
            'Pending cancel': -3,
            'Cancelled': -2,
            'Failed': -1,
            'Pending': 0,
            'Sending': 1,
            'Sent': 2,
            'Awaiting email verification': 3,
            'Awaiting manual verification': 4,
            'Awaiting identity verification': 5
        }
        # return pd.DataFrame(withdrawal_status, index=[0])
        return withdrawal_status

    def get_wallet(self):
        request_path = '/api/account/v3/wallet'
        body = ''
        return Resp(self.query(GET, request_path, body))

    def get_asset_valuation(self, currency='BTC'):
        request_path = '/api/account/v3/asset-valuation'
        p = {'valuation_currency': currency}
        body = json.dumps(p)
        return Resp(self.query(GET, request_path, body))

    # Sub account erroring
    def get_sub_account(self, account_name=None):
        request_path = '/api/account/v3/sub-account'
        if account_name:
            body = {'sub_account': account_name}
            # body = json.dumps(p)
        else:
            body = {'sub-account': ''}
            # body = json.dumps(p)
        return Resp(self.query(GET, request_path, body))

    def get_currency(self, token='BTC'):
        request_path = '/api/account/v3/wallet/' + token
        return Resp(self.query(GET, request_path))

    ## Withdraw or Trade Permission
    def get_funds_transfer(self):
        pass

    ## Withdraw or Trade Permission
    def withdrawal(self):
        pass

    def get_withdrawal_history(self, currency=None):
        if currency:
            request_path = '/api/account/v3/withdrawal/history/' + currency.lower()
        else:
            request_path = '/api/account/v3/withdrawal/history'
        return Resp(self.query(GET, request_path))

    def get_ledger(self):
        request_path = '/api/account/v3/ledger'
        return Resp(self.query(GET, request_path))

    def get_deposit_address(self, currency='BTC'):
        request_path = '/api/account/v3/deposit/address/' + currency.lower()
        return Resp(self.query(GET, request_path))

    def get_deposit_history(self, currency='usd'):
        request_path = '/api/account/v3/deposit/history/' + currency
        # p = {'currency': currency}
        # body = json.dumps(p)
        return Resp(self.query(GET, request_path))  # , body=body)

    def get_currencies(self):
        request_path = '/api/account/v3/currencies'
        return Resp(self.query(GET, request_path))

    # This is buggy. You need to specify a currency to get anything back
    def get_withdrawal_fees(self, currency='BTC'):
        request_path = '/api/account/v3/withdrawal/fee'
        if currency:
            body = {'currency': currency.lower()}
        else:
            body = ''
        # body = json.dumps(p)
        # print(body)
        return Resp(self.query(GET, request_path, body=body))

    def get_balance_from_ledger(self, df, currency='BTC'):
        cur = df[df['currency'] == currency]
        cur_balance = cur.groupby('timestamp')['balance'].max()
        balance = cur_balance.to_frame()
        balance.reset_index(inplace=True)

        fig = go.Figure(data=go.Scatter(
            x=balance.timestamp.tolist(),
            y=balance.balance.tolist(),
            mode='markers'
        ))

        fig.update_layout(
            title=currency,
            xaxis_title="Date",
            yaxis_title="Value in " + currency)

        return balance, fig


class Resp:
    def __init__(self, r, trading_pair=None):
        try:
            if type(r.json()) == dict:
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


class Candlestick(Resp):
    # def __init__(self, trading_pair):
    #    self.trading_pair = trading_pair
    def as_chart(self):
        fig = go.Figure(data=[go.Candlestick(x=self.df['time'],
                                             open=self.df['open'],
                                             high=self.df['high'],
                                             low=self.df['low'],
                                             close=self.df['close'])])

        fig.update_layout(
            title=self.trading_pair,
            yaxis_title='Price of ' + self.trading_pair.replace('-', ' in '))

        return fig


## Spot Trading Account Info
class Spot(Signiture):

    def get_order_status(self):
        # In Spot API
        order_status = {
            'Failed': -2,
            'Canceled': -1,
            'Open': 0,
            'Partially Filled': 1,
            'Fully Filled': 2,
            'Submitting': 3,
            'Cancelling': 4,
            'Incomplete': 6,
            'Complete': 7
        }
        # return pd.DataFrame(order_status, index=[0])
        return order_status

    def get_accounts(self, currency=None):
        request_path = '/api/spot/v3/accounts'
        if currency:
            request_path += "/" + currency.lower()
        return Resp(self.query(GET, request_path))

    def get_ledger(self, currency='BTC'):
        request_path = '/api/spot/v3/accounts'
        request_path += "/" + currency.lower() + "/ledger"
        return Resp(self.query(GET, request_path))

    def place_order(self):
        pass

    def get_order_list(self, trading_pair='BTC-USDT', state=7):
        request_path = '/api/spot/v3/orders'  # ?instrument_id='+trading_pair+'&state='+str(state)
        # Using the "body" doesn't work
        body = {'instrument_id': 'BTC-USDT',
                'state': '7'}
        return Resp(self.query(GET, request_path, body=body))

    def get_orders_pending(self, trading_pair='BTC-USDT'):
        request_path = '/api/spot/v3/orders_pending'
        body = {'instrument_id': trading_pair.lower()}
        return Resp(self.query(GET, request_path, body=body))

    def get_order_details(self, order_id, trading_pair='BTC-USDT'):
        request_path = '/api/spot/v3/orders/' + str(order_id)
        body = {'instrument_id': trading_pair.lower()}
        return Resp(self.query(GET, request_path, body=body))

    def get_trade_fee(self):
        request_path = '/api/spot/v3/trade_fee'
        return Resp(self.query(GET, request_path))

    def get_filled_orders(self, trading_pair='BTC-USDT'):
        request_path = '/api/spot/v3/fills'
        body = {'instrument_id': trading_pair.lower()}
        return Resp(self.query(GET, request_path, body=body))

    def get_trading_pairs(self):
        request_path = '/api/spot/v3/instruments'
        return Resp(self.query(GET, request_path))

    def get_order_book(self, trading_pair='BTC-USDT', aggregation_depth=None):
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/book'
        if aggregation_depth:
            body = {'depth': str(aggregation_depth)}
        else:
            body = ''

        res = Resp(self.query(GET, request_path, body=body))

        if res.r.status_code == 200:
            asks = pd.DataFrame(res.json['asks'], columns=['ask price', 'ask size', 'liquidated orders'])
            bids = pd.DataFrame(res.json['bids'], columns=['bid price', 'bid size', 'liquidated orders'])
        return asks, bids

    def get_ticker(self):
        request_path = '/api/spot/v3/instruments/ticker'
        return Resp(self.query(GET, request_path))

    def get_trading_pair_info(self, trading_pair='BTC-USDT'):
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/ticker'
        return Resp(self.query(GET, request_path))

    def get_latest_trades(self, trading_pair='STX-USD'):
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/trades'
        return Resp(self.query(GET, request_path))

    # granularity=86400&start=2019-03-19T16:00:00.000Z&end=2019-03-19T16:00:00.000Z
    def get_candlestick_chart(self, trading_pair='STX-USD', start='', end='', granularity=None):
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/candles'

        body = {'start': str(start),
                'end': str(end),
                'granularity': str(granularity)}

        res = Candlestick(self.query(GET, request_path, body=body), trading_pair)

        if res.r.status_code == 200:
            res.df = pd.DataFrame(res.json, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        return res

    def get_granularity():
        values = [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 604800]
        return values


class Fiat(Signiture):

    def get_deposit_history(self):
        request_path = '/api/account/v3/fiat/deposit/details'
        return Resp(self.query(GET, request_path))

    def get_channel_info(self):
        request_path = '/api/account/v3/fiat/channel'
        return Resp(self.query(GET, request_path))

    def get_withdrawal_history(self):
        request_path = '/api/account/v3/fiat/withdraw/details'
        return Resp(self.query(GET, request_path))
