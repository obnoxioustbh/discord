import json
import requests

postBody = {"id":"f9c88766-5237-4600-81a4-cdcf2fe18242","product_id":"d998698e","email":"Rustverf@gmail.com","ip_address":"195.67.105.106","country_code":"SE","user_agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","value":"0.5","currency":"USD","gateway":"Bitcoin","risk_level":9,"status":100,"delivered":None,"crypto_value":51426,"crypto_address":"19KQJWhnuWkS6SQB43vzM5PUPYxWJQB8Gy","referral":None,"usd_value":"0.5","exchange_rate":"1.0","custom":{},"created_at":"2017-04-20 03:10:49 UTC","updated_at":"2017-04-20 03:11:22 UTC","webhook_type":1}

rq = requests.post('http://discord.obnoxious.eu/paymentSECRETASFUCKBOY', data=json.dumps(postBody))
print(rq.text)