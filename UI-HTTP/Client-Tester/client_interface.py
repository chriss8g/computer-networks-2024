class HttpClient:
    def send_request(self, method, url, headers=None, data=None):
        """
        Enviar una solicitud HTTP.

        :param method: Método HTTP (GET, POST, etc.)
        :param url: URL completa del servidor
        :param headers: Diccionario con los encabezados HTTP
        :param data: Cuerpo de la solicitud
        :return: HttpResponse con status_code, body y headers
        """
        raise NotImplementedError("send_request must be implemented by subclasses")


class HttpResponse:
    def __init__(self, status_code, body, headers):
        """
        Clase para encapsular las respuestas HTTP.

        :param status_code: Código de estado HTTP (int)
        :param body: Cuerpo de la respuesta (str)
        :param headers: Encabezados de la respuesta (dict)
        """
        self.status_code = status_code
        self.body = body
        self.headers = headers
