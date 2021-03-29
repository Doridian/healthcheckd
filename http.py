from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

server = None

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

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
