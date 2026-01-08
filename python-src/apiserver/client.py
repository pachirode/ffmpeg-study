import grpc
from apiserver.v1 import apiserver_pb2, apiserver_pb2_grpc, audio_pb2


def pull_audio_stream(stream_id: str, server_addr: str = "localhost:6666"):
    # 建立 gRPC 连接
    channel = grpc.insecure_channel(server_addr)
    stub = apiserver_pb2_grpc.FFmpegAudioStreamServiceStub(channel)

    # 构造请求
    request = audio_pb2.StartAudioStreamRequest(stream_id=stream_id)

    # 调用 PullAudioStream 获取流
    try:
        for audio_packet in stub.PullAudioStream(request):
            meta = audio_packet.meta
            print(f"Received AudioPacket - StreamID: {meta.stream_id}, Codec: {meta.codec}, "
                  f"SampleRate: {meta.sample_rate}, Channels: {meta.channels}, "
                  f"PTS: {meta.pts.seconds}.{meta.pts.nanos}, DataLen: {len(audio_packet.data)} bytes")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    pull_audio_stream("test123")
