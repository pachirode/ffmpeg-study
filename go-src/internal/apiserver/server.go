package apiserver

import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/pachirode/pkg/log"
	genericoptions "github.com/pachirode/pkg/options"

	"github.com/pachirode/ffmpeg-study/internal/apiserver/biz"
	"github.com/pachirode/ffmpeg-study/internal/apiserver/pkg/validation"
	"github.com/pachirode/ffmpeg-study/internal/pkg/server"
)

const (
	// GRPCServerMode 定义 gRPC 服务模式.
	// 使用 gRPC 框架启动一个 gRPC 服务器.
	GRPCServerMode = "grpc"
	// GRPCGatewayServerMode 定义 gRPC + HTTP 服务模式.
	// 使用 gRPC 框架启动一个 gRPC 服务器 + HTTP 反向代理服务器.
	GRPCGatewayServerMode = "grpc-gateway"
	// GinServerMode 定义 Gin 服务模式.
	// 使用 Gin Web 框架启动一个 HTTP 服务器.
	GinServerMode = "gin"
)

// Config 配置结构体，用于存储应用相关的配置.
// 不用 viper.Get，是因为这种方式能更加清晰的知道应用提供了哪些配置项.
type Config struct {
	ServerMode        string
	JWTKey            string
	Expiration        time.Duration
	EnableMemoryStore bool
	TLSOptions        *genericoptions.TLSOptions
	HTTPOptions       *genericoptions.HTTPOptions
	GRPCOptions       *genericoptions.GRPCOptions
	MySQLOptions      *genericoptions.MySQLOptions
}

type UnionServer struct {
	srv server.Server
}

// ServerConfig 包含服务器的核心依赖和配置.
type ServerConfig struct {
	cfg *Config
	biz biz.IBiz
	val *validation.Validator
}

// NewUnionServer 根据配置创建联合服务器.
func (cfg *Config) NewUnionServer() (*UnionServer, error) {
	log.Infow("Initializing federation server", "server-mode", cfg.ServerMode, "enable-memory-store", cfg.EnableMemoryStore)

	// 创建服务配置，这些配置可用来创建服务器
	serverConfig, err := cfg.NewServerConfig()
	if err != nil {
		return nil, err
	}

	log.Infow("Initializing federation server", "server-mode", cfg.ServerMode)

	var srv server.Server
	switch cfg.ServerMode {
	case GinServerMode:
		srv, err = serverConfig.NewGinServer(), nil
	default:
		srv, err = serverConfig.NewGRPCServerOr()
	}
	if err != nil {
		return nil, err
	}

	return &UnionServer{srv: srv}, nil
}

// Run 运行应用.
func (s *UnionServer) Run() error {
	go s.srv.RunOrDie()

	// 创建一个 os.Signal 类型的 channel，用于接收系统信号
	quit := make(chan os.Signal, 1)
	// 当执行 kill 命令时（不带参数），默认会发送 syscall.SIGTERM 信号
	// 使用 kill -2 命令会发送 syscall.SIGINT 信号（例如按 CTRL+C 触发）
	// 使用 kill -9 命令会发送 syscall.SIGKILL 信号，但 SIGKILL 信号无法被捕获，因此无需监听和处理
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	// 阻塞程序，等待从 quit channel 中接收到信号
	<-quit

	log.Infow("Shutting down server ...")

	// 优雅关闭服务
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// 先关闭依赖的服务，再关闭被依赖的服务
	s.srv.GracefulStop(ctx)

	log.Infow("Server exited")
	return nil
}
func (cfg *Config) NewServerConfig() (*ServerConfig, error) {

	return &ServerConfig{
		cfg: cfg,
		biz: biz.NewBiz(),
		val: validation.New(),
	}, nil
}
