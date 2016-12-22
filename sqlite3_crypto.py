import binascii
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class CryptoBot(object):

	@staticmethod
	def generate_key(password):

		if len(password) >= 8:
	
			digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
			digest.update(password)
	
			return base64.urlsafe_b64encode(digest.finalize())

		return "Password Length less than 8"

	@staticmethod
	def encrypt(message, key):

		key_token = Fernet(key)
		cipher_text = key_token.encrypt(message)

		return cipher_text

	@staticmethod
	def decrypt(cipher_text, key):
		
		key_token = Fernet(key)

		return key_token.decrypt(bytes(cipher_text)) 


#key = CryptoBot.generate_key("How are you!")
#message = "Fine. Thank you!"

#print CryptoBot.encrypt(message, key)
#print CryptoBot.decrypt(CryptoBot.encrypt(message, key), key)
