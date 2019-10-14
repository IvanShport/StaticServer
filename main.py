from config import Config
from server import Server

if __name__ == '__main__':
    cfg = Config()

    srv = Server(cfg)
    srv.run()
