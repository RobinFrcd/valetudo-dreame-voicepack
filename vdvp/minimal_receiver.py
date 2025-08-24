import http.server
import socketserver

PORT = 8000
FILENAME = "robot_sounds.tar.gz"


class SimpleUploadServer(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        print(f"Receiving file from {self.client_address[0]}...")
        content_length = int(self.headers["Content-Length"])
        with open(FILENAME, "wb") as f:
            f.write(self.rfile.read(content_length))

        self.send_response(201, "Created")
        self.end_headers()
        self.wfile.write(b"File successfully uploaded.\n")
        print(f"Successfully saved file as '{FILENAME}'")


with socketserver.TCPServer(("0.0.0.0", PORT), SimpleUploadServer) as httpd:
    print(f"Server started on port {PORT}. Ready to receive '{FILENAME}'.")
    httpd.serve_forever()
