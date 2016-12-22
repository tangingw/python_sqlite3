# python_sqlite3
This is sqlite3 remote server and client, written in python

Manual:
  1. Edit the db_server.ini by inserting IP, port and path for sqlite3 DB file
  2. Run the server:
  
     ```
      Terminal$> python server.py
     ```
     
Client side:
  1. On another terminal, run the client
  
     ```
     Terminal$> python client.py
     Command: select * from `Table`;
     Received: Result
     ```
