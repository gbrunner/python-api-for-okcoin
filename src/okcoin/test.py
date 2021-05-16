import hmac
import base64
import requests
import json
import datetime
import time

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'

apikey = "4f3a71fc-e4a2-4d52-ac7f-979844687317"
secretkey = "03745830BE3809798023EF471E83B596"
rest_api_url = "https://okcoin.com"
timestamp_sample = "2014-11-06T10:34:47.123Z"
passphrase = "pyCOIN2021"

# signature
def signature(timestamp, method, request_path, secret_key, body = None):
    if str(body) == '{}' or str(body) == 'None' or body == None:
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


# Example Request
# set the request url
base_url = 'https://www.okcoin.com'
request_path = '/api/account/v3/asset-valuation'
#request_path = '/api/account/v3/wallet'
timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"
print(timestamp)
# set request header
params = {'valuation_currency': 'USD'}
body = json.dumps(params)
#body = ''
print(body)
header = get_header(apikey, signature(timestamp, 'GET', request_path, secretkey,body), timestamp, passphrase)
print(header)
# do request
response = requests.get(base_url + request_path, data = body, headers=header)
# json
print(timestamp)
print(response.status_code)
print(response.json())