import BaseHTTPServer
import SimpleHTTPServer
import json
import GPIO_on, GPIO_off

FILE = 'index.html'
PORT = 80


class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        length = self.headers.getheader('content-length')
        print length
        print self.headers.getheader('Content-type')
        data = self.rfile.read(int(length))

        if data[0] == 1:
            GPIO_on.run_script(data[1])
        else:
            GPIO_off.run_script(data[1])
        

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    print "The server has been started on http://localhost:%s" %PORT
    start_server()
