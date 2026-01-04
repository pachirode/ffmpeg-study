# 调用 ffmpeg 作为服务器处理 mp3 文件
### 环境安装

```bash
# 安装 protoc 相关
make tools.install
```

### 运行

```bash
go run cmd/apiserver/main.go -c configs/server-apiserver.yaml
curl -k https://127.0.0.1:5555/healthz
{"timestamp":"2026-01-04 16:04:31"}
```

### Swagger

```bash
# 生成 yaml
make swagger.run
# 启动 swagger 服务
make swagger.serve
```
