import asyncio
import aiohttp
import websockets
import json

from random import randint

class stallOnline:
	def __init__(self, token):
		self.wssURL = 'wss://gateway.discord.gg/?encoding=json&v=6'
		self.token = token
		self.count = 0
		print('[+] Starting Online Process for {0}'.format(token))
		return

	async def start(self):
		async with websockets.connect(self.wssURL) as self.discord:
			await self.discord.send(json.dumps({"op":2,"d":{"token":self.token,"properties":{"os":"Windows","browser":"Chrome","device":"","referrer":"","referring_domain":""},"large_threshold":100,"synced_guilds":[],"presence":{"status":"invisible","since":0,"afk":False,"game":None},"compress":True}}))
			
			try:

				self.buffer = json.loads(await self.discord.recv())
				if self.buffer['s'] != None:
					self.count = self.buffer['s']

			except UnicodeDecodeError:

				print('[!] Binary Frame Detected')

			while True:
				await self.discord.send(json.dumps({"op":1,"d":self.count}))
				try:
					self.buffer = json.loads(await self.discord.recv())
					if self.buffer['s'] != None:
						self.count = self.buffer['s']

				except UnicodeDecodeError:
					print('[!] Binary Frame Detected')
				
				print('[+] Sleeping for 5 seconds')
				await asyncio.sleep(randint(5, 15))
				self.count += 1

async def main(tasks=[]):
	accounts = open('accounts.txt', 'r').readlines()

	for account in accounts:
		username, password, email, token = account.strip().rstrip().split(':')
		tasks.append(asyncio.ensure_future(stallOnline(token).start()))
	
	await asyncio.gather(*tasks)
	

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main())