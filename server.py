import ConfigParser
import socket
import sqlite3
import signal
import sys
import json
import time
from sqlite3_crypto import CryptoBot


def get_config():

        config = ConfigParser.ConfigParser()
        config.read("db_server.ini")

        config_dict = dict()

        for section in config.sections():

                for option in config.options(section):

                        config_dict[option] = config.get(section, option)

        return config_dict


def database_executer(client_socket, key, curr, sql_command):


	def send_encrypt_msg(message, key):
		
		cipher_text = CryptoBot.encrypt(message, key)
                client_socket.send(cipher_text)

	
	try:	

		curr.execute(sql_command)
	
	except sqlite3.OperationalError:
	
		send_encrypt_msg("Syntax_Error", key)
		
	else:

		sql_command_list = sql_command.split(" ")

		if sql_command_list[0] == "SELECT" or sql_command_list[0] == "select":
			
			send_encrypt_msg(json.dumps({"response": curr.fetchall()}), key)

		elif sql_command_list[0] == "CREATE" or sql_command_list[0] == "create":

			send_encrypt_msg("Table " + sql_command_list[1] + " created!", key)

		elif sql_command_list[0] == "INSERT" or sql_command_list[0] == "insert":
		
			send_encrypt_msg("Value/s inserted into the Table", key)
 
		elif sql_command_list[0] == "UPDATE" or sql_command_list[0] == "update":

			send_encrypt_msg("Table " + sql_command_list[1] + " updated!", key)

		else:
			send_encrypt_msg("Command not Found!", key)


class SQLITE_Socket(object):

	def __init__(self, sock=None):

		self.config = get_config()
		self.host = self.config["host_address"]
		self.port = int(self.config["port"])
		self.db_path = self.config["path"]
		self.key = CryptoBot.generate_key("test1234")


		if sock is None:

			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		else:

			self.sock

		self.sock.bind((self.host, self.port))

	def listen(self):

		self.sock.listen(5)
		conn = sqlite3.connect(self.db_path)
		curr = conn.cursor()		

		#commit_keyword_list = ["COMMIT", "commit"]
		#close_keyword_list = ["CLOSE", "close"]
		
		try:
			while True:

				client_socket, addr = self.sock.accept()
				print "%s: %s:%s connected!" % (time.ctime(time.time()), addr[0], addr[1])

				while True:

					try:
					
						encrypt_data_recv = client_socket.recv(4096)
						data_recv = CryptoBot.decrypt(encrypt_data_recv, self.key)

					except:
					
						print "Connection reset by peers!"
						break

					else:
				
						if not data_recv:

							break

						else:

							"""if data_recv in commit_keyword_list:

                                                		curr.close()
                                                		conn.commit()
								break
		
                                        		elif data_recv in close_keyword_list:

								curr.close()
                                                		break

                                        		else:
							
								print data_recv
                                                		database_checker(client_socket, curr, data_recv)
						
							"""

							print "%s: %s: %s" % (time.ctime(time.time()), addr[0], data_recv)
                                                	database_executer(client_socket, self.key, curr, data_recv)
			
		
			#conn.commit()
			curr.close()
			client_socket.close()

		except KeyboardInterrupt:
		
			conn.close()
			self.sock.close()
			print "Server shutdown\n"

def main():

	conn = SQLITE_Socket()
	conn.listen()


if __name__ == '__main__': 

	main()
