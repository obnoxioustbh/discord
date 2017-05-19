import aiohttp
import asyncio
import json
from time import sleep

async def semGet(url, token, sem):
	async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
		async with session.get('http://2captcha.com/in.php?key=5239dcfa969c0f7e3ecfaac6e1924e95&method=userrecaptcha&googlekey=6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn&pageurl=https://discordapp.com/register') as resp:
			CID = await resp.read()
			CID = CID.decode('utf-8').split('|')[1]

		print('[+] Waiting captcha')

		while True:
			async with session.get('http://2captcha.com/res.php?key=5239dcfa969c0f7e3ecfaac6e1924e95&action=get&id={0}'.format(CID)) as resp:
				RES = await resp.read()
				RES = RES.decode('utf-8').split('|')
				
				if 'CAPCHA_NOT_READY' in RES[0]:
					await asyncio.sleep(3)
					continue
				else:
					c = RES[1]
					break
		try:
			async with session.post(url, proxy="http://gw.proxies.online:8081", 
				data=json.dumps({"token":token, "captcha_key":c}),
				headers={
					'Content-Type': 'application/json',
					'Referer': 'https://discordapp.com/verify?token={0}'.format(token),
				}
				) as request:
				body = await request.json()
				try:
					print(body['token'])
					if "Invalid verify token" in body['token'][0]:
						print('[+] Already verified')
					elif 'invalid' in body['token'][0]:
						print('[!] Flagged for captcha... trying again..')
					else:
						print('[+] Verified')
				except KeyError:
					print('[-] Expected captcha.')
					return
				except:
					print('[-] BIG ERROR... trying again..')

					return body
		except:
			return

async def verify(token, sem):
	return await semGet("https://discordapp.com/api/v6/auth/verify", token, sem)

async def task(tokens):
	tasks = []
	sem = asyncio.Semaphore(1000)
	for token in tokens:
		tasks.append(asyncio.ensure_future(verify(token, sem)))
		#await asyncio.sleep(0.5)

	wait = asyncio.gather(*tasks)
	await wait

	for resp in wait:
		print(resp)

def main(urls):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(task(urls))