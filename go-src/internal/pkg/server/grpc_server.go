package server

import (
	"context"
	"net"

	"github.com/pachirode/pkg/log"
	genericoptions "github.com/pachirode/pkg/options"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/health"
	"google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/reflection"
)

type GRPCServer struct {
	srv *grpc.Server
	lis net.Listener
}

func NewGRPCServer(
	grpcOptions *genericoptions.GRPCOptions,
	tlsOptions *genericoptions.TLSOptions,
	serverOptions []grpc.ServerOption,
	registerServer func(grpc.ServiceRegistrar),
) (*GRPCServer, error) {
	lis, err := net.Listen("tcp", grpcOptions.Addr)
	if err != nil {
		log.Errorw(err, "Failed to listen", "err")
		return nil, err
	}

	if tlsOptions != nil && tlsOptions.UseTLS {
		tlsConfig := tlsOptions.MustTLSConfig()
		serverOptions = append(serverOptions, grpc.Creds(credentials.NewTLS(tlsConfig)))
	}

	grpcSrv := grpc.NewServer(serverOptions...)

	registerServer(grpcSrv)
	registerHealthServer(grpcSrv)
	reflection.Register(grpcSrv)

	return &GRPCServer{
		srv: grpcSrv,
		lis: lis,
	}, nil
}

func (s *GRPCServer) RunOrDie() {
	log.Infow("Start to listening the incoming requests", "protocol", "grpc", "addr", s.lis.Addr().String())
	if err := s.srv.Serve(s.lis); err != nil {
		log.Fatalw("Failed to serve grpc server", "err", err)
	}
}

func (s *GRPCServer) GracefulStop(ctx context.Context) {
	log.Infow("Gracefully stop grpc server")
	s.srv.GracefulStop()
}

func registerHealthServer(grpcSrv *grpc.Server) {
	healthServer := health.NewServer()
	healthServer.SetServingStatus("ffmpeg-study", grpc_health_v1.HealthCheckResponse_SERVING)
	grpc_health_v1.RegisterHealthServer(grpcSrv, healthServer)
}
