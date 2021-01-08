import socket
import time
import json
import os
import requests
import win32api
import win32print
import shutil

class PrinterAgetn():
    def __init__(self, server='104.238.190.76', port=4567):
        self.client = None
        self.server = server
        self.port = port
        pass

    def connect(self):
        print_message = ''
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.server, self.port))
        self.client.send(json.dumps({
            "cmd": "connect",
            "data": {
                "name": "Printer",
                "site": "LaserOffice"
            }}).encode())
        while True:
            # wait for print
            print_message = self.client.recv(1024).decode()
            message_list = print_message.split('\n')
            for message in message_list[:-1]:
                m = json.loads(message)
                print(m)

                # deal with ping
                if m["cmd"] != "print":
                    continue

                # get file
                r = requests.get(m["data"]["url"]) 
                with open(m["data"]["name"],'wb') as f:
                    f.write(r.content)

                # print
                time.sleep(1)
                print (win32print.GetDefaultPrinter())
                print (os.getcwd() +  '/' + m["data"]["name"])
                win32api.ShellExecute(
                    0,
                    "print",
                    os.getcwd() +  '/' + m["data"]["name"],
                    '/d:"%s"' %win32print.GetDefaultPrinter(),
                    ".",
                    0
                )

                # del file.  由于打印是异步的，不能删除，否则找不到文件
                # os.remove(os.getcwd() +  '/' + m["data"]["name"])

                # notify
                self.client.send(json.dumps({
                    "cmd": "notify",
                    "data": {
                        "result": 1,
                        "url": m["data"]["url"]
                    }
                }).encode())
        self.client.close()

if __name__ == '__main__':
    p = PrinterAgetn()
    p.connect()
