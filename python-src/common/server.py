import grpc

from concurrent import futures

from utils import config
from utils.log import LoggerManager

logger = LoggerManager.get_logger()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=20), options=config.grpc_options)

    def run(self):
        self.server.add_insecure_port(f'{self.host}:{self.port}')
        self.server.start()
        logger.info(f"Grpc Server running in {self.host}:{self.port}")
        self.server.wait_for_termination()
