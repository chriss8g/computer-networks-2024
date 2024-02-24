import socket
import json

def send_request(host, port, method, resource, data=None):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server
    client_socket.connect((host, port))
    print(f"Conectado a {host}:{port}")

    # Build the HTTP request
    if data:
        data_json = json.dumps(data)
        content_length = len(data_json)
        http_request = f"{method} {resource} HTTP/1.1\r\n" \
                    f"Host: {host}\r\n" \
                    f"Content-Type: application/json\r\n" \
                    f"Content-Length: {content_length}\r\n\r\n" \
                    f"{data_json}"
    else:
        http_request = f"{method} {resource} HTTP/1.1\r\n" \
                       f"Host: {host}\r\n\r\n"

    # Send the request to the server
    client_socket.sendall(http_request.encode())
    print(f"{method} Request enviado...")

    # Receive and display the server's response
    response = receive_response(client_socket)
    print(response)
    # Close the connection
    client_socket.close()

def receive_response(socket, timeout=2):
    response = b""
    socket.settimeout(timeout)  # Establecer el tiempo de espera en segundos

    try:
        while True:
            fragment = socket.recv(1024)
            if not fragment:
                break
            response += fragment
    except OSError as e:
        if "timed out" not in str(e):
            raise  # Si la excepción no es un timeout, relanzarla

    return response.decode("utf-8")

if __name__ == "__main__":
    # Server configuration
    server_host = "localhost"
    server_port = 8000

    # Ejemplo de solicitud GET
    requested_resource_get = "/api/season/"
    send_request(server_host, server_port, "GET", requested_resource_get)

    # Ejemplo de solicitud POST con datos en el cuerpo en formato JSON
    requested_resource_post = "/api/season/"
    post_data = {
    "title": "s",
    "year": 7,
    "edition": "f"
    }
    send_request(server_host, server_port, "POST", requested_resource_post, post_data)

    # Ejemplo de solicitud PUT con datos en el cuerpo en formato JSON
    requested_resource_put = "/api/season/4/"
    put_data = {
    "title": "talla",
    "year": 7,
    "edition": "f"
    }
    send_request(server_host, server_port, "PUT", requested_resource_put, put_data)

    # Ejemplo de solicitud DELETE
    requested_resource_delete = "/api/season/5/"
    send_request(server_host, server_port, "DELETE", requested_resource_delete)
