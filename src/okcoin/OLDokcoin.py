import requests
import getpass
import datetime
#import hashlib
import hmac
#import time
import base64
import json
import pandas as pd
import configparser

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'
GET = 'GET'
POST = 'POST'
REST_API_URL = "https://www.okcoin.com"


def to_df(data):
    return pd.DataFrame(data=data)

class query_result:
    def __init__(self, obj):
        #self.res = res
        self.df = pd.DataFrame(self.res) #None
        self.json = obj.json() #None #self.res #None
        self.r = obj

    def result(self, res):
        self.df = pd.DataFrame(res.json())
        self.json = res.json()
        self.r = res


class auth:
    def __init__(self):

        config = configparser.ConfigParser()
        config.read('auth.config')

        self.api_key = config['DEFAULT']['api_key'] #api_key
        self.secret_key = config['DEFAULT']['secret_key']#secret_key
        self.REST_API_URL = REST_API_URL
        print("GetPass")
        print(config['DEFAULT']['pass_phrase'])
        if config['DEFAULT']['pass_phrase'] == None or config['DEFAULT']['pass_phrase'] == "":
            #print("HERE1")
            p = getpass.getpass(prompt='Enter your password:')
            self.pass_phrase = p
        else:
            #print("HERE2")
            self.pass_phrase = config['DEFAULT']['pass_phrase']  # pass_phrase
        #self.query_result = query_result()

    def get_timestamp(self):
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"
        print(timestamp)
        return timestamp

    # signature
    def get_signature(self, t, method, request_path, body=None):
        if str(body) == '{}' or str(body) == 'None' or body == None:
            body = ''
        message = str(t) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    # set request header
    def get_header(self, sig, t):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = self.api_key
        header[OK_ACCESS_SIGN] = sig
        header[OK_ACCESS_TIMESTAMP] = t
        header[OK_ACCESS_PASSPHRASE] = self.pass_phrase
        return header

    def parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'

        return url[0:-1]

    def query(self, type, request_path, body=''):
        print(request_path)
        print(type)
        print(body)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"
        #self.get_timestamp()
        print(body)
        signature = self.get_signature(timestamp, type, request_path, body)

        header = self.get_header(signature, timestamp)
        # do request

        response = requests.get(self.REST_API_URL + request_path,
                                data=body,
                                headers=header)

        return response

## Funding Account API

    def get_wallet(self):
        request_path = '/api/account/v3/wallet'
        body = ''
        return self.query(GET, request_path, body)

    def get_asset_valuation(self, currency='BTC'):
        request_path = '/api/account/v3/asset-valuation'
        p = {'valuation_currency': currency}
        body = json.dumps(p)
        return self.query(GET, request_path, body)

    # Sub account erroring
    def get_sub_account(self, account_name=None):
        request_path = '/api/account/v3/sub-account'
        if account_name:
            p = {'sub_account':account_name}
            body = json.dumps(p)
        else:
            p = {'sub-account': ''}
            body = json.dumps(p)
        return self.query(GET, request_path, body)

    def get_currency(self, token='BTC'):
        request_path = '/api/account/v3/wallet/' + token
        return self.query(GET, request_path)

    ## Withdraw or Trade Permission
    #def get_funds_transfer(self)
        pass

    ## Withdraw or Trade Permission
    def withdrawal(self):
        pass

    def get_withdrawal_history(self, currency=None):
        if currency:
            request_path = '/api/account/v3/withdrawal/history/' + currency.lower()
        else:
            request_path = '/api/account/v3/withdrawal/history'
        return self.query(GET, request_path)

    def get_ledger(self):
        request_path = '/api/account/v3/ledger'
        return self.query(GET, request_path)

    def get_deposit_address(self, currency='BTC'):
        request_path = '/api/account/v3/deposit/address/' + currency.lower()
        return self.query(GET, request_path)

    def get_deposit_history(self, currency='usd'):
        request_path = '/api/account/v3/deposit/history/'+currency
        p = {'currency': currency}
        body = json.dumps(p)
        return self.query(GET, request_path)#, body=body)

    def get_currencies(self):
        request_path = '/api/account/v3/currencies'
        return self.query(GET, request_path)

    # This is buggy. You need to specify a currency to get anything back
    def get_withdrawal_fees(self, currency='BTC'):
        request_path = '/api/account/v3/withdrawal/fee'
        if currency:
            p = {'currency':currency.lower()}
        else:
            p = {}
        body = json.dumps(p)
        print(body)
        return self.query(GET, request_path, body=body)

    def as_df(self, r):
        return pd.DataFrame(r.json())

## Spot Trading Account Info

    def get_spot_accounts(self, currency=None):
        request_path = '/api/spot/v3/accounts'
        if currency:
            request_path += "/" + currency.lower()
        return self.query(GET, request_path)

    def get_spot_ledger(self, currency='BTC'):
        request_path = '/api/spot/v3/accounts'
        request_path += "/" + currency.lower() + "/ledger"
        return self.query(GET, request_path)




coin = auth()

## Funding
#r = coin.get_wallet()
#r = coin.get_currency()
#r = coin.get_deposit_history('btc')
#r = coin.get_withdrawal_history('BTC')
#r = coin.get_deposit_address()
#r = coin.get_ledger()
#r = coin.get_currencies()
#r = coin.get_withdrawal_fees()#'STX')

## Spot
#r = coin.get_spot_accounts('STX')
r = coin.get_spot_ledger('STX')

print(r)
print(r.status_code)
print(r.json())
print(coin.as_df(r))
