import BaseHTTPServer
import SimpleHTTPServer
import json
import GPIO_on, GPIO_off, GPIO_read

FILE = 'index.html'
PORT = 80

def pin_translate(x):
	return {
		'1': '3',
		'2': '5',
		'3': '7',
		'4': '8'}.get(x,3)

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        length = self.headers.getheader('content-length')
        data = self.rfile.read(int(length))
		
	pin = pin_translate(data[1])
	
        if data[0] == '1':
            GPIO_on.run_script(pin)
        else:
            GPIO_off.run_script(pin)

	self.wfile.write("%s" %(GPIO_read.run_script()))

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    print "The server has been started on http://localhost:%s" %PORT
    start_server()
