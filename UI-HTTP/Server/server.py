import socket
from threading import Thread

# Token de autorización esperado (puedes cambiarlo)
AUTHORIZED_TOKEN = "12345"

# Función para manejar cada cliente
def handle_client(client_socket):
    try:
        request_data = client_socket.recv(2048).decode(errors="ignore")  # Leer datos y manejar caracteres no válidos

        # Solicitud vacía
        if not request_data.strip():
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nEmpty request received. Please send a valid HTTP request."
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        # Extraer la línea de solicitud HTTP
        request_line = request_data.split('\r\n')[0]
        method, path, protocol = request_line.split()

        print(f"Request: {method} {path} {protocol}")

        # Análisis de encabezados
        headers = {}
        for line in request_data.split('\r\n')[1:]:
            if not line.strip():
                break
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        # Validar Authorization
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

        # Casos de prueba con diferentes métodos
        if method == "GET":
            if path == "/secure":
                response_body = "GET request successful! You accessed a protected resource."
            else:
                response_body = f"GET request successful! Path: {path}."

        elif method == "POST":
            try:
                content_length = int(headers.get("Content-Length", 0))
                body = request_data.split("\r\n\r\n")[1][:content_length]

                if headers.get("Content-Type") == "application/json":
                    response_body = f"POST request successful! JSON data received: {body}."
                elif headers.get("Content-Type") == "application/xml":
                    response_body = f"POST request successful! XML data received: {body}."
                else:
                    response_body = f"POST request successful! Plain text or unknown content type received: {body}."
            except (IndexError, ValueError):
                raise ValueError("POST request failed. Body is missing or malformed.")

        elif method == "HEAD":
            response_body = "HEAD request successful! Only headers are sent in this response."

        elif method == "PUT":
            response_body = f"PUT request successful! Resource '{path}' would be updated if this were implemented."

        elif method == "DELETE":
            response_body = f"DELETE request successful! Resource '{path}' would be deleted if this were implemented."

        elif method == "OPTIONS":
            response_headers = [
                "HTTP/1.1 204 No Content",
                "Allow: GET, POST, HEAD, PUT, DELETE, OPTIONS",
                "Content-Length: 0"
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n"
            client_socket.sendall(response.encode())
            client_socket.close()
            return
        
        elif method == "TRACE":
            # Devuelve la solicitud completa como cuerpo de respuesta
            response_body = request_data
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: message/http",
                f"Content-Length: {len(response_body)}"
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

        elif method == "CONNECT":
            response_body = "CONNECT method received. Tunneling not implemented in this server."
            response_headers = [
                "HTTP/1.1 501 Not Implemented",  # Normalmente no implementado en servidores básicos
                "Content-Type: text/plain",
                f"Content-Length: {len(response_body)}"
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

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

    except ValueError as ve:
        # Error 400: Solicitud malformada
        response = f"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request: {ve}"
    except FileNotFoundError:
        # Error 404: Recurso no encontrado
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nThe requested resource was not found."
    except Exception as e:
        # Error 500: Problema interno del servidor
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nServer error: {e}"

    # Enviar la respuesta
    client_socket.sendall(response.encode())
    client_socket.close()

# Función para correr el servidor
def run_server(host='', port=8888):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Inicia el servidor
if __name__ == "__main__":
    run_server()
