from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class request_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            f = open(curdir + sep + '/test.html')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        return

def main():
    try:
        server = HTTPServer(('', 80), request_handler)
        print 'Started HTTPServer...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close

if __name__ == '__main__':
    main()
