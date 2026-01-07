import os
import sys


def run_protoc():
    # 设置命令，包含proto文件路径、输出路径以及插件选项
    protoc_command = (
        f"{sys.executable} -m grpc_tools.protoc "
        "--proto_path=./api "  # proto文件的根目录
        "--proto_path=./third_party/protobuf "  # 需要指定所有依赖proto文件的目录
        "--python_out=./ "  # 生成Python代码的输出目录
        "--grpc_python_out=./ "  # 生成gRPC Python代码的输出目录
        "./api/apiserver/v1/apiserver.proto "
        "./api/apiserver/v1/audio.proto "
        "./api/apiserver/v1/healthz.proto "  # 目标proto文件
    )

    # 执行protoc命令
    os.system(protoc_command)


if __name__ == "__main__":
    run_protoc()
