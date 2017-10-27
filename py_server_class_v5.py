import socket
import sys
import threading
import time
import os
assert sys.version_info >= (3,5)

#### Default Seetings
port_no = 20039
rcv_buffer_size = 100
######################

########################## Get My IP address ##########################
print("Configuring...")
ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    ipsock.connect(("8.8.8.8", 80))
    host_name = ipsock.getsockname()[0]
    print("Your IP address is :%s" % ipsock.getsockname()[0])
    ipsock.close()
except:
    print("Can not resolve your public IP address")
    print("The chatroom would be started at localhost")
    print("Clients would be able to connect locally on '127.0.0.1' ")
    host_name = "127.0.0.1"
finally:
    #ipsock.shutdown(socket.SHUT_RD)
    ipsock.close()
    print("The default port # for the chatroom is %d" % port_no)
    print("Both IP address and port # should be known and reachable by clients.")
########################################################################

print("Initializing...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host_name,port_no)
    sock.bind(server_address)
    sock.listen(0)
except OSError as OSerr:
    print("Can not open the socket, addres might already been used.")
    print("The problem might be solved by tring different port #")
    print("Use '$netstat -t | grep '%d' ' to check" % port_no)
    sys.exit()

class CONNECTs(object):
    connects = []
    FTPs = []

class Chatroom(CONNECTs):
    def __init__(self,sock,rcv_buffer):
        self.addr = server_address
        self.config = ''
        self.rcv_buffer = rcv_buffer
        self.sock = sock
        self.th = threading.Thread(target = self.Thread_connect)
        self.th.start()
    def Thread_connect(self):
        self.clien_addr = ()
        print('waiting for a connection')
        try:
            self.connection, self.clien_addr = self.sock.accept()
            self.connects.append(self)
            try:
                print('connection from',self.clien_addr)
                self.configuration()
                #rtt test
                self.rtt_test()
                # colormapping
                if self.rtt != 'failed':
                    self.colorth = threading.Thread(target = self.colormapping)
                    self.colorth.start()
                while True:
                    self.data = self.connection.recv(self.rcv_buffer)
                    print('received: %s from' % self.data.decode(), self.clien_addr)
                    if self.data:
                        #1-1 secret talk
                        if self.data.decode()[0] == '#':
                            self.unicast_send(self.data)
                        #n-n chatroom
                        else:
                            for i in self.connects:
                                if i.th.isAlive():
                                    i.general_send('%s: %s'%(self.config, self.data.decode()))
                    else:
                        print('no more data from the client')
                        print('closing socket NO.',self.clien_addr)
                        self.close()
                        break
            except:
                print('FORCED to close the connection of ',self.clien_addr)
                self.close()
        except:
            print('connection lost')
    def close(self):
        if self.config != '':
            self.connection.close()
        else:
            print("null socket")
    def general_send(self,msg):
        print('sending msg: %s to %s, addr:' % (msg,self.config),self.clien_addr)
        try:
            if self.th.isAlive():
                self.connection.sendall(msg.encode('utf-8'))
            else:
                print(self.clien_addr,' not alive')
        except:
            print('failed to send the msg')
    def unicast_send(self,inmsg):
        inmsg = inmsg.decode()[1:]
        loc = inmsg.find(' ')
        found = False
        recv_name = inmsg
        msg = ''
        if loc > -1:
            recv_name = inmsg[:loc]
            msg = inmsg[loc+1 :]
        for name in connects:
            if name.config == recv_name and name.th.isAlive():
                print('sending secret msg to %s' % name.config)
                self.general_send('SECRET MSG SENT TO %s' % name.config)
                name.general_send('SECRET MSG FROM %s: %s' %(self.config, msg))
                found = True
        if not found:
            if len(inmsg) > 1:
                print('User not found')
                self.general_send('\nCan not find "%s"\nUser may logged out or does not exist.' % recv_name)
            self.colormapping(1)
    def configuration(self):
        try:
            self.config = self.connection.recv(self.rcv_buffer).decode()
            print('connection from user name %s' % self.config)
            if self.config:
                self.general_send('Hello %s' % self.config)
        except:
            print('configuration failure')
            self.close()
    def colormapping(self, once_flag = None):
        countp = ''
        count = ''
        while self.th.isAlive():
            count = ''
            for i in self.connects:
                if i.th.isAlive() and i.config != '':
                    count += i.config
            if count != countp:
                print(count)
                print(countp)
                countp = count
                alive = 0
                self.general_send('-------------------------------------------')
                for i in self.connects:
                    if i.config != '' and i.th.isAlive() and self.th.isAlive():
                        alive = alive + 1
                        color = alive % 7 + 1
                        mapping = 'CoLoR\x1b[0;3%s;40mrOloC~+_=|||%s|||=_+~\x1b[0mcccconfigcccC' % (color,i.config)
                        self.general_send(mapping)
                        time.sleep(self.rtt*18)
                self.general_send('-------------------------------------------')
            if once_flag is None:
                once_flag = 0
            elif once_flag == 1:
                break
            time.sleep(5)
    def rtt_test(self):
        try:
            msg = self.connection.recv(4)
            if msg.decode() == 'rtt':
                self.general_send('rtt')
                msg = self.connection.recv(self.rcv_buffer)
                msg = float(msg)
                self.rtt = msg
                print('%s rtt = %f sec' % (self.config,self.rtt))
            else:
                print('rtt test failed')
                self.close()
                self.rtt = 'failed'
        except:
            print('rtt test failed')
            self.close()
            self.rtt = 'failed'
# class FTP(CONNECTs):
#     """ muitithreadly send data by UDP"""
#     BUFFER = 4064
#     MAX_THREAD = 40
#     def __init__(self):
#         if self.file_preparation():
#             self.UDP_initialize()
#         else:
#             print('FTP startup failure')
#
#     def send_data(self):
#         pass
#     def file_preparation(self):
#         path = input('Please input the path of a file: ')
#         if os.path.isfile(path):
#             self.file = open(path,'rb')
#             self.file_name = path
#             self.size = self.file.seek(0,2)
#             self.file.seek(0,0)
#             self.loop = self.size / (self.BUFFER * self.MAX_THREAD)
#             return True
#         else:
#             print('Not a file')
#             return False
#
#     def NAME(self):
#         print('clien_addr\tclien_name')
#         for cli in self.connects:
#             if cli.th.isAlive() and cli.clien_addr != ():
#                 print('%s\t\t%s' %(cli.config, cli.clien_addr))
#         name = input('Please specify a client: ')
#         for cli in self.connects:
#             if cli.th.isAlive() and cli.clien_addr != () and name == cli.config:
#                 self.name = cli.config
#                 self.UDP_dest = (cli.clien_addr[0],cli.clien_addr[1]+10)
#                 self.chatroom = cli
#                 return True
#
#         print('client not found')
#         return False
#     def UDP_initialize(self):
#         if self.NAME():
#             self.chatroom.general_send('FiLe')
#             self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         else:
#             print('UDP startup failure')
#



connects = []
def auto_add_member_thread():
    KeepAlive = True
    while KeepAlive :
        if connects[-1].config != '':
            server_side_member = Chatroom(sock,rcv_buffer_size)
            connects.append(server_side_member)
            time.sleep(1)
        KeepAlive = False
        for member in connects:
            KeepAlive |= member.th.isAlive()
    print("member adding thread terminated")
FTPs = []
print('listening on %s port %s' % server_address)
server_msg='''
                        Please input control messages:
                        [mode]:show all threads status
                        [close]:close a speific connection
                        [close all]:close connection
                        [broadcast]:send msg to all client
                        [FTP]:upload a file #UNAVAILABLE
                        [FTP-send]:send file to a client #UNAVALIABLE
                        '''
try:
    print(server_msg)
    server_side_member = Chatroom(sock,rcv_buffer_size)
    connects.append(server_side_member)
    add_member_thread = threading.Thread(target = auto_add_member_thread)
    add_member_thread.deamon = True
    add_member_thread.start()
    while True:
        control_msg = input(': ')
        if control_msg == 'broadcast':
            msg = input('msg to broadcast: ')
            for i in connects:
                if i.th.isAlive():
                    print('sending to %s (%s)' % (i.config, i.clien_addr))
                    i.general_send('msg from server: %s' % msg)

        elif control_msg == 'close all':
            for i in connects:
                if i.clien_addr != ():
                    print('closing connection of #',i.clien_addr)
                    i.close()
            print('closing socket')
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            break
        elif control_msg == 'close':
            number_of_client = 0
            for i in connects:
                if i.clien_addr != () and i.th.isAlive():
                    number_of_client+=1
            if number_of_client > 0:
                print('please select a client# from clients status listed below to close:\nclient#\tname\trunning')
                num = 0
                allow = ''
                for i in connects:
                    num += 1
                    if i.clien_addr != () and i.th.isAlive():
                        print('%d\t%s\t%s' %(num, i.config, i.th.isAlive()))
                        allow = allow + ' %d ' % num
                    else:
                        print('X%dX\t%s\t%s\t|not allow to be closed ' %(num, i.config, i.th.isAlive()))
                try:
                    close_num = int(input(': '))
                    print('closing #%d client' % close_num)
                    close_num -= 1
                    if connects[close_num].th.isAlive():
                        connects[close_num].close()
                    else:
                        print('connection has already been closed')
                except:
                    print('unrecognized input or client#')
                    time.sleep(2)
                    print(server_msg)
            else:
                print('Has no connected client yet\nTo close the server, please input: close all')
                time.sleep(2)
                print(server_msg)
        elif control_msg == 'mode':
            print('clients status\nname\trunning')
            for i in connects:
                print('%s\t%s' %(i.config, i.th.isAlive()))
        elif control_msg == 'FTP':
            ftp = FTP()
            FTPs.append(ftp)
        else:
            print('UNRECOGNIZED CONTROL MESSAGE ')
            print(server_msg)
except:
    for i in connects:
        i.close()
    sock.close()
    print('Connection closed unexpectly')
    #raise #DEBUG
