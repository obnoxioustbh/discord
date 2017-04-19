import aiohttp
import asyncio
import json

async def semGet(url, token, sem):
	async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
		while True:
			try:
				async with session.get('https://discordapp.com/verify?token={0}'.format(token), proxy="http://gw.proxies.online:8081",
					headers={
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate, br',
						'DNT': '1',
						'Connection': 'keep-alive',
						'Upgrade-Insecure-Requests': '1',
					}) as rq:
					await rq.read()

				async with session.post(url, proxy="http://gw.proxies.online:8081", 
					data=json.dumps({"token":token, "captcha_key":'null'}),
					headers={
						'Content-Type': 'application/json',
						'Referer': 'https://discordapp.com/verify?token={0}'.format(token),
						'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiJ9',
						'Accept': '*/*',
						'Accept-Language': 'en-US',
						'Accept-Encoding': 'gzip, deflate, br',
						'DNT': '1',
						'Connection': 'keep-alive',
					}
					) as request:
					body = await request.json()
					try:
						print(body['token'])
						if "Invalid verify token" in body['token'][0]:
							print('[+] Already verified')
							return
						elif 'invalid' in body['token'][0]:
							print('[!] Flagged for captcha... trying again..')
							continue
						else:
							print('[+] Verified')
							return
					except KeyError:
						print('[-] Expected captcha.')
						continue
					except:
						print('[-] BIG ERROR... trying again..')
						continue

						return body

			except aiohttp.errors.ServerDisconnectedError:
				continue

			except aiohttp.errors.HttpProxyError:
				continue

			except aiohttp.errors.ClientResponseError:
				continue

			except aiohttp.errors.ClientOSError:
				continue

async def verify(token, sem):
	return await semGet("https://discordapp.com/api/v6/auth/verify", token, sem)

async def task(urls):
	tasks = []
	sem = asyncio.Semaphore(1000)
	for url in urls:
		token = url.split('?token=')[1]
		tasks.append(asyncio.ensure_future(verify(token, sem)))

	wait = asyncio.gather(*tasks)
	await wait

	for resp in wait:
		print(resp)

def main(urls):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(task(urls))