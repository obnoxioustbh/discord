import json
import os
import signal
import spammer
import datetime
import requests
import attack

from multiprocessing import Process
from flask import Flask
from flask import request
from flask import render_template
from bson.codec_options import CodecOptions
from pymongo.collation import Collation
from pymongo import MongoClient

app = Flask(__name__)

runningAttacks = {}

client = MongoClient('mongodb://93.190.142.215', 27017)
db = client.get_database('admin', codec_options=CodecOptions(unicode_decode_error_handler='ignore'))
print('Signed in: {0}'.format(db.authenticate('admin', '.gpe7h+99W:P}gU}')))
collection24h = db['discord']
collection2w = db['discord_2weeks']
collection1m = db['discord_1month']
collectionLifetime = db['discord_lifetime']

collections = [collection24h, collection2w, collection1m, collectionLifetime]

def stopAttack(authcode):
	os.kill(runningAttacks[authcode], signal.SIGTERM)
	return {'authcode': authcode, 'stopped': True}

def sendAttack(message=None, invite=None, authcode=None, channel=None, uid=None):
	process = Process(target=attack.nonMain, args=[message, invite, channel, uid])
	process.start()
	pid = process.pid
	runningAttacks[authcode] = pid
	return {'message': message, 'invite': invite, 'authcode': authcode, 'sent': True, 'pid': pid}

def getParams(request):
	return {
		'action': request.args.get('action'), 
		'authcode': request.args.get('authcode'),
		'message': request.args.get('message'),
		'invite': request.args.get('invite'),
		'channel': request.args.get('channel'),
		'uid': request.args.get('uid')
	}

def isAuthorized(code, authorized=False):
	authCodes = []
	for collection in collections:
		for acode in collection.find():
			authCodes.append(acode['code'])
	
	print(authCodes)

	for acode in authCodes:
		if code == acode:
			authorized = True

	print(authorized)

	return authorized
#	return authorized

def error_payment(data):
	data = str(data)
	with open(PAYMENT_ERROR_FILE) as ERROR_FILE:
		print('ERROR: {0}'.format(data), file=ERROR_FILE)

@app.route('/payment', methods=['GET'])
def payment():
	return render_template('payment.html')

@app.route('/paymentSECRETASFUCKBOY', methods=['POST'])
def ipn():

	print(request.data)

	PRODUCT_IDS = {'d998698e': ['86400', collection24h], '7572afa1': ['1209600', collection2w], 'ef5f4af1': ['2592000', collection1m], '6bbd9475': ['0', collectionLifetime]}
	PAYMENT_ERROR_FILE = 'errors.txt'

	try:
		data = request.data.decode('utf-8')
	except:
		data = request.data

	headers = {
		'X-Auth-Email': 'i.am@obnoxious.eu',
		'X-Auth-Key': '7H-rshyU6x-JbemzWkbFKXPysxSdLWPBrsoDLWXs4JrdZnrB-A',
	}

	try:
		theJSON = json.loads(data)
	except:
		print('invalid json...')
		
	if theJSON['product_id'] in PRODUCT_IDS:
		ORDER_ID = theJSON['id']
		time = PRODUCT_IDS[theJSON['product_id']][0]
		if theJSON['product_id'] != "6bbd9475":
			code = requests.get('https://selly.gg/api/orders/{0}'.format(ORDER_ID), headers=headers, proxies={'http': 'http://us1.proxies.online:8182', 'https': 'http://us1.proxies.online:8182'}).json()['delivered']
			print(code)
			PRODUCT_IDS[theJSON['product_id']][1].insert({'createdAt': datetime.datetime.utcnow(), 'logEvent': 2, 'logMessage': 'Success!', 'code': code})
		else:
			PRODUCT_IDS[theJSON['product_id']][1].insert({'code': code})
		print({'code': code, 'time': time})
	else:
		error_payment(theJSON)
	return str(theJSON)

@app.route('/stop')
def stop():
	params = getParams(request)
	
	if params['authcode']:
		try:
			authorized = isAuthorized(params['authcode'])
			stop = stopAttack(params['authcode'])
			return render_template('new_index.html', log='Stopped attack successfully', authcode=params['authcode'])
		except:
			return render_template('new_index.html', log='Failed to stop attack', authcode=params['authcode'])
	return render_template('new_index.html', log='Failed to stop attack.', authcode=params['authcode'])

@app.route('/start')
def start():
	params = getParams(request)

	if params['authcode'] and params['message'] and params['invite']:
		try:
			stopAttack(params['authcode'])
		except:
			pass

		channel = params['channel']

		authorized = isAuthorized(params['authcode'])
		if authorized:
			print("{0}:{1}:{2}".format(params['invite'], params['message'], params['authcode']), file=open('attacks.txt', 'a'))
			start = sendAttack(message=params['message'], invite=params['invite'], authcode=params['authcode'], channel=channel, uid=params['uid'])
		else:
			return render_template('new_index.html', log='Failed to start attack.', authcode=params['authcode'])

		return render_template('new_index.html', log='Started attack successfully on {0} sending {1}'.format(params['invite'], params['message']), authcode=params['authcode'])

	return render_template('new_index.html', log='Failed to start attack.', authcode=params['authcode'])

@app.route('/')
def discord():
	#return 'Downtime for a few days at most, super busy and I need to work on the whole project, people will be given time for this. Sorry.'
	return render_template('new_index.html', log="Ready for an attack!")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)