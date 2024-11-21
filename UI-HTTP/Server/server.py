import socket
from threading import Thread

# Función para manejar cada cliente
def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()
    # Extraer la línea de solicitud HTTP
    request_line = request_data.split('\r\n')[0]
    method, path, protocol = request_line.split()

    print(f"Request: {method} {path} {protocol}")

    # Casos de prueba para métodos HTTP
    if method == "GET":
        if path == "/hello":
            response_body = "Hello, world!"
        elif path == "/empty":
            response_body = ""
        else:
            response_body = f"GET request received for {path}"
    
    elif method == "POST":
        # Leer el cuerpo de la solicitud
        try:
            content_length = int(request_data.split("Content-Length: ")[1].split('\r\n')[0])
            request_body = request_data.split('\r\n\r\n')[1][:content_length]
            response_body = f"POST data received: {request_body}"
        except (IndexError, ValueError):
            response_body = "Invalid POST request"
    
    elif method == "HEAD":
        response_body = ""
    
    elif method == "PUT":
        response_body = "PUT method received but not implemented"
    
    elif method == "DELETE":
        response_body = f"DELETE request received for {path}"
    
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

    else:
        response_body = "Unsupported HTTP method"

    # Construir la respuesta HTTP
    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain",
        f"Content-Length: {len(response_body)}"
    ]
    response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

    # Enviar la respuesta al cliente
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
