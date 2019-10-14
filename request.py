from urllib import parse

methodGET = 'GET'
methodHEAD = 'HEAD'


class Request:

    def __init__(self):
        self.method = ''
        self.url = ''
        self.version = ''
        self.headers = {}

    def addHeader(self, key: str, value: str):
        self.headers[key.strip()] = value.strip()

    def setUrl(self, newUrl: str):
        newUrl = parse.unquote(newUrl)
        sep = newUrl.find('?') if newUrl.find('?') != -1 else newUrl.find('#')
        if sep != -1:
            newUrl = newUrl[:sep]

        self.url = newUrl