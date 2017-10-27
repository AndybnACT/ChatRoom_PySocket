# ChatRoom_PySocket
#### Requirements
There is no need to install any extra libraries. The program is running on Python 3.5 using the standard packages only.  
#### Usage
- Make sure that you are running on Python 3.5 or above
- **Set up the server side:** You should run the server-side script whenever you wish to start up a new chatroom.
   - 1. Make sure that your ip address is resolvable by clients
   - 2. Run the script with Python 3.5.
   - Server-Side Commands:
       - [mode]: show status all of clients
       - [close]: close connection of a particular client
       - [close all]: terminate all connections, shutdown the server
       - [broadcast]: send a server-side message to all clients
   - *Warnings:* Make sure that all member thread are terminated before shutting down the server gracefully.
- **Connect to the server from clients:** The member of the chatroom are implemented by client-side script. You could join a chatroom by specifying server's IP and port number  
   - 1. Modify variables ```portno``` and ```server_name``` to server's port number and IP address
   - Client-Side Commands:
       - [CLOSE]: leave the chatroom
       - [#*username*]: send unicast message to a user whose name is *username*
       - [##]: Get the latest members' information
#### Todo list
- [x] Automatically append clients whenever the server receives connections  (10/27/2017)
- [ ] FTP server
- [ ] Dump most recent records to new members
