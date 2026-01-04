.DEFAULT_GOAL := help

.PHONY: all
all: format tidy gen lint cover build

include scripts/make-rules/common.mk
include scripts/make-rules/common-versions.mk
include scripts/make-rules/all.mk

# ==============================================================================
# Usage

define USAGE_OPTIONS

选项:
  BINS             要构建的二进制文件。默认值为cmd中的所有文件。
                   此选项可用于以下命令：make build
                   示例：make build BINS="apiserver"
  VERSION          编译到二进制文件中的版本信息。
  V                设置为1以启用详细的构建信息输出。默认值为0。
endef
export USAGE_OPTIONS

.PHONY: format
format: # 格式化 Go 源码.
	@gofmt -s -w ./

.PHONY: tidy
tidy: # 自动添加/移除依赖包.
	@go mod tidy

.PHONY: protoc
protoc: ## Generate api proto files.
	$(MAKE) gen.protoc

.PHONY: clean
clean: ## Remove all artifacts that are created by building and generaters.
	@echo "===========> Cleaning all build output"
	@-rm -vrf $(OUTPUT_DIR)

ca: ## 生成 CA 文件.
	@$(MAKE) gen.ca
