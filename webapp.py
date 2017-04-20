import json
import os
import signal
import spammer
import datetime

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

def sendAttack(message=None, invite=None, authcode=None):
	process = Process(target=spammer.nonMain, args=[message, invite])
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
	}

def isAuthorized(code, authorized=False):
	authCodes = []
	for collection in collections:
		for acode in collection.find():
			authCodes.append(acode['code'])
	
	for acode in authCodes:
		if code == acode:
			authorized = True

	return authorized

def error_payment(data):
	data = str(data)
	with open(PAYMENT_ERROR_FILE) as ERROR_FILE:
		print('ERROR: {0}'.format(data), file=ERROR_FILE)

@app.route('/paymentSECRETASFUCKBOY', methods=['POST'])
def ipn():
	PRODUCT_IDS = {'d998698e': ['86400', collection24h], '7572afa1': ['1209600', collection2w], 'ef5f4af1': ['2592000', collection1m], '6bbd9475': ['0', collectionLifetime]}
	PAYMENT_ERROR_FILE = 'errors.txt'

	data = request.data
	theJSON = json.loads(data)
	if theJSON['product_id'] in PRODUCT_IDS:
		time = PRODUCT_IDS[theJSON['product_id']][0]
		code = theJSON['delivered']
		if theJSON['product_id'] != "6bbd9475":
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
		authorized = isAuthorized(params['authcode'])
		start = sendAttack(message=params['message'], invite=params['invite'], authcode=params['authcode'])
		return render_template('new_index.html', log='Started attack successfully on {0} sending {1}'.format(params['invite'], params['message']), authcode=params['authcode'])

	return render_template('new_index.html', log='Failed to start attack.', authcode=params['authcode'])

@app.route('/')
def discord():
	return render_template('new_index.html', log="Ready for an attack!")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

"""
	if params['action'] and params['authcode']:
		authorized = isAuthorized(params['authcode'])

		if authorized:
			if params['action'] == 'attack':
				attack = sendAttack(message=params['message'], invite=params['invite'], authcode=params['authcode'])
				return render_template('new_index.html', log=str(attack))

			elif params['action'] == 'stop':
				stop = stopAttack(params['authcode'])
				return render_template('new_index.html', log=str(stop))
"""