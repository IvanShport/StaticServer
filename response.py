
statuses = {
    200: '200 OK',
    400: '400 Bad Request',
    403: '403 Forbidden',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
}

types = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash',
    'txt': 'text/plain'
}

version1_1 = 'HTTP/1.1'


class Response:

    def __init__(self, version=version1_1, status=statuses[200]):
        self.status = status
        self.version = version
        self.headers = {}
        self.body = ''

    def addHeader(self, key: str, value: str):
        self.headers[key.strip()] = value.strip()

    def serialize(self) -> bytes:
        buffer = ' '.join([self.version, self.status])
        buffer += '\r\n'
        for items in self.headers.items():
            buffer += ': '.join(items)
            buffer += '\r\n'
        buffer += '\r\n'

        buffer = buffer.encode()

        if self.body != '':
            buffer += self.body

        return buffer

def closeConnection(resp: Response) -> Response:
    resp.addHeader('Connection', 'close')
    resp.addHeader('Server', 'server/1.0')
    return resp

def defineContentType(fileName: str) -> str:
    chunks = fileName.rsplit('.', 1)

    if len(chunks) != 2:
        return 'application/octet-stream'
    extention = chunks[1]
    ct = types.get(extention)

    return ct or 'application/octet-stream'
