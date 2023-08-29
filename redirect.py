import http.server
import socketserver
import ssl

PORT = 8080
CGI = 'play.cgi'
SSL = False

class Redirect(http.server.CGIHTTPRequestHandler):
    cgi_directories = ['/']
    def do_GET(self):
        if self.path == f'/{CGI}' and self.is_cgi():
            super().do_GET()
        else:
            self.send_response(301)
            new_path = f'http://localhost:{PORT}/{CGI}'
            self.send_header('Location', new_path)
            self.end_headers()


with http.server.HTTPServer(("localhost", PORT), Redirect) as httpd:
    if SSL:
        httpd.have_fork = False
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile="ssl/openai.com+4.pem",
                            keyfile="ssl/openai.com+4-key.pem")
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    httpd.serve_forever()
