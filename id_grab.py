import requests

headers = {
	'X-Auth-Email': 'i.am@obnoxious.eu',
	'X-Auth-Key': '7H-rshyU6x-JbemzWkbFKXPysxSdLWPBrsoDLWXs4JrdZnrB-A',
}

URL = 'https://selly.gg/api/orders/4e6b6ae7-a6d5-472e-9f1f-ca6fdaea6eb2'

rq = requests.get(URL, headers=headers)

print(rq.json())