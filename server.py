from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from checker import is_all_up

server = None

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if is_all_up():
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'FAIL')

def start_server(port):
    global server
    server = ThreadingHTTPServer(('0.0.0.0', port), Server)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    stop_server()

def stop_server():
    global server
    server.server_close()
