import json
import requests

quote_ = 'RUB'

r = requests.get(
                f"https://free.currconv.com/api/v7/convert?q=USD_{quote_}&compact=ultra&apiKey=ec0d89548ad9ff4620ad")
quote_to_usd = float(json.loads(r.content)['RUB_USD'])

print(quote_to_usd)