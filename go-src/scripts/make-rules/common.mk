# ==============================================================================
# 定义全局 Makefile 变量方便后面引用

SHELL := /bin/bash

COMMON_SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
# 项目根目录
ifeq ($(origin PROJ_ROOT_DIR),undefined)
PROJ_ROOT_DIR :=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
endif

GO := go

SCRIPTS_DIR="${PROJ_ROOT_DIR}/scripts"

# 构建产物、临时文件存放目录
OUTPUT_DIR := $(PROJ_ROOT_DIR)/_output

# 定义包名
ROOT_PACKAGE=github.com/pachirode/ffmpeg-study

# Protobuf 文件存放路径
APIROOT=$(PROJ_ROOT_DIR)/pkg/api

# 编译的操作系统可以是 linux/windows/darwin
PLATFORMS ?= darwin_amd64 windows_amd64 linux_amd64 linux_arm64

# 设置一个指定的操作系统
ifeq ($(origin PLATFORM), undefined)
	ifeq ($(origin GOOS), undefined)
		GOOS := $(shell go env GOOS)
	endif
	ifeq ($(origin GOARCH), undefined)
		GOARCH := $(shell go env GOARCH)
	endif
	PLATFORM := $(GOOS)_$(GOARCH)
	# 构建镜像时，使用 linux 作为默认的 OS
	IMAGE_PLAT := linux_$(GOARCH)
else
	GOOS := $(word 1, $(subst _, ,$(PLATFORM)))
	GOARCH := $(word 2, $(subst _, ,$(PLATFORM)))
	IMAGE_PLAT := $(PLATFORM)
endif

# 设置单元测试覆盖率阈值
ifeq ($(origin COVERAGE),undefined)
COVERAGE := 1
endif

# Makefile 设置
ifndef V
MAKEFLAGS += --no-print-directory
endif

# Linux 命令设置
FIND := find . ! -path './third_party/*' ! -path './vendor/*'
XARGS := xargs --no-run-if-empty
