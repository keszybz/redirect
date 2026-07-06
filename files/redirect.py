# pylint: disable=missing-module-docstring,missing-class-docstring,invalid-name

import http.server
import socket
import socketserver
import ssl
import subprocess
import sys
import threading
import time

from systemd import daemon

PAGE = (
    """\
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Gotcha</title>
    <style>
     html { font-size: 15vw; text-align: center }
    </style>
  </head>
  <body>
      👮<br>GOTCHA!
  </body>
</html>
"""
).encode()


class RedirectHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))

        self.end_headers()

        self.wfile.write(PAGE)

        cmd = ["systemctl", "start", "ai-guard-alarm.service"]
        res = subprocess.run(cmd)
        print(f"executed {res}")


class SocketActivatedServer(http.server.HTTPServer):
    # pylint: disable=non-parent-init-called,super-init-not-called
    def __init__(self, RequestHandlerClass, bind_and_activate=True):
        assert bind_and_activate

        (fd,) = daemon.listen_fds()
        print(f"got {fd=}")
        sock = socket.fromfd(fd, self.address_family, self.socket_type)

        server_address = sock.getsockname()[:2]
        print(f"{server_address=}")

        socketserver.BaseServer.__init__(self, server_address, RequestHandlerClass)

        self.socket = sock


def server_watchdog(server, secs):
    time.sleep(secs)
    print("Shutting down server")
    server.shutdown()


if __name__ == "__main__":
    with SocketActivatedServer(RedirectHandler) as server:
        if len(sys.argv) > 1 and sys.argv[1] == "--ssl":
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(
                certfile="certs/redirect-cert.pem", keyfile="certs/redirect-key.pem"
            )
            server.socket = ctx.wrap_socket(server.socket, server_side=True)

        threading.Thread(target=server_watchdog, args=(server, 60), daemon=True).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

        server.server_close()
