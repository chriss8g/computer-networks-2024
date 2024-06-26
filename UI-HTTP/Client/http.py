import socket

def send_request(method, url, data=None, headers=None, content_type="application/json"):
    try:
        # Parse URL to extract host, port, and resource
        host, port, resource = parse_url(url)

        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the server
        client_socket.connect((host, port))

        # Build the HTTP request
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

        # Send the request to the server
        client_socket.sendall(http_request.encode())

        # Receive and display the server's response
        response = receive_response(client_socket)

        if not response:
            return "Error: No response received from the server", "", ""

        status, body, response_headers = parse_response(response)

        # Close the connection
        client_socket.close()

        return status, body, response_headers

    except socket.error as e:
        return f"Socket error: {str(e)}", "", ""
    except socket.timeout:
        return "Connection timeout while connecting to the server", "", ""

def parse_url(url):
    # Remove the protocol if present
    if '://' in url:
        url = url.split('://')[1]

    # Split the URL into host, port, and resource
    parts = url.split('/')
    host_port = parts[0].split(':')
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 80
    resource = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'

    return host, port, resource

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
#     # URL del servidor
#     server_url = "http://localhost:8000"

#     # Ejemplo de solicitud GET
#     requested_resource_get = "/api/tournament/"
#     status, body, response_headers = send_request("GET", server_url + requested_resource_get)
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
#     status, body, response_headers = send_request("POST", server_url + requested_resource_post, data=post_data, headers=headers, content_type="application/json")
#     print("POST request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
    
#     # Ejemplo de solicitud POST con datos en el cuerpo en formato XML
#     post_data_xml = "<data><value>example</value></data>"
#     status, body, response_headers = send_request("POST", server_url + requested_resource_post, data=post_data_xml, content_type="application/xml")
#     print("POST request (XML):")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
    
#     # Ejemplo de solicitud POST con datos en el cuerpo en formato de formulario
#     post_data_form = "name=John&age=30"
#     status, body, response_headers = send_request("POST", server_url + requested_resource_post, data=post_data_form, content_type="application/x-www-form-urlencoded")
#     print("POST request (Form):")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud PUT con datos en el cuerpo en formato JSON
#     requested_resource_put = "/api/tournament/11/"
#     put_data = """{
#         "name": "talla"
#     }"""
#     status, body, response_headers = send_request("PUT", server_url + requested_resource_put, data=put_data)
#     print("PUT request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud DELETE
#     requested_resource_delete = "/api/tournament/11/"
#     status, body, response_headers = send_request("DELETE", server_url + requested_resource_delete)
#     print("DELETE request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
    
#     # Ejemplo de solicitud HEAD
#     requested_resource_head = "/api/tournament/"
#     status, body, response_headers = send_request("HEAD", server_url + requested_resource_head)
#     print("HEAD request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud OPTIONS
#     requested_resource_options = "/api/tournament/"
#     status, body, response_headers = send_request("OPTIONS", server_url + requested_resource_options)
#     print("OPTIONS request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud CONNECT
#     requested_resource_connect = "/api/tournament/"
#     status, body, response_headers = send_request("CONNECT", server_url + requested_resource_connect)
#     print("CONNECT request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")

#     # Ejemplo de solicitud TRACE
#     requested_resource_trace = "/api/tournament/"
#     status, body, response_headers = send_request("TRACE", server_url + requested_resource_trace)
#     print("TRACE request:")
#     print("Status:", status)
#     print("Response Body:", body)
#     print("Response Headers:", response_headers)
#     print("-----------------------------------")
