from datetime import datetime
import asyncore
from smtpd import SMTPServer

class EmlServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        if 'Verify Email' in data:
            print('Got a EMAIL VERIFICATION')
            token = data.split('https://discordapp.com/verify?token=')[1].split('"')[0]
            print(token)

def run():
    foo = EmlServer(('0.0.0.0', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()