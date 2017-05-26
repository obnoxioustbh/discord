import asyncio
import json
import aiohttp
import random
import string
import sys

from aiohttp import ClientSession
from aiohttp import TCPConnector
from random import shuffle
from random import randint
from random import choice

class spammer:
	def __init__(self, token=None, message=None, invite=None, channel=None, uid=None):
		self.invite = invite
		self.token = token
		self.messageContent = message
		self.uid = uid		
		self.channel = channel
		self.sent = 0
		self.channels = []
		self.proxy = choice(['http://us1.proxies.online:8182', 'http://gw.proxies.online:8081', 'http://gw.proxies.online:8104', 'http://gw.proxies.online:8100', 'http://gw.proxies.online:8101', 'http://gw.proxies.online:8102', 'http://gw.proxies.online:8103'])
		self.message = '{message} {random}'

		return

	async def start(self):
		headers = {
			'User-Agent': choice(['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']),
			'Content-Type': 'application/json',
			'Authorization': self.token,
		}

		connector = TCPConnector(verify_ssl=False)

		for i in range(3):
			try:
				async with ClientSession(headers=headers, connector=connector) as session:
					self.joinJSON = await self.joinServer(session)
					self.guildID = self.joinJSON['guild']['id']
 
					if self.uid:
						self.meID = await self.getMeID(session)
						await self.createPMChannel(session)
					

					await self.getAllChannels(session)
					await self.attackAllChannels(session)
					return
			except:
				continue

	async def leaveServer(self, session):
		async with session.delete('https://discordapp.com/api/v6/users/@me/guilds/{0}'.format(self.guildID)) as request:
			try:
				resp = await request.read()
				return resp
			except:
				return False


	async def createPMChannel(self, session):
		async with session.post(
			'https://discordapp.com/api/v6/users/{0}/channels'.format(self.meID), 
				data=json.dumps({'recipients': [self.uid]}),
				proxy=self.proxy
			) as resp:
			resp = await resp.json()
			self.channels.append(resp['id'])
			return resp

	async def getMeID(self, session):
		async with session.get('https://discordapp.com/api/v6/users/@me', proxy=self.proxy) as resp:
			resp = await resp.json()
			return resp['id']

	async def getAllChannels(self, session):
		async with session.get(
			'https://discordapp.com/api/guilds/{0}/channels'.format(self.guildID),
				proxy=self.proxy,
			) as request:
			resp = await request.json()
			for channel in resp:
				if channel['type'] == 'voice':
					continue
				self.channels.append(channel['id'])
			return resp

	async def attackAllChannels(self, session):
		for i in range(15):
			await self.joinServer(session)
			for cID in self.channels:
				self.messageSent = await self.sendMessage(session, cID)
				try:
					if self.messageSent['code']:
						print('[+] Flagged for verification, exiting.')
					return
				except:
					pass

				try:


					if not self.messageSent['nonce']:
						self.sent += 1
						print('[+] Messages Sent: {0}'.format(self.sent))
				except:
					pass
				await self.humanSleep()
			await self.humanSleep()
		#await self.leaveServer(session)

	async def sendMessage(self, session, cID):
		async with session.post(
			'https://discordapp.com/api/v6/channels/{0}/messages'.format(cID), 
				proxy=self.proxy, 
				data=json.dumps({'content': self.message.format(random=self.generateSomeRandomCharacters(), message=self.messageContent)}),
			) as request:
			resp = await request.json()
			return resp

	async def joinServer(self, session):
		async with session.post(
			'https://discordapp.com/api/v6/invite/{0}'.format(self.invite), 
				proxy=self.proxy
			) as request:
			resp = await request.json()
			return resp

	async def humanSleep(self):
		return await asyncio.sleep(random.uniform(0.0, 0.2))

	def generateSomeRandomCharacters(self):
		return ''.join(random.choice(string.ascii_lowercase) for _ in range(randint(0,6)))

async def main(invite, message, channel, uid, tasks=[]):
	if '/' in invite:
		invite = invite.split('/')[-1]

	accounts = open('accounts.txt', 'r').readlines()
	shuffle(accounts)

	for account in accounts[0:21]:
		try:
			username, password, email, token = account.strip().rstrip().split(':')
		except ValueError:
			continue
		tasks.append(asyncio.ensure_future(spammer(token=token, message=message, invite=invite, uid=uid).start()))
	
	await asyncio.gather(*tasks)

def nonMain(message, invite, channel, uid):
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main(invite, message, channel, uid))

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	if len(sys.argv) < 1:
		sys.exit(0)
	try:
		uid = sys.argv[2]
	except:
		uid = None
	loop.run_until_complete(main(sys.argv[1], open('message.txt', 'r').read(), 'all', uid))