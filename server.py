import ConfigParser
import socket
import sqlite3
import signal
import sys
import json
import time
import threading 
from sqlite3_crypto import CryptoBot


def get_config():

    config = ConfigParser.ConfigParser()
    config.read("db_server.ini")

    config_dict = dict()

    for section in config.sections():

        for option in config.options(section):

            config_dict[option] = config.get(section, option)

    return config_dict

class SQLiteDB(object):

	def __init__(self):
    	
		self.__config = get_config()
		self.__db_path = self.__config["path"]
		self.__conn = sqlite3.connect(self.__db_path)
		self.__cursor = self.__conn.cursor()

	def shutdown_cursor(self):

		self.__cursor.close()
	
	def shutdown_connection(self):
    		
		self.__conn.close()

	def database_executer(self, client_socket, key, sql_command):

		def send_encrypt_msg(message, key):
		
			cipher_text = CryptoBot.encrypt(message, key)
			client_socket.send(cipher_text)

		try:	

			self.__cursor.execute(sql_command)
	
		except sqlite3.OperationalError:
	
			send_encrypt_msg("Syntax_Error", key)

		else:

			sql_command_list = sql_command.split(" ")

			if sql_command_list[0] == "SELECT" or sql_command_list[0] == "select":
			
				send_encrypt_msg(json.dumps({"response": self.__cursor.fetchall()}), key)

			elif sql_command_list[0] == "CREATE" or sql_command_list[0] == "create":

				self.__conn.commit()
				send_encrypt_msg("Table " + sql_command_list[1] + " created!", key)

			elif sql_command_list[0] == "INSERT" or sql_command_list[0] == "insert":
		
				self.__conn.commit()
				send_encrypt_msg("Value/s inserted into the Table", key)
 
			elif sql_command_list[0] == "UPDATE" or sql_command_list[0] == "update":

				self.__conn.commit()
				send_encrypt_msg("Table " + sql_command_list[1] + " updated!", key)

			else:
    			
				send_encrypt_msg("Command not Found!", key)


class SQLITE_Socket(object):

	def __init__(self, sock=None):

		self.__config = get_config()
		self.__host = self.__config["host_address"]
		self.__port = int(self.__config["port"])
		self.__password = self.__config["password"]
		self.__key = CryptoBot.generate_key(self.__password)

		if sock is None:

			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		else:
    		
			self.sock = sock

		self.sock.bind((self.__host, self.__port))
		self.sock.listen(5)

		self.clients = list()
    	
	def run(self):

		print("Server starts")

		try:
			self.accept_client()

		except Exception as ex:

			print(ex)

	def accept_client(self):
    		
		while True:

			client_socket, addr = self.sock.accept()
			self.clients.append(client_socket)

			print("%s: %s:%s connected!" % (time.ctime(time.time()), addr[0], addr[1]))

			server_thread = threading.Thread(target=self.receive, args=(client_socket, addr))
			server_thread.start()

	def receive(self, client_socket, addr):
    		
			while True:

				sqlite_db = SQLiteDB()

				try:
					
					encrypt_data_recv = client_socket.recv(4096)
					data_recv = CryptoBot.decrypt(encrypt_data_recv, self.__key)

				except:
					
					print("%s: Connection reset by peers!" % time.ctime(time.time()))
					sqlite_db.shutdown_connection()
					break

				else:
				
					if not data_recv:

						break

					else:
    						
						print("%s: %s: %s" % (time.ctime(time.time()), addr[0], data_recv))
						sqlite_db.database_executer(client_socket, self.__key, data_recv)

			self.clients.remove(client_socket)
			client_socket.close()


def main():

	conn = SQLITE_Socket()
	try:

		conn.run()	

	except KeyboardInterrupt:

		for client in conn.clients:
    				
			client.close()

		conn.sock.close()
		print("Server shutdown\n")


if __name__ == '__main__': 

	main()
