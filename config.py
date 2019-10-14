class Config:

    def __init__(self, address = '/etc/httpd.conf'):

        self.root = '/var/www/html'
        self.threadCount = 16

        try:
            with open(address, 'r') as file:
                for line in file:
                    key, value = line.split(' ')

                    if key == 'thread_limit':
                        self.threadCount = int(value)
                    elif key == 'document_root':
                        self.root = value
                        if self.root[-1] == '/':
                            self.root = self.root[:-1]
        except FileNotFoundError:
            return
