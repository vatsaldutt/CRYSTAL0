from http.server import BaseHTTPRequestHandler, HTTPServer

Request = None


class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global Request
        messagetosend = bytes('Hello World', "utf")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        Request = self.requestline
        Request = Request[5: int(len(Request)-9)]
        print(Request)
        if Request == 'walk':
            print("walking")
        if Request == 'sit':
            print("sitting")
        if Request == 'back':
            print("Backing")

server_address_httpd = ('192.168.0.8', 8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print("Starting Server: ")
httpd.serve_forever()
quit()
