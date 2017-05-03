import aiohttp
import asyncio
import sys
import random
import time
import json
import string

from random import choice
from random import randint
from GmailDotEmailGenerator import GmailDotEmailGenerator

#sys.argv = ['', 'accounts.txt', 120]

class bot:
	def __init__(self, sem):
		self.sem = sem
		self.proxy = 'http://gw.proxies.online:8081'
		self.googleKey = '6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn'	
		self.captchaKey = '5239dcfa969c0f7e3ecfaac6e1924e95'
		self.username = '{0}{0}'.format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(3,9))))
		self.password = '{0}{0}'.format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(3,9))))
		self.fingerprint = '{0}.{1}'.format(self.random(18), ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +string.digits) for _ in range(randint(10, 27))))
		self.superproperties = ''.join(random.choice(string.ascii_uppercase +  + string.ascii_lowercase + string.digits) for _ in range(randint(100, 112)))
		self.domains = ['hugweuighjwegiojk.dress-code.si', 'ewgwegwehwhweh.isok.info', 'wegwehwhwhwhe.opt-inrewards.com']
		self.domain = choice(self.domains)
		if '*' in self.domain:
			self.domain = self.domain.replace('*', ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(randint(3,15))))
		self.email = '{0}@{1}'.format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(10,27))), self.domain)
		print(self.email)

	def random(self, n):
		range_start = 10**(n-1)
		range_end = (10**n)-1
		return randint(range_start, range_end)

	async def start(self):
		try:
			async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
				kek = await self.captcha(session)
				index = await self.index(session)
				account = await self.register(session)
				token = json.loads(account)['token']
				print('{0}:{1}:{2}:{3}'.format(self.username, self.password, self.email, token), file=open(sys.argv[1], 'a'))
		except Exception as e:
			print('EXCEPTION: {0}'.format(e))
			return	

	async def captcha(self, session):
		async with session.get('http://2captcha.com/in.php?key={0}&method=userrecaptcha&googlekey=6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn&pageurl=https://discordapp.com/register'.format(self.captchaKey)) as resp:
			CID = await resp.read()
			CID = CID.decode('utf-8').split('|')[1]
			#print(CID)

		while True:
			async with session.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self.captchaKey, CID)) as resp:
				RES = await resp.read()
				RES = RES.decode('utf-8').split('|')
				print('[+] Waiting captcha')
				if 'CAPCHA_NOT_READY' in RES[0]:
					await asyncio.sleep(3)
					continue
				else:
					self.theCaptcha = RES[1]
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
					'captcha_key': self.theCaptcha,

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
