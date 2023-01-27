#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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

        header_arguments = self.data.decode("utf-8").split(" ")
        method_argument = header_arguments[0]
        site_argument = header_arguments[1]

        mime_type_html = "text/html"
        mime_type_css = "text/css"

        if method_argument == "GET":

            path_no_header = site_argument
            path = "www" + path_no_header
            
            if os.path.isdir(path):
                if not path.endswith("/"):
                    message = "HTTP/1.1 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080"+path_no_header+"/\r\n"
                    message = message.encode("utf-8")
                    self.request.sendall(message)
                    return

            try:

                if path.endswith(".html"):
                    mime_type = mime_type_html
                elif path.endswith(".css"):
                    mime_type = mime_type_css
                else:
                    path = path + "index.html"
                    mime_type = mime_type_html

                with open(path, "rb") as file_to_open:
                    response = file_to_open.read()

                message = "HTTP/1.1 200 OK\nContent-Type: "+mime_type+"\n\n"
                message = message.encode("utf-8")
                self.request.sendall(message+response)

            except:
                message = "HTTP/1.1 404 Not Found\r\n"
                message = message.encode("utf-8")
                self.request.sendall(message)

        else:
            message = "HTTP/1.1 405 Method Not Allowed\r\n"
            message = message.encode("utf-8")
            self.request.sendall(message)
            return
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
