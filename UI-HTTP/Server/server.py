import socket
from threading import Thread
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mandi1709',
    'database': 'ventas'
}

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()

    # Extraer la línea de solicitud HTTP
    request_line = request_data.split('\r\n')[0]
    method, path, protocol = request_line.split()

    # Mostrar la solicitud recibida
    print(f"Request: {method} {path} {protocol}")

    # Construir la respuesta HTTP
    if method == 'GET':
        try:
            # Conexión a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            table = path.split("/")[-1]
            # Ejecutar consulta para obtener datos
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            # Construir la respuesta HTTP con los datos obtenidos
            response_body = ""
            for row in rows:
                response_body += f"{row}\r\n"

            # Cerrar la conexión a la base de datos
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Error:", err)
            response_body = "Error retrieving data from MySQL"

    elif method == 'POST':
        try:
            content_length = int(request_data.split('Content-Length: ')[1].split('\r\n')[0])
            request_body = request_data.split('\r\n\r\n')[1][:content_length]

            # Conexión a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            table = path.split("/")[-1]
            # Ejecutar inserción de datos en la base de datos
            cursor.execute(f"INSERT INTO {table} (`NoC`, `NoP`, `Fecha`, `Cantidad`) VALUES ({request_body})")
            conn.commit()

            response_body = "Data inserted successfully into MySQL"

            # Cerrar la conexión a la base de datos
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Error:", err)
            response_body = "Error inserting data into MySQL"

    elif method == 'HEAD':
        response_body = ""

    else:
        response_body = "Unsupported Method"

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