import aiohttp
import asyncio
import sys
import random
import time
import json

#from GmailDotEmailGenerator import GmailDotEmailGenerator

sys.argv = ['', 'accounts.txt', 100]

class bot:
	def __init__(self, sem):
		self.sem = sem
		self.proxy = 'http://us1.proxies.online:8182'
		self.googleKey = '6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn'
		self.captchaKey = '5239dcfa969c0f7e3ecfaac6e1924e95'
		self.username = 'obnoxious{0}'.format(random.randint(100, 999999))
		self.email = 'obnoxious+{0}@dongcorp.org'.format(self.username)
		self.password = 'apple123'
		self.fingerprint = '302020375816962048.Kz2cCvWNOnJxmjfRtg4sBavQ0lY'
		self.superproperties = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiJ9'

	async def start(self):
		try:
			async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
				#ipcheck = await self.ipCheck(session)
				#print(ipcheck)
				index = await self.index(session)
				account = await self.register(session)
				token = json.loads(account)['token']
				print('{0}:{1}:{2}:{3}'.format(self.username, self.password, self.email, token), file=open(sys.argv[1], 'a'))
		except:
			return
			

	async def ipCheck(self, session):
		return await self.semGet('https://httpbin.org/ip', session, proxy=self.proxy)

	async def index(self, session):
		return await self.semGet('https://discordapp.com/register', session,
			headers={
				'Referer': 'http://google.com/'			
			},
			proxy=self.proxy
		)

	async def register(self, session):
		return await self.semPost('https://discordapp.com/api/v6/auth/register', session, 
			data=json.dumps(
				{
					'fingerprint': self.fingerprint,
					'email': self.email, 
					'username': self.username, 
					'password': self.password, 
					'invite': "null", 
					'captcha_key': "null",

				}
			), 
			headers={
				'X-Fingerprint': self.fingerprint,
				'X-Super-Properties': self.superproperties,
				'Accept': '*/*',
				'Accept-Language': 'en-US',
				'Accept-Encoding': 'gzip, deflate, br',
				'Content-Type': 'application/json',
				'Referer': 'https://discordapp.com/register',
				'DNT': '1',
				'Connection': 'keep-alive',
			},
			proxy=self.proxy)

	async def semPost(self, url, session, headers={}, params={}, data=None, proxy=None):
		async with self.sem as sem:
			async with session.post(url, headers=headers, params=params, data=data, proxy=proxy) as request:
				data = await request.read()
				return data.decode('utf-8')

	async def semGet(self, url, session, headers={}, params={}, data=None, proxy=None, generator=False):
		async with self.sem as sem:
			async with session.get(url, headers=headers, params=params, proxy=proxy, data=data) as request:
				data = await request.read()
				if generator:
					return request
				return data.decode('utf-8')

async def main():
	futures = []
	sem = asyncio.Semaphore(1000)
	for i in range(int(sys.argv[2])):
		futures.append(bot(sem).start())
	
	wait = asyncio.gather(*futures)
	await wait

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())