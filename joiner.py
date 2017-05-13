import asyncio
import aiohttp
import time
import random
import sys
import json
import websockets
import random
import string

from random import shuffle

def dprint(data):
	print(data)
	sys.stdout.flush()


class spammer:
	def __init__(self, authorization, invID):
		self.proxy = 'http://us1.proxies.online:8182'
		self.id = invID
		self.auth = authorization
		return

	def dprint(self, data):
		print(data)
		sys.stdout.flush()

	async def start(self):
		async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Authorization': self.auth}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
			try:
				join = await self.joinServer(session)
				joinJson = json.loads(join)
			except Exception as e:
				self.dprint(e)
				return

	async def joinServer(self, session):
		return await self.semPost('https://discordapp.com/api/v6/invite/{0}'.format(self.id), session, #proxy=self.proxy,
			headers={
				'accept':'*/*',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'en-US',
				'origin':'https://discordapp.com',
				'referer':'https://discordapp.com/channels/@me',
				'x-context-properties': 'eyJMb2NhdGlvbiI6IkpvaW4gYSBTZXJ2ZXIgTW9kYWwifQ==',
				'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIn0',
			})

	async def semPost(self, url, session, headers={}, params={}, data=None, proxy=None):
		async with session.post(url, headers=headers, params=params, data=data, proxy=proxy) as request:
			data = await request.read()
			return data.decode('utf-8')

	async def semGet(self, url, session, headers={}, params={}, data=None, proxy=None, generator=False):
		async with session.get(url, headers=headers, params=params, proxy=proxy, data=data) as request:
			data = await request.read()
			if generator:
				return request
			return data.decode('utf-8')

async def wss(auth, sem):
	try:
		WSS_URL = 'wss://gateway.discord.gg/?encoding=json&v=6'
		async with websockets.connect(WSS_URL) as websocket:
			await websocket.send(json.dumps({"op":2,"d":{"token":auth,"properties":{"os":"Windows","browser":"Chrome","device":"","referrer":"","referring_domain":""},"large_threshold":100,"synced_guilds":[],"presence":{"status":"online","since":0,"afk":False,"game":None},"compress":True}}))
			await asyncio.sleep(120)
			return
	except:
		return

async def main(invite):
	try:
		if '#' in channel:
			channel = channel.replace('#', '')
	except:
		channel = ''
	invID = invite.split('/')[-1]
	accounts = open(sys.argv[2], 'r').readlines()
	tasks = []

	shuffle(accounts)

	for account in range(len(accounts)):
		account = accounts[account]
		username, password, email, authorization = account.strip().rstrip().split(':')
		tasks.append(asyncio.ensure_future(spammer(authorization, invID).start()))
		await asyncio.sleep(0.01)
		#tasks.append(asyncio.ensure_future(wss(authorization, sem)))

	wait = asyncio.gather(*tasks)
	await wait

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(sys.argv[1]))