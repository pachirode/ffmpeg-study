package apiserver

import (
	"context"

	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"

	handler "github.com/pachirode/ffmpeg-study/internal/apiserver/handler/grpc"
	"github.com/pachirode/ffmpeg-study/internal/pkg/server"
	apiv1 "github.com/pachirode/ffmpeg-study/pkg/api/apiserver/v1"
)

type grpcServer struct {
	srv  server.Server
	stop func(context.Context)
}

var _ server.Server = (*grpcServer)(nil)

func (c *ServerConfig) NewGRPCServerOr() (server.Server, error) {
	// 配置 gRPC 服务器选项，包括拦截器链
	serverOptions := []grpc.ServerOption{
		// 注意拦截器顺序！
		grpc.ChainUnaryInterceptor(),
	}

	// 创建 gRPC 服务器
	grpcSrv, err := server.NewGRPCServer(
		c.cfg.GRPCOptions,
		c.cfg.TLSOptions,
		serverOptions,
		func(s grpc.ServiceRegistrar) {
			apiv1.RegisterFFmpegAudioStreamServiceServer(s, handler.NewHandler(c.biz))
		},
	)
	if err != nil {
		return nil, err
	}

	if c.cfg.ServerMode == GRPCServerMode {
		return &grpcServer{
			srv: grpcSrv,
			stop: func(ctx context.Context) {
				grpcSrv.GracefulStop(ctx)
			},
		}, nil
	}

	// 先启动 gRPC 服务器，因为 HTTP 服务器依赖 gRPC 服务器.
	go grpcSrv.RunOrDie()

	httpSrv, err := server.NewGRPCGatewayServer(
		c.cfg.HTTPOptions,
		c.cfg.GRPCOptions,
		c.cfg.TLSOptions,
		func(mux *runtime.ServeMux, conn *grpc.ClientConn) error {
			return apiv1.RegisterFFmpegAudioStreamServiceHandler(context.Background(), mux, conn)
		},
	)
	if err != nil {
		return nil, err
	}

	return &grpcServer{
		srv: httpSrv,
		stop: func(ctx context.Context) {
			grpcSrv.GracefulStop(ctx)
			httpSrv.GracefulStop(ctx)
		},
	}, nil
}

// RunOrDie 启动 gRPC 服务器或 HTTP 反向代理服务器，异常时退出.
func (s *grpcServer) RunOrDie() {
	s.srv.RunOrDie()
}

// GracefulStop 优雅停止 HTTP 和 gRPC 服务器.
func (s *grpcServer) GracefulStop(ctx context.Context) {
	s.stop(ctx)
}
