import os, sys, http.server, socketserver

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

handler = http.server.SimpleHTTPRequestHandler
with ReuseTCPServer(('', 8080), handler) as httpd:
    print('Serving on http://localhost:8080', flush=True)
    httpd.serve_forever()
