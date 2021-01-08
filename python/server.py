import socketserver
import sys
import os
import shutil
import json
import time

class PrintHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Connected from: ", self.client_address)

        self.file_list = []
        self.print_list = []
        os.system('rm -rf /var/www/wx/files/*')
        
        recvData = self.request.recv(1024)
        print (json.loads(recvData.decode()))

        while True:
            self.file_list = os.listdir('/var/www/wx/files/')
            if len(self.file_list) == 0:
                self.request.sendall((json.dumps({
                    "cmd": "ping"
                }) + '\n').encode())
                time.sleep(1)
                continue
        
            # 依次打印
            for f in self.file_list:
                # send to printer
                if self.check_file():
                    self.request.sendall((json.dumps({
                        "cmd": "print",
                        "data": {
                            "url": "http://wx.ashliu.com/files/" + f,
                            "name": f
                        }
                    }) + '\n').encode())

                # wait printer
                recvData = self.request.recv(1024)
                if not recvData:
                    break
                recvData = json.loads(recvData.decode())
                print (recvData)
                
                # del file
                os.system('rm -rf /var/www/wx/files/' + f)

        self.request.close()
        print("Disconnected from: ", self.client_address)
    
    def check_file(self):
        return True
 
srv = socketserver.ThreadingTCPServer(("", 4567), PrintHandler)
srv.serve_forever()
