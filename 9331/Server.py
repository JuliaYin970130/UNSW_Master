# encoding = utf-8
import threading
import random
import time
import re
import socket
import sys

class TempID:
    temp_id = ""
    start_time = None
    expiry_time = None

    def __init__(self,temp_id,start,expiry):
        self.temp_id = temp_id
        self.start_time = start
        self.expiry_time = expiry

class user:
    username = None
    password = None
    client = None
    state = "logout"
    login_failure_times = 1
    block_time = 0
    temp_id = []

    def __init__(self,username, password):
        self.username = username
        self.password = password

    def block_timer(self):
        self.state = "logout"
        self.login_failure_times = 1
        #print("block.")

    def login(self,password,client,block_duration):
        if self.state == "block":
            return 2
        elif self.state == "login":
            return 4
        if self.password == password:
            self.state = "login"
            self.login_failure_times = 1
            self.client = client
            return 0
        else:
            if self.login_failure_times >= 3:
                self.state = "block"
                threading.Timer(block_duration,self.block_timer).start()
                return 2
            else:
                self.login_failure_times += 1
                return 1

    def logout(self):
        if self.state != "login":
            return 1
        else:
            self.state = "logout"
            self.client = None
            self.login_failure_times = 1
            self.temp_id = []
            return 0

    def set_temp_id(self,temp_id):
        self.temp_id.append(temp_id)

class server:
    user_info_fileName = "credentials.txt"
    user_temp_id_fileName = "tempIDs.txt"
    user_list = {}
    locals_address = "127.0.0.1"
    locals_port = 11024
    socket_server = None
    client_pool = []
    block_duration = 15
    max_temp_id = 10000000000000000000
    temp_id_list = {}

    def __init__(self,server_port,block_duration):
        self.block_duration = block_duration
        self.locals_port = server_port
        # 读取文件内容，并转换为字典{username:password}
        fp = open(self.user_info_fileName,'r')
        for line in fp.readlines():
            #print(line)
            match_rst = re.match(r"(\+\w+) (\w+)", line)
            self.user_list[match_rst.group(1)] = user(match_rst.group(1), match_rst.group(2))

        fp.close()
        #初始化tempID内容
        fp = open(self.user_temp_id_fileName,'r')
        for line in fp.readlines():
            #print(line)
            match_rst = re.match(r"(\+\w+) (\d+) (\d+/\d+/\d+ \d+:\d+:\d+) (\d+/\d+/\d+ \d+:\d+:\d+)",line)
            self.user_list[match_rst.group(1)].temp_id.append(TempID(match_rst.group(2),match_rst.group(3),match_rst.group(4)))
            start_time = time.mktime(time.strptime(match_rst.group(3),"%d/%m/%Y %H:%M:%S"))
            expiry_time = time.mktime(time.strptime(match_rst.group(4),"%d/%m/%Y %H:%M:%S"))
            self.temp_id_list[match_rst.group(2)] = {"username": match_rst.group(1),"start_time":start_time,"expiry_time":expiry_time}
        fp.close()
        #初始化服务器连接
        self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_server.bind((self.locals_address,self.locals_port))

    def login_recv(self,client,username,password):
        massage = "login:"
        if username in self.user_list:
            result = self.user_list[username].login(password,client,self.block_duration)
            massage += str(result)
        else:
            massage += "3"
        print(massage)
        #self.sendtoClient(massage,client)
        client.sendall(massage.encode(encoding="utf8"))

    def logout_recv(self,client,username):
        massage = "logout:"
        if username in self.user_list:
            result = self.user_list[username].logout()
            massage += str(result)
            print(massage)
        else:
            massage += "3"
        #self.sendtoClient(massage,client)
        #print(massage)
        client.sendall(massage.encode())
        if result == 0:
            print(username+"logout")

    def getFromatTime(self,ctime):
        return time.strftime("%d/%m/%Y %H:%M:%S",ctime)

    def get_temp_id(self):
        temp_id = self.max_temp_id
        while True:
            temp_id = self.max_temp_id + random.randint(0,99)
            self.max_temp_id = temp_id
            yield temp_id

    def tempID_recv(self,client,username):
        temp_id = next(self.get_temp_id())
        self.user_list[username].set_temp_id(temp_id)
        start_time = time.time()
        expiry_time = start_time + 15*60
        massage = "tempID:" + str(temp_id) + ":" + str(start_time) + ":" + str(expiry_time)
        #self.sendtoClient(massage,client)
        client.sendall(massage.encode())
    
        self.temp_id_list[str(temp_id)] = {"username":username,"start_time":start_time,"expiry_time":expiry_time}
        with open(self.user_temp_id_fileName,"a") as fp:

            fp.write(username + " " + str(temp_id) + " " + self.getFromatTime(time.localtime())+ " " + self.getFromatTime(time))
        print("user:" + username + "\nTempID\n" + str(temp_id))

    def contactlog_recv(self,client,username, log_str):
        log_list = log_str.split("!")
        print("received contact log form" + username)
        for log in log_list:
            match_rst = re.match(r"(\d+) (\d+/\d+/\d+ \d+:\d+:\d+) (\d+/\d+/\d+ \d+:\d+:\d+)",log)
            if match_rst:
                log = match_rst.group(1) + ", " + match_rst.group(2) + ", " + match_rst.group(3) + ";"
                print(log)
            print("\nContact log checking")
            # print(log_list)

        for log in log_list:
            match_rst = re.match(r"(\d+) (\d+/\d+/\d+ \d+:\d+:\d+) (\d+/\d+/\d+ \d+:\d+:\d+)",log)
            if match_rst:
                username = self.temp_id_list[match_rst.group(1)]["username"]
                log = log.replace(match_rst.group(1),username,1)
                log = username + ", " + match_rst.group(2) + ", " + match_rst.group(1) + ";"
                print(log)

    def recvfromClient(self,client):
        while True:
            try:
                recv = client.recv(1024)
            except ConnectionError:
                print("Connection error.")
                client.close()
                self.client_pool.remove(client)
                for username in self.user_list:
                    user = self.user_list[username]
                    if user.client == client and user.state == "login":
                        user.state = "logout"
                break
            recv = recv.decode(encoding="utf8")
            print("  recv"+recv)
            if re.match(r"login:(\+\w+):(\w+)", recv):
                match = re.match(r"login:(\+\w+):(\w+)",recv)
                self.login_recv(client,match.group(1),match.group(2))
            elif re.match(r"logout:(\+\w+)", recv):
                match = re.match(r"logout:(\+\w+)", recv)
                self.logout_recv(client,match.group(1))
            elif re.match(r"tempID:(\+\w+)",recv):
                match = re.match(r"tempID:(\+\w+)",recv)
                self.tempID_recv(client,match.group(1))
            elif re.match(r"uploading:(\+\w+):(.+)",recv):
                #print(recv)
                match = re.match(r"uploading:(\+\w+):(.+)",recv)
                self.contactlog_recv(client,match.group(1),match.group(2))

    def start(self):
        self.socket_server.listen(10)
        while True:
            client,_ = self.socket_server.accept()
            thread = threading.Thread(target=self.recvfromClient,args=(client,))
            thread.setDaemon(True)
            thread.start()
            self.client_pool.append(client)


if __name__ == "__main__":
    server_port = int(sys.argv[1])
    block_duration = int(sys.argv[2])
    server_i = server(server_port, block_duration)
    server_i.start()




