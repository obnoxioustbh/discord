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

#sys.argv = ['', 'https://discord.gg/UbQaM', 'accounts.txt']

def dprint(data):
	print(data)
	sys.stdout.flush()


class spammer:
	def __init__(self, authorization, invID, sem, message, channel):
		self.message = message
		self.sem = sem
		self.proxy = 'http://us1.proxies.online:8182'
		self.id = invID
		self.auth = authorization
		self.channel = channel
		return

	def dprint(self, data):
		print(data)
		sys.stdout.flush()

	async def start(self):
		async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Authorization': self.auth}, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
			try:
				join = await self.joinServer(session)
				joinJson = json.loads(join)

				if self.channel:
					async with session.get('https://discordapp.com/api/guilds/{0}/channels'.format(joinJson['guild']['id'])) as resp:
						kek = await resp.json()
						for channel in kek:
							if channel['name'] == self.channel:
								channelID = channel['id']
				else:
					channelID = joinJson['channel']['id']
				
				self.dprint('[+] Joined: {0}'.format(channelID))
				for i in range(15):
					randomExtra = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
					message = await self.messageChannel(channelID, session, '{0} {1}'.format(self.message, randomExtra))
					await asyncio.sleep(4)
			except Exception as e:
				self.dprint(e)
				return
				

	async def messageChannel(self, cid, session, message):
		return await self.semPost('https://discordapp.com/api/v6/channels/{0}/messages'.format(cid), session, proxy=self.proxy,
			headers={
				'content-type':'application/json',
				'origin':'https://discordapp.com',
				'referer':'https://discordapp.com/channels/{0}/{0}'.format(cid),
				'accept':'*/*',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'en-US',
			},
			data=json.dumps({'content': message, 'nonce': "302048676446994432", 'tts': False}))

	async def joinServer(self, session):
		return await self.semPost('https://discordapp.com/api/v6/invite/{0}'.format(self.id), session, proxy=self.proxy,
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

async def main(invite, message, channel):
	try:
		if '#' in channel:
			channel = channel.replace('#', '')
	except:
		channel = ''
	invID = invite.split('/')[-1]
	dprint(invID)
	accounts = open('accounts.txt', 'r').readlines()
	sem = asyncio.Semaphore(100)
	tasks = []

	shuffle(accounts)

	for account in range(50):
		account = accounts[account]
		username, password, email, authorization = account.strip().rstrip().split(':')
		tasks.append(asyncio.ensure_future(spammer(authorization, invID, sem, message, channel).start()))
		tasks.append(asyncio.ensure_future(wss(authorization, sem)))

	wait = asyncio.gather(*tasks)
	await wait


def nonMain(message, invite, channel):
	dprint([message, invite])
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main(invite, message, channel))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main("https://discord.gg/NCUzQ", "cocks", "general"))

"""
			except aiohttp.errors.ServerDisconnectedError:
				return

			except aiohttp.errors.HttpProxyError:
				return

			except aiohttp.errors.ClientResponseError:
				return

			except aiohttp.errors.ClientOSError:
				return
"""
