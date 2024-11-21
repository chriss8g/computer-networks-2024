import requests
from client_interface import HttpClient, HttpResponse

class RequestsHttpClient(HttpClient):
    def send_request(self, method, url, headers=None, data=None):
        try:
            response = requests.request(method, url, headers=headers, data=data)
            return HttpResponse(response.status_code, response.text, dict(response.headers))
        except Exception as e:
            return HttpResponse(0, f"Error: {e}", {})


import socket

class CustomHttpClient(HttpClient):
    def send_request(self, method, url, headers=None, data=None):
        try:
            # Helper functions
            def parse_url(url):
                if not url.startswith("http://"):
                    raise ValueError("Only 'http' scheme is supported")
                url = url[len("http://"):]
                parts = url.split("/", 1)
                host_port = parts[0]
                resource = "/" + parts[1] if len(parts) > 1 else "/"
                host, port = (host_port.split(":") if ":" in host_port else (host_port, 80))
                return host, int(port), resource

            def receive_response(sock):
                response = b""
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                return response.decode()

            def parse_response(response):
                lines = response.split("\r\n")
                status_line = lines[0]
                headers = {}
                body = ""
                reading_headers = True
                for line in lines[1:]:
                    if line == "":
                        reading_headers = False
                        continue
                    if reading_headers:
                        key, value = line.split(": ", 1)
                        headers[key] = value
                    else:
                        body += line + "\n"
                status_code = int(status_line.split(" ")[1])
                return HttpResponse(status_code, body.strip(), headers)

            # Parse URL
            host, port, resource = parse_url(url)

            # Create and connect socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            # Build request
            http_request = f"{method} {resource} HTTP/1.1\r\nHost: {host}\r\n"
            if headers:
                for header, value in headers.items():
                    http_request += f"{header}: {value}\r\n"
            if data:
                http_request += f"Content-Length: {len(data)}\r\n\r\n{data}"
            else:
                http_request += "\r\n"

            # Send request and receive response
            client_socket.sendall(http_request.encode())
            response = receive_response(client_socket)
            client_socket.close()

            # Parse response
            return parse_response(response)

        except Exception as e:
            return HttpResponse(0, f"Error: {e}", {})
