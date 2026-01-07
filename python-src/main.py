from common.log import LoggerManager
from common.server import Server
from apiserver.v1 import apiserver_pb2_grpc
from apps.apiserver.view import FFmpegAudioStreamServicer

logger = LoggerManager.get_logger()


def main():
    server = Server("0.0.0.0", "8082")
    apiserver_pb2_grpc.add_FFmpegAudioStreamServiceServicer_to_server(FFmpegAudioStreamServicer(), server.server)
    server.run()


if __name__ == '__main__':
    main()
