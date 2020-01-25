from http.server import BaseHTTPRequestHandler, HTTPServer
from ServerClass import MyHTTPRequestHandler

address = ('localhost', 8080)

with HTTPServer(address, MyHTTPRequestHandler) as server:
    server.serve_forever()