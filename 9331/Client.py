# encoding = utf-8
import sys
import socket
import threading
import time
import re


class client:
    client_socket = None
    client_p2p_socket = None
    username = ""
    is_login = False
    temp_id = ""
    contactlog_list = []
    contactlog_file = None
    contactlog_lock = None

    def __init__(self, server_address, p2p_port):
        try:
            self.client_socket = socket.socket()
            self.client_socket.connect(server_address)
        except:
            print("connection: error")
            exit()

        try:
            self.client_p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_p2p_socket.bind(("127.0.0.1", p2p_port))
        except:
            print("p2p connection: error")
            exit()

    def start(self):
        client_recv_thread = threading.Thread(target=self.recvfromClient)
        client_recv_thread.setDaemon(True)
        client_recv_thread.start()
        while True:
            while not self.is_login:
                self.login_send()

            massage = input()

            if massage == "Download_tempID":
                self.downloadID_send()
            elif massage == "Upload_contact_log":
                self.uploadlog_send()
            elif massage == "logout":
                self.logout_send()
            elif re.match(r"Beacon (\d+\.\d+\.\d+\.\d+) (\d+)", massage):
                match = re.match(r"Beacon (\d+\.\d+\.\d+\.\d+) (\d+)", massage)
                self.beacon_send((match.group(1), int(match.group(2))))
            else:
                print("Error. Invalid command.")

    # recvfromClient ?

    def recvfromClient(self):
        while True:
            massage, p2p_addr = self.client_p2p_socket.recvfrom(1024)
            massage = massage.decode()

            match_rst = re.match(r"beacon:(\d+) (\d+/\d+/\d+ \d+:\d+:\d+) (\d+/\d+/\d+ \d+:\d+:\d+) ([.\d]+)", massage)
            if match_rst:
                # attention
                format_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                print("Received beacon:" + match_rst.group(1) + ", " + match_rst.group(2) + ", " + match_rst.group(
                    3) + ';')
                print("Current time is: " + format_time)
                current_time = time.time()
                start_time = time.mktime(time.strptime(match_rst.group(2), "%d/%m/%Y %H:%M:%S"))
                expiry_time = time.mktime(time.strptime(match_rst.group(3), "%d/%m/%Y %H:%M:%S"))
                if start_time <= current_time and current_time <= expiry_time:
                    print("The beacon is valid")
                    self.contactlog_list.append({"tem_id": match_rst.group(1), "start_time": float(start_time),
                                                 "expiry_time": float(expiry_time), "str": massage[7:]})
                    self.contactlog_lock.acquire()
                    with open(self.username + "_contactlog.txt", "a") as file:
                        file.write(massage[7:] + '\n')

                    self.contactlog_lock.release()
                else:
                    print("The beacon is invalid.")

    # login_send

    def login_send(self):
        username = input("username:")
        password = input("password:")
        msg = "login:" + username + ":" + password
        # encoding = utf-8
        self.client_socket.send(msg.encode(encoding="utf8"))
        recv = self.client_socket.recv(1024).decode()

        if recv == "login:0":
            self.is_login = True
            self.username = username
            print("Welcome to the BlueTrace Simulator!")

            # ---------- remove time out log -----------
            self.contactlog_lock = threading.Lock()
            beacon_remove_thread = threading.Thread(target=self.beacon_remove)
            beacon_remove_thread.setDaemon(True)
            beacon_remove_thread.start()

        elif recv == "login:1":
            print("Invalid Password. Please try again.")
        elif recv == "login:2":
            print("Invalid Password. Your account has been blocked. Please try again later.")
        elif recv == "login:3":
            print("Username does not exist.")
        elif recv == "login:4":
            print("User already login.")

    # logout_send
    def logout_send(self):
        massage = "logout:" + self.username
        # encoding = utf-8
        self.client_socket.send(massage.encode())

        recv = self.client_socket.recv(1024).decode()

        if recv == "logout:0":
            print("logout successful.")
            self.is_login = False
            self.username = ''
            self.temp_id = ''

    # downloadID
    def downloadID_send(self):
        massage = "tempID:" + self.username
        self.client_socket.send(massage.encode())

        recv = self.client_socket.recv(1024)
        recv.decode()

        match = re.match(r"tempID:(\w+):([.\d]+):([.\d]+)", recv)
        if match:
            self.temp_id = match.group(1)
        print("TempID:\n" + self.temp_id)

    # uploadlog_send

    def uploadlog_send(self):
        context = ""
        for beacon in self.contactlog_list:

            context += beacon["str"]
            context += "!"
        # contactlog_lock = None
        self.contactlog_lock.acquire()
        with open(self.username + "_contactlog.txt", "w") as file:
            for beacon in self.contactlog_list:
                file.write(beacon["str"] + "\n")

        self.contactlog_lock.release()
        context = context[:-1]
        massage = "uploadlog:" + self.username + ":" + context
        self.client_socket.send(massage.encode())

    # ------------- beacon ---------------#


    def beacon_send(self, p2p_address):
        current_time = time.time()
        # start_time = current_time
        start_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(current_time))
        # expiry_time = current_time + 60 * 0.5
        expiry_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(current_time + 60 * 0.5))

        massage = self.temp_id + " " + start_time + " " + expiry_time + " " + str(1.0)
        print(self.temp_id + ", " + start_time + ", " + expiry_time + ";")
        self.client_p2p_socket.sendto(("beacon:" + massage).encode(), p2p_address)
        pass

    def beacon_remove(self):
        def beacon_filter(beacon):
            if beacon["start_time"] <= time.time() and time.time() <= beacon["expiry_time"]:
                return True
            return False

        while True:
            length = len(self.contactlog_list)
            temp_list = filter(beacon_filter, self.contactlog_list)
            self.contactlog_list = list(temp_list)
            if length > len(self.contactlog_list):
                self.contactlog_lock.acquire()
                with open(self.username + "_contactlog.txt", "w") as file:
                    for beacon in self.contactlog_list:
                        file.write(beacon["str"] + "\n")
                        # print("hihi")
                self.contactlog_lock.release()


if __name__ == "__main__":
    print(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    p2p_port = int(sys.argv[3])
    client_i = client((server_ip, server_port), p2p_port)
    client_i.start()
