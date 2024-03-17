import socket
from threading import Thread

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()

    # Extraer la línea de solicitud HTTP
    request_line = request_data.split('\r\n')[0]
    method, path, protocol = request_line.split()

    # Mostrar la solicitud recibida
    print(f"Request: {method} {path} {protocol}")

    # Construir la respuesta HTTP
    if method == 'GET':
        response_body = "<html><body><h1>Hello, World!</h1></body></html>"
    elif method == 'POST':
        content_length = int(request_data.split('Content-Length: ')[1].split('\r\n')[0])
        request_body = request_data.split('\r\n\r\n')[1]
        response_body = f"<html><body><h1>POST Data Received:</h1><p>{request_body}</p></body></html>"
    elif method == 'HEAD':
        response_body = ""
    else:
        response_body = "<html><body><h1>Unsupported Method</h1></body></html>"

    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {len(response_body)}"
    ]
    response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

    # Enviar la respuesta al cliente
    client_socket.sendall(response.encode())

    # Cerrar la conexión con el cliente
    client_socket.close()

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

if __name__ == '__main__':
    run_server()