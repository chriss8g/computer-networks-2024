import socket

def send_request(host, port, method, resource, data=None, headers=None, content_type=None):
    try:
        # Crear un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conectar el socket al servidor
        client_socket.connect((host, port))

        # Construir la solicitud HTTP
        http_request = f"{method} {resource} HTTP/1.1\r\n" \
                       f"Host: {host}\r\n"

        if headers:
            for header, value in headers.items():
                http_request += f"{header}: {value}\r\n"

        if content_type:
            http_request += f"Content-Type: {content_type}\r\n"

        if data:
            content_length = len(data)
            http_request += f"Content-Length: {content_length}\r\n\r\n" \
                            f"{data}"
        else:
            http_request += "\r\n"

        # Enviar la solicitud al servidor
        client_socket.sendall(http_request.encode())

        # Recibir y mostrar la respuesta del servidor
        response = receive_response(client_socket)

        if not response:
            return "Error: No se recibió respuesta del servidor", "", ""

        status, body, response_headers = parse_response(response)

        # Cerrar la conexión
        client_socket.close()

        return status, body, response_headers

    except socket.error as e:
        return f"Error de socket: {str(e)}", "", ""
    except socket.timeout:
        return "Tiempo de espera agotado al conectar al servidor", "", ""

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

def parse_response(response):

    # Separa la respuesta en status, headers y body
    headers, body = response.split('\r\n\r\n', 1)
    
    # # Separa el status en el código y el mensaje
    # status_code, status_message = status_line.split(' ', 1)
    
    # # Parsea los headers en un diccionario
    # headers_dict = {}
    first = True
    newHeaders = ""
    status_line = ""
    for header in headers.split('\r\n'):
        if first:
            status_line = header
            first = False
        else:
            newHeaders = newHeaders + header + '\r\n'
    newHeaders = newHeaders[:-2]
    return status_line, body, newHeaders

# if __name__ == "__main__":
#     # Server configuration
#     server_host = "localhost"
#     server_port = 8000

#     # Ejemplo de solicitud GET
#     requested_resource_get = "/api/tournament/"
#     status, body, response_headers = send_request(server_host, server_port, "GET", requested_resource_get)
#     print("GET request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud POST con datos en el cuerpo en formato JSON
#     requested_resource_post = "/api/tournament/"
#     post_data = """{
#         "name": "s"
#     }"""
#     headers = {
#         "User-Agent": "MiAplicacion/1.0",
#         "Authorization": "Bearer token"
#     }
#     status, body, response_headers = send_request(server_host, server_port, "POST", requested_resource_post, post_data, headers=headers, content_type="application/json")
#     print("POST request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
    
#     # Ejemplo de solicitud POST con datos en el cuerpo en formato XML
#     post_data_xml = "<data><value>example</value></data>"
#     status, body, response_headers = send_request(server_host, server_port, "POST", requested_resource_post, post_data_xml, content_type="application/xml")
#     print("POST request (XML):")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
    
#     # Ejemplo de solicitud POST con datos en el cuerpo en formato de formulario
#     post_data_form = "name=John&age=30"
#     status, body, response_headers = send_request(server_host, server_port, "POST", requested_resource_post, post_data_form, content_type="application/x-www-form-urlencoded")
#     print("POST request (Form):")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud PUT con datos en el cuerpo en formato JSON
#     requested_resource_put = "/api/tournament/4/"
#     put_data = """{
#         "name": "talla"
#     }"""
#     status, body, response_headers = send_request(server_host, server_port, "PUT", requested_resource_put, put_data)
#     print("PUT request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud DELETE
#     requested_resource_delete = "/api/tournament/4/"
#     status, body, response_headers = send_request(server_host, server_port, "DELETE", requested_resource_delete)
#     print("DELETE request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")