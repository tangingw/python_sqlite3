import socket
from sqlite3_crypto import CryptoBot


def main():

	server_host = "127.0.0.1"
	server_port = 8082

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	password = "test1234"
	key = CryptoBot.generate_key(password)

	try:

		s.connect((server_host, server_port))

		data = raw_input("Command: ")

		while data != "QUIT" and data !="quit":

			encrypt_data = CryptoBot.encrypt(data, key)
			s.send(encrypt_data)

			encrypt_data_recv = s.recv(4096)
			data_recv = CryptoBot.decrypt(encrypt_data_recv, key)		

			if not data_recv:
			
				print "Server closed!"
				break
		
			else:

				print "Received: %s" % data_recv

				data = raw_input("Command: ")

	

		s.close()

	except socket.error:

		print "Server %s:%d cannot be reached!" % (server_host, server_port)


if __name__ == '__main__':

	main()
