package apiserver

import (
	"context"

	"github.com/gin-contrib/pprof"
	"github.com/gin-gonic/gin"
	"github.com/pachirode/pkg/core"

	handler "github.com/pachirode/ffmpeg-study/internal/apiserver/handler/http"
	"github.com/pachirode/ffmpeg-study/internal/pkg/errno"
	"github.com/pachirode/ffmpeg-study/internal/pkg/server"
)

type ginServer struct {
	srv server.Server
}

var _ server.Server = (*ginServer)(nil)

func (c *ServerConfig) NewGinServer() server.Server {
	// 创建 Gin 引擎
	engine := gin.New()

	// 注册全局中间件
	engine.Use(gin.Recovery())

	// 注册 REST API 路由
	c.InstallRESTAPI(engine)

	httpSrv := server.NewHTTPServer(c.cfg.HTTPOptions, c.cfg.TLSOptions, engine)

	return &ginServer{srv: httpSrv}
}

func (c *ServerConfig) InstallRESTAPI(engine *gin.Engine) {
	// 注册业务无关的 API 接口
	InstallGenericAPI(engine)

	// 创建核心业务处理器
	handler := handler.NewHandler(c.biz, c.val)

	// 注册健康检查接口
	engine.GET("/healthz", handler.Healthz)
}

func InstallGenericAPI(engine *gin.Engine) {
	// 注册 pprof 路由
	pprof.Register(engine)

	// 注册 404 路由处理
	engine.NoRoute(func(c *gin.Context) {
		core.WriteResponse(c, errno.ErrPageNotFound, nil)
	})
}

func (s *ginServer) RunOrDie() {
	s.srv.RunOrDie()
}

func (s *ginServer) GracefulStop(ctx context.Context) {
	s.srv.GracefulStop(ctx)
}
