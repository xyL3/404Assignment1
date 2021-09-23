#  coding: utf-8 
import socketserver, os, requests


# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Xueying Luo
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # parse the get request 

        # [0]=method(GET, etc) [1]=path, [6]=host (or [4]=host for browser/curl)
        parsed_request = self.data.decode().split()  

        host = "127.0.0.1:8080"
        root = "./www"

        # status code & headers 
        status_200 = "HTTP/1.0 200 OK\r\n"
        status_301 = "HTTP/1.0 301 Moved Permanently\r\n"
        status_404 = "HTTP/1.0 404 Not Found\r\n"
        status_405 = "HTTP/1.0 405 Method Not Allowed\r\n"
        content_type_html = "Content-Type: text/html\r\n"
        content_type_css = "Content-Type: text/css\r\n"
        header_end = "\r\n"

        if parsed_request[0] != 'GET':
            # cannot handle methods other than GET - 405 Method Not Allowed
            self.request.sendall(bytearray(status_405+header_end,'utf-8'))
        
        else: 

            path = parsed_request[1]
            if os.path.exists(root+path): # check whether path exists

                if host == parsed_request[4] or host == parsed_request[6]:
                    # correct host

                    path_split = path.split('.')

                    if path[-1] == '/':
                        # display index.html

                        self.request.sendall(bytearray(status_200+content_type_html+header_end,'utf-8'))

                        file = open(root+path+"/index.html", "r")
                        self.request.sendall(bytearray(file.read(), 'utf-8'))
                        file.close()

                    elif path_split[-1] == "html" :
                        # display index.html

                        self.request.sendall(bytearray(status_200+content_type_html+header_end,'utf-8'))

                        file = open(root+path, "r")
                        self.request.sendall(bytearray(file.read(), 'utf-8'))
                        file.close()

                    elif path_split[-1] == "css":
                        # display css
                        self.request.sendall(bytearray(status_200+content_type_css+header_end,'utf-8'))

                        file = open(root+path, "r")
                        self.request.sendall(bytearray(file.read(), 'utf-8'))
                        file.close()

                    elif path[-1] != '/' and not os.path.isfile(root+path):
                        
                        addr = root+ path + '/'

                        if os.path.exists(addr):
                            # incorret path - 301 Moved Permanently
                            self.request.sendall(bytearray(status_301+"Location: "+host+path+'/'+header_end+header_end,'utf-8'))

                        else:
                            # 404 not found
                            self.request.sendall(bytearray(status_404+header_end,'utf-8'))

                    else:
                        # wrong path - 404 Not Found
                        self.request.sendall(bytearray(status_404+header_end,'utf-8'))


            else:
                # wrong path - 404 Not Found
                self.request.sendall(bytearray(status_404+header_end,'utf-8'))


        




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


    



