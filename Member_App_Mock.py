from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from socketserver import ThreadingMixIn
import random

class MyRequestHandler(BaseHTTPRequestHandler):

    MembersDict = {}

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self) #calls the original end_headers

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(bytes("Invalid endpoint", "utf-8"))

    def handleAddMember(self):
        global MembersDict
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        try:
            name = body['request']['name']
            email = body['request']['email']
            phone = body['request']['phone']
            memberID = random.choice([i for i in range(0,9999) if i not in MembersDict.keys()])
            MembersDict[memberID] = {"memberID": memberID, "name": name, "email": email, "phone": phone}
            response = {"response": {"memberID":memberID}}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
        except:
            self.send_response(500)
            self.end_headers()

    def handleInquireMember(self):
        global MembersDict
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        try:
            memberID = body['request']['memberID']
            member = MembersDict[memberID]
            response = {"response": member}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
        except:
            self.send_response(500)
            self.end_headers()

    def handleUpdateMember(self):
        global MembersDict
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        try:
            memberID = body['request']['memberID']
            name = body['request']['name']
            email = body['request']['email']
            phone = body['request']['phone']
            MembersDict[memberID] = {"memberID": memberID, "name": name, "email": email, "phone": phone}
            response = {"response": {"memberID":memberID}}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
        except:
            self.send_response(500)
            self.end_headers()
    
    def handleRemoveMember(self):
        global MembersDict
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        try:
            memberID = body['request']['memberID']
            MembersDict.pop(memberID)
            response = {"response": {"status":"success"}}
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
            self.send_response(200)
            self.end_headers()
        except:
            response = {"response": {"status":"failure"}}
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        xSplit = self.path.split('/')
        if xSplit[1] == "addMember":
            self.handleAddMember()
        elif xSplit[1] == "inquireMember":
            self.handleInquireMember()
        else:
            self.handleNotFound()
    
    def do_PUT(self):
        xSplit = self.path.split('/')
        if xSplit[1] == "updateMember":
            self.handleUpdateMember()
        else:
            self.handleNotFound()
    
    def do_DELETE(self):
        xSplit = self.path.split('/')
        if xSplit[1] == "removeMember":
            self.handleRemoveMember()
        else:
            self.handleNotFound()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    #The main function <(*.*<) (^*.*^) (>*.*)>
    print("Beep Boop: Server Initialized - Please build additional Pylons")
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)
    server.serve_forever()  
    
main()