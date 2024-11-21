import socket
from threading import Thread

AUTHORIZED_TOKEN = "12345"

def handle_client(client_socket):
    try:
        request_data = client_socket.recv(2048).decode(errors="ignore")
        if not request_data.strip():
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nEmpty request received. Please send a valid HTTP request."
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        # Extraer la línea de solicitud HTTP
        request_line = request_data.split('\r\n')[0]
        method, path, protocol = request_line.split()

        print(f"Request: {method} {path} {protocol}")

        headers = {}
        for line in request_data.split('\r\n')[1:]:
            if not line.strip():
                break
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        # Casos sin autorización
        if path == "/" and method == "GET":
            response_body = "Welcome to the server! No authorization required here."
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/plain",
                f"Content-Length: {len(response_body)}"
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        # Validar autorización solo para rutas protegidas
        if path.startswith("/secure"):
            if "Authorization" in headers:
                auth_token = headers["Authorization"].replace("Bearer ", "").strip()
                if auth_token != AUTHORIZED_TOKEN:
                    response = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/plain\r\n\r\nInvalid or missing authorization token."
                    client_socket.sendall(response.encode())
                    client_socket.close()
                    return
            else:
                response = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/plain\r\n\r\nAuthorization header missing."
                client_socket.sendall(response.encode())
                client_socket.close()
                return

        # Métodos HTTP
        if method == "GET":
            if path == "/secure":
                response_body = "GET request successful! You accessed a protected resource."
            else:
                response_body = f"GET request successful! Path: {path}."
        elif method == "POST":
            try:
                # Validar longitud del cuerpo
                content_length = int(headers.get("Content-Length", 0))
                body = request_data.split("\r\n\r\n")[1][:content_length]

                # Validar contenido según Content-Type
                content_type = headers.get("Content-Type", "text/plain")
                if content_type == "application/json":
                    try:
                        import json
                        json.loads(body)  # Intentar parsear como JSON
                        response_body = f"POST request successful! JSON body received: {body}."
                    except json.JSONDecodeError:
                        raise ValueError("Malformed JSON body")
                elif content_type == "application/xml":
                    try:
                        import xml.etree.ElementTree as ET
                        ET.fromstring(body)  # Intentar parsear como XML
                        response_body = f"POST request successful! XML body received: {body}."
                    except ET.ParseError:
                        raise ValueError("Malformed XML body")
                else:
                    # Manejar cuerpos de texto o desconocidos
                    response_body = f"POST request successful! Plain text body received: {body}."
            except (IndexError, ValueError) as e:
                response_headers = [
                    "HTTP/1.1 400 Bad Request",
                    "Content-Type: text/plain",
                    f"Content-Length: {len(str(e))}"
                ]
                response = "\r\n".join(response_headers) + "\r\n\r\n" + str(e)
                client_socket.sendall(response.encode())
                client_socket.close()
                return

        elif method == "HEAD":
            response_body = ""
        elif method == "PUT":
            response_body = f"PUT request successful! Resource '{path}' would be updated if this were implemented."
        elif method == "DELETE":
            response_body = f"DELETE request successful! Resource '{path}' would be deleted if this were implemented."
        elif method == "OPTIONS":
            response_headers = [
                "HTTP/1.1 204 No Content",
                "Allow: GET, POST, HEAD, PUT, DELETE, OPTIONS, TRACE, CONNECT",
                "Content-Length: 0"
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n"
            client_socket.sendall(response.encode())
            client_socket.close()
            return
        elif method == "TRACE":
            response_body = request_data
        elif method == "CONNECT":
            # Implementación básica de CONNECT
            target = path.strip("/")  # Supongamos que el target está en el path
            response_body = f"CONNECT method successful! Tunneling to {target} established."
        else:
            response = f"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nMethod '{method}' not allowed."
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        # Construir respuesta HTTP
        response_headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/plain",
            f"Content-Length: {len(response_body)}"
        ]
        response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nServer error: {e}"

    client_socket.sendall(response.encode())
    client_socket.close()

def run_server(host='', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    run_server()
