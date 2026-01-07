from apiserver.v1 import apiserver_pb2_grpc, apiserver_pb2, healthz_pb2


class FFmpegAudioStreamServicer(apiserver_pb2_grpc.FFmpegAudioStreamService):

    def Healthz(self, request, context):
        return healthz_pb2.HealthzResponse()

