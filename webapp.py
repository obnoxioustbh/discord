import json
import os
import signal
import spammer

from multiprocessing import Process

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

runningAttacks = {}

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

def isAuthorized(code):
	authCodes = json.loads(open('auth.json', 'r').read())
	if code in authCodes['codes']:
		return True
	else:
		return False

@app.route('/paymentSECRETASFUCKBOY')
def ipn():
	data = web.data()
	print(data)
	return data

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