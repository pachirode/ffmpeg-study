# ==============================================================================
# 工具相关的 Makefile
#

CI_WORKFLOW_TOOLS := golangci-lint goimports wire

PROTOC_TOOLS := protoc-plugins protolint

TOOLS := ${CI_WORKFLOW_TOOLS} ${PROTOC_TOOLS}

tools.verify: $(addprefix tools.verify., $(TOOLS))

tools.install: $(addprefix tools.install., $(TOOLS))

tools.install.%:
	@echo "===========> Installing $*"
	@$(MAKE) install.$*

tools.verify.%:
	@if ! which $* &>/dev/null; then $(MAKE) tools.install.$*; fi

install.wire:
	@$(GO) install github.com/google/wire/cmd/wire@$(WIRE_VERSION)

install.golangci-lint:
	@$(GO) install github.com/golangci/golangci-lint/cmd/golangci-lint@$(GOLANGCI_LINT_VERSION)
	@golangci-lint completion bash > $(HOME)/.golangci-lint.bash
	@if ! grep -q .golangci-lint.bash $(HOME)/.bashrc; then echo "source \$$HOME/.golangci-lint.bash" >> $(HOME)/.bashrc; fi

install.goimports:
	@$(GO) install golang.org/x/tools/cmd/goimports@$(GO_IMPORTS_VERSION)

install.protoc-plugins:
	@$(GO) install google.golang.org/protobuf/cmd/protoc-gen-go@$(PROTOC_GEN_GO_VERSION)
	@$(GO) install google.golang.org/grpc/cmd/protoc-gen-go-grpc@$(PROTOC_GEN_GO_GRPC_VERSION)
	@$(GO) install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@$(GRPC_GATEWAY_VERSION)
	@$(GO) install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@$(GRPC_GATEWAY_VERSION)
	@$(SCRIPTS_DIR)/install-protoc.sh

install.redis:
	@$(SCRIPTS_DIR)/install-redis.sh

install.swagger:
	@$(GO) install github.com/go-swagger/go-swagger/cmd/swagger@$(GO_SWAGGER_VERSION)

install.protolint:
	@$(GO) install github.com/yoheimuta/protolint/cmd/protolint@latest

# 伪目标（防止文件与目标名称冲突）
.PHONY: tools.verify tools.install tools.install.% tools.verify.% install.golangci-lint \
	install.goimports install.protoc-plugins install.swagger \
	protolint
