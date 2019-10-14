import os
from socket import socket
from request import Request
from response import Response, statuses, closeConnection, defineContentType

separator = '\r\n'
maxRequestLen = 64 * 1024

def handleSocket(sock: socket, root: str):
    while True:
        print('started')
        clientSock, info = sock.accept()

        data = readFromSocket(clientSock)
        if data:
            response = httpHandler(data, root)
            if response != '':
                writeToSocket(clientSock, response)

        clientSock.close()

def readFromSocket(clientSock: socket) -> str:
    buffer = ''

    while True:
        data = clientSock.recv(1024)

        if not data:
            return ''

        buffer += data.decode()
        if buffer.find('\r\n\r\n'):
            break
        if len(buffer) >= maxRequestLen:
            return ''

    return buffer

def writeToSocket(clientSock: socket, data: bytes):
    pos = 0
    while pos < len(data):
        wrote = clientSock.send(data[pos:pos + 1024])
        if wrote == 0:
            return
        pos += wrote

def httpHandler(data: str, root: str) -> bytes:
    firstLineParsed = False
    request = Request()
    for line in data.split('\r\n')[:-2]:
        if not firstLineParsed:
            chunks = line.split(' ')
            if len(chunks) != 3:
                return ''
            request.method = chunks[0]
            request.setUrl(chunks[1])
            request.version = chunks[2]
            firstLineParsed = True
        else:
            chunks = line.split(':', 1)
            if len(chunks) != 2:
                return ''
            request.addHeader(chunks[0], chunks[1])

    return handleHttpRequest(request, root).serialize()

def handleHttpRequest(request: Request, root: str) -> Response:
    if request.url == '':
        return Response()

    needBody = False
    if request.method == 'GET':
        needBody = True
    elif request.method == 'HEAD':
        needBody = False
    else:
        return closeConnection(Response(status=statuses[405]))

    isDir = False
    path = root + request.url

    if request.url[-1] == '/':
        isDir = True
        path += 'index.html'

    if path.find('../') != -1:
        return closeConnection(Response(status=statuses[403]))

    resp = Response()

    if needBody:
        try:
            with open(path, 'rb') as file:
                resp.body = file.read()
                resp.addHeader('Content-Length', str(len(resp.body)))
        except FileNotFoundError:
            if isDir:
                return closeConnection(Response(status=statuses[403]))
            else:
                return closeConnection(Response(status=statuses[404]))
    else:

        resp.addHeader('Content-Length', str(os.lstat(path).st_size))

    resp.addHeader('Content-Type', defineContentType(path))
    return closeConnection(resp)

# todo:

