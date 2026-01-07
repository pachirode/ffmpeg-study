import grpc

from concurrent import futures

from common import config
from common.log import LoggerManager

LoggerManager.init()
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
