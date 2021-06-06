# python-api-for-okcoin
A python API for interacting with [okcoin](https://www.okcoin.com/). The API currently only supports reading from the account.

# Python API for ``okcoin`` Quickstart
## Install the API
``pip install okcoin-GBRUNNER``

## Register an API Key with [okcoin]()
Instructions to register API Key

## Create an auth.config file
``[DEFAULT]
api_key=YOUR_API_KEY
secret_key=YOUR SECRET_KEY
pass_phrase=YOUR_PASS_PHRASE``

## Import classes from ``okcoin``
``from okcoin import Account
acc  = Account('auth.config')``

## Use the API!
``ledger = acc.get_ledger()
ledger.df``
