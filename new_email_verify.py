import imaplib
import verifier
import glob

from time import sleep

verificationUrls = []

emlFiles = glob.glob('emails/*.eml')
for file in emlFiles:
	with open(file, 'r') as fileData:
		data = fileData.read()
		verificationToken = data.split('https://discordapp.com/verify?token=')[1].split()[0].strip().rstrip()
		verificationUrls.append(verificationToken)

print('[+] Got {0} verification URLs'.format(len(verificationUrls)))

emailVerifier = verifier.main(verificationUrls)