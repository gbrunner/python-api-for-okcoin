import sys
sys.path.append(r'C:\Users\greg6750\Documents\python-api-for-okcoin\src')

from okcoin import Account




acc = Account(r'C:\Users\greg6750\Documents\IPython Notebooks\okcoin\auth.config')
print(acc)

acc_type = acc.get_account_type()
print(acc_type)

withdraw_status = acc.get_withdrwal_status()
print(withdraw_status)

wallet = acc.get_wallet()
print(wallet.r)
print(wallet.json)
print(wallet.df)

asset_val = acc.get_asset_valuation(currency='USD')
print(asset_val.r)
print(asset_val.json)
print(asset_val.df)

curr = acc.get_currency(token='BTC')
print(curr.r)
print(curr.json)
print(curr.df)

withdraw_hist = acc.get_withdrawal_history(currency='STX')
print(withdraw_hist.r)
print(withdraw_hist.json)
print(withdraw_hist.df)

ledger = acc.get_ledger()
print(ledger.r.status)
print(ledger.json)
print(ledger.df)

deposit_addr = acc.get_deposit_address(currency='BTC')
print(deposit_addr.r.status)
print(deposit_addr.json)
print(deposit_addr.df)

deposit_hist = get_deposit_history(currency='USD')
print(deposit_hist.r.status)
print(deposit_hist.json)
print(deposit_hist.df)

currencies = acc.get_currencies()
print(currencies.r.status)
print(currencies.json)
print(currencies.df)

withdraw_fees = get_withdrawal_fees(currency='BTC')
print(withdraw_fees.r.status)
print(withdraw_fees.json)
print(withdraw_fees.df)

balance = get_balance_from_ledger(self, ledger.df, 'BTC')
print(balance[0])
balance[1].show()

#spot = Spot()

