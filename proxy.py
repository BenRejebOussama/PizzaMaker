import socket
import http.server
import socketserver

BIND_ADDR = "1.2.3.4"  # l'adresse source voulue

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_CONNECT(self):
        # Crée un tunnel HTTPS
        host, port = self.path.split(":")
        port = int(port)

        # Crée une socket bindée
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((BIND_ADDR, 0))  # bind source IP
        s.connect((host, port))

        self.send_response(200, "Connection Established")
        self.end_headers()

        # Transfert bidirectionnel (client <-> serveur)
        self._forward(self.connection, s)

    def _forward(self, client, server):
        import threading

        def forward(src, dst):
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        threading.Thread(target=forward, args=(client, server)).start()
        threading.Thread(target=forward, args=(server, client)).start()

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("127.0.0.1", 8080), Proxy) as httpd:
        print("Proxy actif sur 127.0.0.1:8080")
        httpd.serve_forever()