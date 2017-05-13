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

class spammer:
	def __init__(self, token=None, message=None, invite=None, channel=None, uid=None):
		self.invite = invite
		self.token = token
		self.messageContent = message
		self.uid = uid		
		self.channel = channel
		
		self.channels = []
		self.proxy = 'http://gw.proxies.online:8081'
		self.message = '{message} {random}'

		return

	async def start(self):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
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
					else:	
						await self.getAllChannels(session)
					
					await self.attackAllChannels(session)
					return
			except:
				continue

	async def createPMChannel(self, session):
		async with session.post(
			'https://discordapp.com/api/v6/users/{0}/channels'.format(self.meID), 
				data=json.dumps({'recipients': [self.uid]}),
				headers={'Content-Type': 'application/json'}, 
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
				self.channels.append(channel['id'])
			return resp

	async def attackAllChannels(self, session):
		for i in range(15):
			for cID in self.channels:
				self.messageSent = await self.sendMessage(session, cID)
			await asyncio.sleep(randint(0,1))

	async def sendMessage(self, session, cID):
		async with session.post(
			'https://discordapp.com/api/v6/channels/{0}/messages'.format(cID), 
				proxy=self.proxy, 
				headers={'Content-Type': 'application/json'},
				data=json.dumps({'content': self.message.format(random=self.generateSomeRandomCharacters(), message=self.messageContent), 'nonce': randint(1000000000000000000, 9000000000000000000)}),
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

	def generateSomeRandomCharacters(self):
		return ''.join(random.choice(string.ascii_lowercase) for _ in range(randint(1,2)))

async def main(invite, message, channel, uid, tasks=[]):
	if '/' in invite:
		invite = invite.split('/')[-1]

	print('here')

	accounts = open('accounts.txt', 'r').readlines()
	shuffle(accounts)

	for account in accounts[0:15]:
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
	loop.run_until_complete(main('https://discord.gg/h63jw', 'test', 'all', None))