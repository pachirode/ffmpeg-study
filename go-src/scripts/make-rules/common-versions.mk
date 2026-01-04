GOLANGCI_LINT_VERSION := v1.55.2
GO_IMPORTS_VERSION ?= v0.14.2
GO_SWAGGER_VERSION ?= v0.31.0

GRPC_GATEWAY_VERSION ?= $(call get_go_version,github.com/grpc-ecosystem/grpc-gateway/v2)
KRATOS_VERSION ?= $(call get_go_version,github.com/go-kratos/kratos/v2)
PROTOC_GEN_VALIDATE_VERSION ?= $(call get_go_version,github.com/envoyproxy/protoc-gen-validate)
PROTOC_GEN_GO_VERSION ?= $(call get_go_version,google.golang.org/protobuf)
PROTOC_GEN_GO_GRPC_VERSION ?= $(call get_go_version,google.golang.org/grpc)
CODE_GENERATOR_VERSION ?= $(call get_go_version,k8s.io/code-generator)
WIRE_VERSION ?= $(call get_go_version,github.com/google/wire)
MOCKGEN_VERSION ?= $(call get_go_version,github.com/golang/mock)
