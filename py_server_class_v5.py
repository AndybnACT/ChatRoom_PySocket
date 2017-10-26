import socket
import sys
import threading
import time
import os
assert sys.version_info >= (3,5)
port_no = 20039
rcv_buffer_size = 100
host_name = 'localhost'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host_name,port_no)
sock.bind(server_address)
sock.listen(0)
class CONNECTs(object):
    connects = []
    FTPs = []

class Chatroom(CONNECTs):
    def __init__(self,sock,rcv_buffer):
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
                            self.secret_talk(self.data)
                        #n-n chatroom
                        else:
                            for i in self.connects:
                                if i.th.isAlive():
                                    i.boardcasting('%s: %s'%(self.config, self.data.decode()))
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
        self.connection.close()
    def boardcasting(self,msg):
        print('sending boardcast msg: %s to' % (msg),self.clien_addr)
        try:
            if self.th.isAlive():
                self.connection.sendall(msg.encode('utf-8'))
            else:
                print(self.clien_addr,' not alive')
        except:
            print('failed to send the msg')
    def secret_talk(self,inmsg):
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
                self.boardcasting('SECRET MSG SENT TO %s' % name.config)
                name.boardcasting('SECRET MSG FROM %s: %s' %(self.config, msg))
                found = True
        if not found:
            if len(inmsg) > 1:
                print('User not found')
                self.boardcasting('\nCan not find "%s"\nUser may logged out or does not exist.' % recv_name)
            self.colormapping(1)
    def configuration(self):
        try:
            self.config = self.connection.recv(self.rcv_buffer).decode()
            print('connection from user name %s' % self.config)
            if self.config:
                self.boardcasting('Hello %s' % self.config)
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
                self.boardcasting('-------------------------------------------')
                for i in self.connects:
                    if i.config != '' and i.th.isAlive() and self.th.isAlive():
                        alive = alive + 1
                        color = alive % 7 + 1
                        mapping = 'CoLoR\x1b[0;3%s;40mrOloC~+_=|||%s|||=_+~\x1b[0mcccconfigcccC' % (color,i.config)
                        self.boardcasting(mapping)
                        time.sleep(self.rtt*18)
                self.boardcasting('-------------------------------------------')
            if once_flag is None:
                once_flag = 0
            elif once_flag == 1:
                break
            time.sleep(5)
    def rtt_test(self):
        try:
            msg = self.connection.recv(4)
            if msg.decode() == 'rtt':
                self.boardcasting('rtt')
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
class FTP(CONNECTs):
    """ muitithreadly send data by UDP"""
    BUFFER = 4064
    MAX_THREAD = 40
    def __init__(self):
        if self.file_preparation():
            self.UDP_initialize()
        else:
            print('FTP startup failure')

    def send_data(self):
        pass
    def file_preparation(self):
        path = input('Please input the path of a file: ')
        if os.path.isfile(path):
            self.file = open(path,'rb')
            self.file_name = path
            self.size = self.file.seek(0,2)
            self.file.seek(0,0)
            self.loop = self.size / (self.BUFFER * self.MAX_THREAD)
            return True
        else:
            print('Not a file')
            return False

    def NAME(self):
        print('clien_addr\tclien_name')
        for cli in self.connects:
            if cli.th.isAlive() and cli.clien_addr != ():
                print('%s\t\t%s' %(cli.config, cli.clien_addr))
        name = input('Please specify a client: ')
        for cli in self.connects:
            if cli.th.isAlive() and cli.clien_addr != () and name == cli.config:
                self.name = cli.config
                self.UDP_dest = (cli.clien_addr[0],cli.clien_addr[1]+10)
                self.chatroom = cli
                return True
            pass
        print('client not found')
        return False
    def UDP_initialize(self):
        if self.NAME():
            self.chatroom.boardcasting('FiLe')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print('UDP startup failure')




connects = []
FTPs = []
print('starting up on %s port %s' % server_address)
server_msg='''
                        Please input control messages:
                        [add]:add new client
                        [mode]:show all threads status
                        [close]:close a speific connection
                        [close all]:close connection
                        [boardcast]:send msg to all client
                        [FTP]:upload a file
                        [FTP-send]:send file to a client
                        '''
# try:
print(server_msg)
while True:
    control_msg = input(': ')
    if control_msg == 'add':
        lan = Chatroom(sock,rcv_buffer_size)
        connects.append(lan)
        pass
    elif control_msg == 'boardcast':
        msg = input('msg to boardcast: ')
        for i in connects:
            if i.th.isAlive():
                print('sending to %s (%s)' % (i.config, i.clien_addr))
                i.boardcasting('msg from server: %s' % msg)
            pass
    elif control_msg == 'close all':
        for i in connects:
            if i.clien_addr != ():
                print('closing connection of #',i.clien_addr)
                i.close()
        print('closing socket')
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
# except:
#     for i in connects:
#         i.close()
#     sock.close()
#     print('Connection closed unexpectly')
