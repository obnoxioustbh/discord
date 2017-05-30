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

sys.argv = ['', 'accounts.txt', 15]

class bot:
	def __init__(self, sem):
		self.sem = sem
		self.proxy = 'http://gw.proxies.online:8081'
		self.googleKey = '6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn'	
		self.captchaKey = '5239dcfa969c0f7e3ecfaac6e1924e95'
		self.username = self.generateName()
		self.password = '{0}{0}'.format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(4,9))))
		self.fingerprint = '{0}.{1}'.format(self.random(randint(13,18)), ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +string.digits) for _ in range(randint(5, 35))))
		self.superproperties = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(80, 112)))
		try:
			vrorandom = sys.argv[3]
			self.email = "{0}@gmail.com".format(''.join(choice(string.ascii_lowercase) for _ in range(randint(3,9))), ''.join(choice(string.ascii_lowercase) for _ in range(randint(3,9))))
		except:
			self.email = "{0}@nwejghiwejh.gq".format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(1,9))))
		print(self.email)

	def random(self, n):
		range_start = 10**(n-1)
		range_end = (10**n)-1
		return randint(range_start, range_end)

	def generateName(self, count=2, fillers=2, name=''):
		fillers = ['', '_', 'x', 'v', 'ii', '_', '-', 'vv', 'LL']
		names = open('parsed.txt', 'r').readlines()
		for i in range(count):
			name += choice(fillers)
			name += choice(names).strip().rstrip()

		name += choice(fillers)

		return name

	async def start(self):
		try:
			async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'X-Fingerprint': self.fingerprint, 'X-Super-Properties': self.superproperties}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
				kek = await self.captcha(session)
				index = await self.index(session)
				await asyncio.sleep(5)
				account = await self.register(session)
				token = json.loads(account)['token']
				print('[+] Successfully Created Account')
				print('{0}:{1}:{2}:{3}'.format(self.username, self.password, self.email, token))
				print('{0}:{1}:{2}:{3}'.format(self.username, self.password, self.email, token), file=open(sys.argv[1], 'a'))
				print(account)
		except Exception as e:
			try:
				print(account)
			except:
				return
			print('EXCEPTION: {0}'.format(e))
			return	

	async def captcha(self, session):
		async with session.get('http://2captcha.com/in.php?key={0}&method=userrecaptcha&googlekey=6Lef5iQTAAAAAKeIvIY-DeexoO3gj7ryl9rLMEnn&pageurl=https://discordapp.com/register'.format(self.captchaKey)) as resp:
			CID = await resp.read()
			CID = CID.decode('utf-8').split('|')[1]
			#print(CID)

		print('[+] Waiting captcha')

		while True:
			async with session.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self.captchaKey, CID)) as resp:
				RES = await resp.read()
				RES = RES.decode('utf-8').split('|')
				
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
			proxy=self.proxy
		)

	async def register(self, session):
		return await self.semPost('https://discordapp.com/api/v6/auth/register', session, 
			data=json.dumps(
				{
					'email': self.email, 
					'username': self.username, 
					'password': self.password, 
					'invite': None, 
					'captcha_key': self.theCaptcha,

				}
			), 
			headers={
				'Content-Type': 'application/json',
				'Referer': 'https://discordapp.com/register',
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

