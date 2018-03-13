# Remote SQLITE3 Server and Client
This is sqlite3 remote server and client, written in python

Server side:
  1. Edit the db_server.ini by inserting IP, port, path and password for sqlite3 DB file.
  2. Run the server:
  
     ```
      Terminal$> python server.py
     ```
     
Client side:
  1. Open client.py using any editor.
  2. Enter the IP address, port and password of the server.
  3. On another terminal, run the client.
  
     ```
     Terminal$> python client.py
     Command: select * from `Table`;
     Received: Result
     ```
### Features added:
  * Multithreading features - manage to support more than 2 users

### Problem to be solved
  * Race condition between 2 users
    Solution: Consumer and Producer model (to be appeared in the next rolling)

