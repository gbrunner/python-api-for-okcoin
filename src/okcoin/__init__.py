import requests
import getpass
import datetime
import hmac
import base64
#import json
import pandas as pd
import configparser
import plotly.graph_objects as go

# documentation following numpy: https://numpydoc.readthedocs.io/en/latest/example.html#example

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'
GET = 'GET'
POST = 'POST'
REST_API_URL = "https://www.okcoin.com"


class _Signature:
    """
    The Signature class is a private class that is used to create a signature to that enables users to
    interface with the okcoin API. It takes as inputs a config file that contains your
    API_KEY, SECRET_KEY, and an optional PASS_PHRASE. If the PASS_PHRASE is not specified, you
    will be prompted for it upon instantiating the account object.


    Parameters
    ----------
    config_file : A file containing the api_key, secret_key, and pass_phrase

    pass_phrase : If a pass_phrase is not specified in the config_file, it can be entered as a separate parameter
    or you will be prompted to enter it through your Python IDE.

    Attributes
    ----------
    """

    def __init__(self,
                 config_file=r'auth.config',
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
        #print(request_path)
        #print(type)
        #print(body)
        if body != '':
            body = self.__parse_params_to_str(body)

        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        # self.get_timestamp()
        print(body)
        signature = self.__get_signature(timestamp, type, request_path, body)
        #signature = self.__get_signature(timestamp, type, request_path, body)
        #signature = self.__get_signature(timestamp, type, request_path, '')

        header = self.__get_header(signature, timestamp)
        # do request
        response = requests.get(self.REST_API_URL + request_path + body,
                                headers=header)
#data=body

        return response

class Account(_Signature):
    """
    The Account class is used to interface with you okcoin account. If contains functions that
    return your account value, the assets in contains, and its history. The Account class
    inherits from the Signature class, which takes as inputs a config file that contains your
    API_KEY, SECRET_KEY, and an optional PASS_PHRASE. If the PASS_PHRASE is not specified, you
    will be prompted for it upon instantiating the account object.


    Parameters
    ----------
    config_file : A file containing the api_key, secret_key, and pass_phrase

    pass_phrase : If a pass_phrase is not specified in the config_file, it can be entered as a separate parameter
    or you will be prompted to enter it through your Python IDE.

    Attributes
    ----------

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> from okcoin import Account
    >>> acc = Account(config_file='auth.conf')
    <okcoin.Account object at 0x00000291A320A288>
    """

    def get_account_type(self):
        r"""Returns a dictionary of the different acount types and the
        numerical code that corresponds to them in okcoin.

        Returns
        -------
        account_tpye : dict
            A dictionary of account types (i.e. funding, trading, spot).

        Examples
        --------
        >>> account_type = acc.get_account_type()
        >>> print(account_type)
        {'spot': 1, 'margin': 5, 'funding': 6}
        """
        # In Account API
        account_type = {
            'spot': 1,
            'margin': 5,
            'funding': 6
        }
        #return pd.DataFrame(account_type, index=[0])
        return account_type

    def get_withdrwal_status(self):
        r"""Returns a dictionary of the withdrawal status and the
        numerical code that corresponds to them in okcoin.

        Returns
        -------
        withdrawal_status : dict
            A dictionary of withdrawal status (i.e. cancelled, failed, pending, etc.).

        Examples
        --------
        >>> withdrawal_status = acc.get_withdrwal_status()
        >>> print(withdrawal_status)
        {'Pending cancel': -3, 'Cancelled': -2, 'Failed': -1, 'Pending': 0, 'Sending': 1, 'Sent': 2,
        'Awaiting email verification': 3, 'Awaiting manual verification': 4,
        'Awaiting identity verification': 5}
        """
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
        #return pd.DataFrame(withdrawal_status, index=[0])
        return withdrawal_status

    def get_wallet(self):
        r"""Retrieves information on the balances of all of the assets that are
        available or on hold.

        Returns
        -------
        account_info : _AccountInfo
            A custom data structure that enables you to view you wallet as a dataframe,
            json, or plotly chart.

        Examples
        --------
        >>> acc = Account('auth.conf')
        >>> wallet = acc.get_wallet()
        >>> print(wallet.r)
        <Response [200]>
        >>> print(wallet.json)
        [{'balance': '0.00071305', 'available': '0.00071305', 'currency': 'BTC', 'hold': '0.00000000'}, {'balance': '793.99043577', 'available': '793.99043577', 'currency': 'STX', 'hold': '0.00000000'}]
        >>> print(wallet.df)
                balance     available currency        hold
        0    0.00071305    0.00071305      BTC  0.00000000
        1  793.99043577  793.99043577      STX  0.00000000
        """
        request_path = '/api/account/v3/wallet'
        #body = ''

        #resp = _AccountInfo(self.query(GET, request_path, body))

        #fig = go.Figure([go.Bar(x=resp.df['currency'].tolist(), y=resp.df['balance'].tolist())])
        #fig.update_layout(
        #    title='Funding Account Assets',
        #    yaxis_title='Asset',
        #    xaxis_title='Quantity')

        return _AccountInfo(self.query(GET, request_path)) #, fig

    def get_asset_valuation(self, currency='BTC'):
        r"""Get the valuation of the total assets of the account in btc or fiat currency.

        Parameters
        ----------
        currency : 	The valuation according to a certain fiat currency.  The currency
            can only be one of the following: BTC, USD, CNY, JPY, KRW, RUB.
            The default unit is BTC.

        Returns
        -------
        account_info : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> asset_val = acc.get_asset_valuation('USD')
        >>> print(asset_val.df)
        account_type                               0
        balance                               523.51
        valuation_currency                       USD
        timestamp           2021-05-13T02:21:30.061Z
        """
        request_path = '/api/account/v3/asset-valuation'
        body = {'valuation_currency': currency}

        return _Resp(self.query(GET, request_path, body))

    # Sub account erroring
    def get_sub_account(self, account_name=''):
        r""" Obtains the fund balance information in each sub account in the users okcoint
        account.

        Parameters
        ----------
        account_name : 	The name of the sub-account.

        Returns
        -------
        account_info : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> sub_account = acc.get_sub_account()
        >>> print(sub_account.json)
        {
            "data": {
                "sub_account": "Test",
                "asset_valuation": 0.00003463,
                "account_type:futures": [
                    {
                        "balance": 0.00000245,
                        "max_withdraw": 0.00000245,
                        "currency": "BTC",
                        "underlying": "BTC_USD",
                        "equity": 0.00000245
                    },
                    {
                        "balance": 1.053473,
                        "max_withdraw": 1.053473,
                        "currency": "XRP",
                        "underlying": "XRP_USD",
                        "equity": 1.053473
                    }
                ],
                "account_type:spot": [
                    {
                        "balance": 0.000312544038152,
                        "max_withdraw": 0.000312544038152,
                        "available": 0.000312544038152,
                        "currency": "USDT",
                        "hold": 0
                    }
                ]
            }
        }
        """
        request_path = '/api/account/v3/sub-account'
        if account_name:
            body = {'sub-account':account_name}

        else:
            body = {'sub-account': ''}

        return _Resp(self.query(GET, request_path, body))

    def get_currency(self, token='BTC'):
        r""" Retrieves information for a single token in your account,
        including the remaining balance, and the amount available or on hold.

        Parameters
        ----------
        token : str
            The token you are querying.

        Returns
        -------
        token_info : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> curr = acc.get_currency(token='BTC')
        >>> print(curr.df)
              balance   available currency        hold
        0  0.00076409  0.00076409      BTC  0.00000000
        """
        request_path = '/api/account/v3/wallet/' + token
        return _Resp(self.query(GET, request_path))

    ## Withdraw or Trade Permission
    def get_funds_transfer(self):
        r"""This request supports the transfer of funds among your funding account,
        trading accounts, main account, and sub accounts.

        Returns
        -------
        success : bool

        Examples
        --------
        >>>
        """
        pass

    ## Withdraw or Trade Permission
    def withdrawal(self):
        pass

    def get_withdrawal_history(self, currency=''):
        r""" Retrieves the 100 most recent withdrawal records.

        Parameters
        ----------
        currency : 	str
            The currency that was withdrawn.

        Returns
        -------
        withdrawal_hist : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> withdraw_hist = acc.get_withdrawal_history()
        >>> withdraw_hist.df
        Empty DataFrame
        Columns: []
        Index: []
        """
        if currency:
            request_path = '/api/account/v3/withdrawal/history/' + currency.lower()
        else:
            request_path = '/api/account/v3/withdrawal/history'
        return _Resp(self.query(GET, request_path))

    def get_ledger(self):
        r""" Retrieves the value of your account for the past month.


        Returns
        -------
        bills : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> ledger = acc.get_ledger()
        >>> ledger.df
                   amount       balance  ...            typename                 timestamp
        0      0.00000611    0.00076409  ...                      2021-05-16T05:41:27.000Z
        1      0.00000793    0.00075798  ...                      2021-05-15T04:41:24.000Z
        2      0.00001004    0.00075005  ...                      2021-05-14T04:41:25.000Z
        3      0.00001777    0.00074001  ...                      2021-05-13T04:41:27.000Z
        [4 rows x 7 columns]
        """
        request_path = '/api/account/v3/ledger'
        ledger_resp = _Resp(self.query(GET, request_path))
        ledger_resp.df.amount = ledger_resp.df.amount.astype('float64')
        ledger_resp.df.balance = ledger_resp.df.balance.astype('float64')
        ledger_resp.df.fee = ledger_resp.df.fee.astype('float64')
        ledger_resp.df.ledger_id = ledger_resp.df.ledger_id.astype('int64')
        ledger_resp.df.timestamp = ledger_resp.df.timestamp.astype('datetime64')
        return ledger_resp

    def get_deposit_address(self, currency='BTC'):
        r""" Retrieves the deposit addresses of currencies, including previously used addresses.

        Parameters
        ----------
        currency : 	str
            The currency deposited.

        Returns
        -------
        account_info : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> dep_addr = acc.get_deposit_address()
        >>> dep_addr.json
        {'code': 404,
         'data': {},
         'detailMsg': '',
         'error_code': '404',
         'error_message': 'Not Found',
         'msg': 'Not Found'}
        """

        request_path = '/api/account/v3/deposit/address/' + currency.lower()
        return _Resp(self.query(GET, request_path))

    def get_deposit_history(self, currency='USD'):
        r""" Retrieves the deposit history of all currencies,
        up to 100 recent records(Within one year).

        Parameters
        ----------
        currency : 	str
            The currency deposited.

        Returns
        -------
        account_info : _Resp
            A custom data structure that allows you to view the request status,
            the request response as json, and the request response as a dataframe.

        Examples
        --------
        >>> dep_hist = acc.get_deposit_history()
        >>> dep_hist.df
                 amount                updated_at  ...                 timestamp status
        0  200.00000000  2021-05-11T17:18:21.000Z  ...  2021-05-10T13:09:39.000Z      5
        1  100.00000000  2021-05-03T17:18:41.000Z  ...  2021-04-30T17:06:11.000Z      5
        2  100.00000000  2021-04-24T03:13:52.000Z  ...  2021-04-23T13:34:20.000Z      5
        3  100.00000000  2021-04-12T15:40:51.000Z  ...  2021-04-09T12:22:16.000Z      5
        [4 rows x 9 columns]
        """
        request_path = '/api/account/v3/deposit/history/'+currency.lower()

        return _Resp(self.query(GET, request_path))

    def get_currencies(self):
        r""" This retrieves a list of all currencies.

        Returns
        -------
        currency_info : _Resp
            An object containing the currencies currently supported by okcoin.

        Examples
        --------
        >>> currencies = acc.get_currencies()
        >>> print(currencies.df)
        can_internal                     name  ... can_deposit min_withdrawal
        0             0                US Dollar  ...           1
        1             0                     Euro  ...           1
        """
        request_path = '/api/account/v3/currencies'
        return _Resp(self.query(GET, request_path))


    # This is buggy. You need to specify a currency to get anything back
    def get_withdrawal_fees(self, currency='BTC'):
        r"""

        Parameters
        ----------
        account_name : 	str
            The name of the sub-account.

        Returns
        -------
        fee : _Resp
            An object contianing the min and max fees for the withdrawal of the
            specified currency.

        Examples
        --------
        >>> withdraw_fee = acc.get_withdrawal_fees('STX')
        >>> print(withdraw_fee.df)
        min_fee     currency     max_fee
        0  1.00000000      STX  2.00000000
        """
        request_path = '/api/account/v3/withdrawal/fee'
        if currency:
            body = {'currency':currency.lower()}
        else:
            body=''
        #body = json.dumps(p)
        #print(body)
        return _Resp(self.query(GET, request_path, body=body))

    def get_balance_from_ledger(self, df, currency='BTC'):
        r""" Returns a dataframe and Plotly chart that show the balance
        of the funding account.

        Parameters
        ----------
        df : 	dataframe
            The dataframe generated by the

        currency : str
            The currency that you are querying.

        Returns
        -------
        balance : _Resp
            A n object that...

        fig : Plotly chart
            A plotly chart of the balance of the funding account.

        Examples
        --------
        >>> ledger = account.get_ledger()
        >>> btc_balance = account.get_balance_from_ledger(ledger.df,'BTC')
        >>> print(btc_balance[0])
        >>> btc_balance[1].write_html('test.html', auto_open=True)
        """
        cur = df[df['currency']==currency]
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


## Spot Trading Account Info
class Spot(_Signature):
    """
    The Spot class is used to interface with you okcoin spot trading account. If contains functions that
    return your account value and your trading history. It also contains functions that return the current
    crypto market conditions, such as trading pairs, asset prices, ad asset history. The Spot class
    inherits from the Signature class, which takes as inputs a config file that contains your
    API_KEY, SECRET_KEY, and an optional PASS_PHRASE. If the PASS_PHRASE is not specified, you
    will be prompted for it upon instantiating the account object.


    Parameters
    ----------
    config_file : A file containing the api_key, secret_key, and pass_phrase

    pass_phrase : If a pass_phrase is not specified in the config_file, it can be entered as a separate parameter
    or you will be prompted to enter it through your Python IDE.

    Attributes
    ----------

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> from okcoin import Spot
    >>> spot = Spot(config_file='auth.conf')

    """

    def get_account_chart(self, df):
        fig = go.Figure([go.Bar(x=df['currency'].tolist(), y=df['balance'].tolist())])
        fig.show()

    def get_order_status(self):
        # In Spot API
        r""" Returns the status of an order and the numeric value that corresponds to it
        in the Okcoin API.

        Returns
        -------
        order_status : A dictionary object of order status values.

        Examples
        --------
        >>> status = spot.get_order_status()
        """
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
        #return pd.DataFrame(order_status, index=[0])
        return order_status

    def get_accounts(self, currency=None):
        r""" Returns a list of assets, (with non-zero balance),
        remaining balance, and amount available in the spot trading account.

        Parameters
        ----------
        currency : 	str
            Optional parameter specifying which asset you want to return

        Returns
        -------
        resp : _Resp
            A query response object that contains the query result as a dictionary or dataframe

        fig : figure
            A Plotly figure displaying the valuation of the assets in the account

        Examples
        --------
        >>> accounts = spot.get_accounts()
        >>> accounts[1].write_html('temp.html', auto_open=True)
        """
        request_path = '/api/spot/v3/accounts'
        if currency:
            request_path += "/" + currency.lower()

        resp = _Resp(self.query(GET, request_path))

        fig = go.Figure([go.Bar(x=resp.df['currency'].tolist(), y=resp.df['balance'].tolist())])
        fig.update_layout(
            title='Spot Trading Account Assets',
            yaxis_title='Asset',
            xaxis_title='Quantity')

        return resp, fig

    def get_ledger(self, currency='BTC'):
        r""" Returns the spot account bills dating back the past 3 months.
        Pagination is supported and the response is sorted
        with most recent first in reverse chronological order.

        Parameters
        ----------
        currency : 	str
            Currency being queried

        Returns
        -------
        balance : _Resp
            A query response opbect that contains the query result as a dictionary and as a dataframe

        Examples
        --------
        >>> currency = spot.get_ledger('USD')
        >>> currency.df
        """
        request_path = '/api/spot/v3/accounts'
        request_path += "/" + currency.lower() + "/ledger"
        return _Resp(self.query(GET, request_path))

    def place_order(self):
        pass

    def get_order_list(self, trading_pair='BTC-USDT', state=7):
        r""" Returns This the list of your orders from
        the most recent 3 months. This request supports paging
        and is stored according to the order time in chronological
        order from latest to earliest.

        Parameters
        ----------
        trading_pair : str
            The trading pair that was ordered

        state : int
            The state of the order, represented as an integer.


        Returns
        -------
        orders : _Resp
            A query response object that contains the query result as a dictionary and as a dataframe

        Examples
        --------
        >>> orders = spot.get_order_list('STX-USD')
        >>> orders.df
        """
        request_path = '/api/spot/v3/orders'#?instrument_id='+trading_pair+'&state='+str(state)
        # Using the "body" doesn't work
        body = {'instrument_id':trading_pair,
            'state':str(state)}
        return _Resp(self.query(GET, request_path, body=body))

    def get_orders_pending(self, trading_pair='BTC-USD'):
        r""" Returns the list of your current open orders.
        Pagination is supported and the response
        is sorted with most recent first in reverse chronological order.

        Parameters
        ----------
        trading_pair : str
            The trading pair that was ordered.


        Returns
        -------
        orders : _Resp
            A query response opbect that contains the query result as a dictionary and as a dataframe


        Examples
        --------
        >>> pending = spot.get_orders_pending('STX-USD')
        >>> pending.df
        """
        request_path = '/api/spot/v3/orders_pending'
        body = {'instrument_id':trading_pair.lower()}
        return _Resp(self.query(GET, request_path, body=body))

    def get_order_details(self, order_id, trading_pair='BTC-USDT'):
        r""" Returns order details by order ID.Can get order information for nearly 3 months。
        Unfilled orders will be kept in record for only
        two hours after it is canceled.

        Parameters
        ----------
        order_id : int
            The specific order ID that you want to query

        trading_pair : str
            The trading pair that was ordered


        Returns
        -------
        orders : _Resp
            A query response opbect that contains the query result as a dictionary and as a dataframe


        Examples
        --------
        >>> details = spot.get_order_details(order_id, 'BTC-USD')
        >>> details.df
        """
        request_path = '/api/spot/v3/orders/' + str(order_id)
        body = {'instrument_id': trading_pair.lower()}
        return _Resp(self.query(GET, request_path, body=body))

    def get_trade_fee(self):
        r""" Returns the transaction fee rate corresponding to
        your current account transaction level. The sub-account
        rate under the parent account
        is the same as the parent account.
        Update every day at 0am

        Returns
        -------
        fee : _Resp
            A query response opbect that contains the query result as a dictionary and as a dataframe


        Examples
        --------
        >>> fees = spot.get_trade_fee()
        >>> fees.json
        {'category': '1', 'maker': '0.001', 'taker': '0.002', 'timestamp': '2021-06-11T02:41:44.149Z'}
        """
        request_path = '/api/spot/v3/trade_fee'
        return _Resp(self.query(GET, request_path))

    def get_filled_orders(self, trading_pair='BTC-USDT'):
        r""" Returns recently filled transaction details.
        This request supports paging and is stored according
        to the transaction time in chronological order from
        latest to earliest.
        Data for up to 3 months can be retrieved.

        Parameters
        ----------
        trading_pair : 	str
            The trading pair that was ordered


        Returns
        -------
        orders : _Resp
            A query response opbect that contains the query result as a dictionary and as a dataframe

        Examples
        --------
        >>> filled = spot.get_filled_orders('STX-USD')
        >>> filled.df
                  created_at        currency  ...                 timestamp trade_id
        0   2021-04-02T15:20:37.000Z      USD  ...  2021-04-02T15:20:37.000Z   103932
        1   2021-04-02T15:20:37.000Z      BTC  ...  2021-04-02T15:20:37.000Z   103932
        """
        request_path = '/api/spot/v3/fills'
        body = {'instrument_id': trading_pair.lower()}
        return _Resp(self.query(GET, request_path, body=body))

    def get_trading_pairs(self):
        r""" Returns snapshots of market data and is publicly
        accessible without account authentication. Retrieves
        list of trading pairs, trading limit, and unit increment.


        Returns
        -------
        trading_pairs : dict
            A dictionary of trading pairs available on Okcoin.

        Examples
        --------
        >>>
        """
        request_path = '/api/spot/v3/instruments'
        return _Resp(self.query(GET, request_path))

    def get_order_book(self, trading_pair='BTC-USDT',
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
        >>>
        """
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/book'
        if aggregation_depth:
            body = {'depth': str(aggregation_depth)}
        else:
            body = ''

        res = _Resp(self.query(GET, request_path, body=body))

        if res.r.status_code ==200:
            asks = pd.DataFrame(res.json['asks'], columns=['ask price', 'ask size', 'liquidated orders'])
            bids = pd.DataFrame(res.json['bids'], columns=['bid price', 'bid size', 'liquidated orders'])
        return asks, bids

    def get_ticker(self):
        r""" Returns the latest price snapshot, best bid/ask price,
        and trading volume in the last 24 hours for all trading pairs.
        This is publicly accessible without account authentication.

        Returns
        -------
        tickers : _Resp
            A query response object that contains the query result as a dictionary and as a dataframe

        Examples
        --------
        >>>
        """
        request_path = '/api/spot/v3/instruments/ticker'
        return _Resp(self.query(GET, request_path))


    def get_trading_pair_info(self, trading_pair='BTC-USDT'):
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
        >>>
        """
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/ticker'
        return _Resp(self.query(GET, request_path))

    def get_latest_trades(self, trading_pair='STX-USD'):
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
        >>>
        """
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/trades'
        return _Resp(self.query(GET, request_path))

    #granularity=86400&start=2019-03-19T16:00:00.000Z&end=2019-03-19T16:00:00.000Z
    def get_candlestick_chart(self, trading_pair='STX-USD', start='', end='', granularity=None):
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
        >>>
        """
        request_path = '/api/spot/v3/instruments/' + trading_pair + '/candles'

        body = {'start': str(start),
               'end':str(end),
               'granularity':str(granularity)}

        res = _Candlestick(self.query(GET, request_path, body=body), trading_pair)

        if res.r.status_code ==200:
            res.df = pd.DataFrame(res.json, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        return res

    def get_granularity(self):
        r""" Returns a list of intervals that can be used to
        generating candlestick charts.


        Returns
        -------
        values : list
            A list of all possible granularity intervals

        Examples
        --------
        >>> spot.get_granularity()
        """
        values = [60,180,300,900,1800,3600,7200,14400,21600,43200,86400,604800]
        return values

class Fiat(_Signature):
    """
    The Fiat class is used to withdraw and deposit money into your okcoin account. It enables you to
    understand your deposit and withdrawal history. It also enables you to withdraw and deposit currency
    if you have created an API key that enables trading. The Fiat class
    inherits from the Signature class, which takes as inputs a config file that contains your
    API_KEY, SECRET_KEY, and an optional PASS_PHRASE. If the PASS_PHRASE is not specified, you
    will be prompted for it upon instantiating the account object.


    Parameters
    ----------
    config_file : A file containing the api_key, secret_key, and pass_phrase

    pass_phrase : If a pass_phrase is not specified in the config_file, it can be entered as a separate parameter
    or you will be prompted to enter it through your Python IDE.

    Attributes
    ----------

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> from okcoin import Fiat
    >>> fiat = Fiat(config_file='auth.conf')

    """

    def get_deposit_history(self, deposit_id):
        r""" Returns the details of a deposit given the
        deposit ID.

        Parameters
        ----------
        deposit_id : str
            The dataframe generated by the


        Returns
        -------
        deposit_hist : _Resp
            A query response object that contains the query result as a dictionary and as a dataframe


        Examples
        --------
        >>>
        """
        request_path = '/api/account/v3/fiat/deposit/details'
        return _Resp(self.query(GET, request_path))

    def get_channel_info(self):
        r""" Returns the status of an order and the numeric value that corresponds to it
        in the Okcoin API.

        Parameters
        ----------
        df : 	dataframe
            The dataframe generated by the


        Returns
        -------
        balance : _Resp
            A n object that...

        Examples
        --------
        >>>
        """
        request_path = '/api/account/v3/fiat/channel'
        return _Resp(self.query(GET, request_path))

    def get_withdrawal_history(self):
        r""" Returns the status of an order and the numeric value that corresponds to it
        in the Okcoin API.

        Parameters
        ----------
        df : 	dataframe
            The dataframe generated by the


        Returns
        -------
        balance : _Resp
            A n object that...

        Examples
        --------
        >>>
        """
        request_path = '/api/account/v3/fiat/withdraw/details'
        return __Resp(self.query(GET, request_path))
