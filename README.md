# python-api-for-okcoin
A Python API for interacting with [okcoin](https://www.okcoin.com/). The API returns account information as 
[```pandas```](https://pandas.pydata.org/) dataframes and [```plotly```](https://plotly.com/python/) graph objects 
where possible. The API currently only supports reading from the account. 

# Python API for ```okcoin``` Quickstart
## Install the API
```pip install okcoin-GBRUNNER```

## Register an API Key with [okcoin](https://www.okcoin.com/account/my-api)
1. Go to [**API**](https://www.okcoin.com/account/my-api).
2. Click [**Create API Key**](https://www.okcoin.com/account/my-api/create)
    - Give your key a ***Label***.
    - Give your key a ***passphrase***.
    - Select **Read** for ***Permissions*** (The current Python API only supports **Read**).
    - Get a code via SMS.
    - Click ***Confirm***.

## Create an auth.config file
Your **auth.config** file must contain the following fields:

    [DEFAULT]
    api_key=YOUR_API_KEY
    secret_key=YOUR SECRET_KEY

Optionally, you can add the ***pass_phrase*** into your **auth.config** file as follows:

    [DEFAULT]
    api_key=YOUR_API_KEY
    secret_key=YOUR SECRET_KEY
    pass_phrase=YOUR_PASS_PHRASE

If the ***pass_phrase*** is not included in your **auth.config** file, you will be 
prompted to enter it when connecting to your account.

## Import classes from ```okcoin```
```
from okcoin import Account
acc  = Account('auth.config')
```

## Use the API!
```
ledger = acc.get_ledger()
ledger.df
```
