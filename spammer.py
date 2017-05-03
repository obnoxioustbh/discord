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
from random import randint
#sys.argv = ['', 'https://discord.gg/UbQaM', 'accounts.txt']

def dprint(data):
	print(data)
	sys.stdout.flush()


class spammer:
	def __init__(self, authorization, invID, sem, message, channel, uid):
		self.uid = uid
		self.message = message
		self.sem = sem
		self.proxy = 'http://gw.proxies.online:8081'
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

				async with session.patch('https://discordapp.com/api/v6/users/@me/settings', headers={'Content-Type': 'application/json'}, data=json.dumps({'status': 'invisible'}), proxy=self.proxy) as resp:
					theJSON = await resp.json()

				join = await self.joinServer(session)
				joinJson = json.loads(join)

				blackList = ['308106118545276930']
				if joinJson['guild']['id'] in blackList:
					return

				if self.uid:
					async with session.get('https://discordapp.com/api/v6/users/@me', proxy=self.proxy) as resp:
						theJSON = await resp.json()
						meUID = theJSON['id']

					async with session.post('https://discordapp.com/api/v6/users/{0}/channels'.format(meUID), data=json.dumps({'recipients': [self.uid]}), headers={'Content-Type': 'application/json'}, proxy=self.proxy) as resp:
						theJSON = await resp.json()
						channelToMsg = theJSON['id']

					for i in range(randint(14, 29)):
						randomExtra = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(1, 10))).swapcase()
						secondExtra = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(1, 10))).swapcase()
						await self.messageChannel(channelToMsg, session, '{1} {0} {2}'.format(self.message, randomExtra, secondExtra).swapcase())
						print('[+] Messages Sent: {0}'.format(i))
						await asyncio.sleep(randint(1, 7))

					return

				if self.channel:
					channels = []
					async with session.get('https://discordapp.com/api/guilds/{0}/channels'.format(joinJson['guild']['id']), proxy=self.proxy) as resp:
						kek = await resp.json()
						for channel in kek:
							channels.append(channel['id'])
				else:
					channelID = joinJson['channel']['id']
					channels = [channelID]

				self.dprint('[+] Joined!')
				for i in range(randint(4,16)):
					for channel in channels:
						randomExtra = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(randint(1, 10))).swapcase()
						secondExtra = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(randint(1, 10))).swapcase()
						message = await self.messageChannel(channel, session, '{1} {0} {2}'.format(self.message, randomExtra, secondExtra).swapcase())
						print('[+] Messages Sent: {0}'.format(i))
						await asyncio.sleep(randint(1, 7))

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
			await websocket.send(json.dumps({"t":"USER_SETTINGS_UPDATE","s":2,"op":0,"d":{"status":"invisible"}}))
			await asyncio.sleep(120)
			return
	except:
		return

async def main(invite, message, channel, uid):
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

	for account in range(randint(9, 26)):
		account = accounts[account]
		username, password, email, authorization = account.strip().rstrip().split(':')
		tasks.append(asyncio.ensure_future(spammer(authorization, invID, sem, message, channel, uid).start()))
		tasks.append(asyncio.ensure_future(wss(authorization, sem)))
		await asyncio.sleep(randint(1, 7))

	wait = asyncio.gather(*tasks)
	await wait


def nonMain(message, invite, channel, uid):
	dprint([message, invite])
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main(invite, message, channel, uid))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main("https://discord.gg/SxtDs", "cocks", None, None))
