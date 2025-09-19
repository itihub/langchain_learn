# 使用 bash 作为其 shell
SHELL := /bin/bash

# --- 变量定义 ---
VENV_DIR = .venv
REQUIREMENTS_FILE = requirements.txt
REQUIREMENTS_DEV_FILE = requirements-dev.txt
ENV_FILE := .env
ENV_EXAMPLE_FILE := .env.example

# 特殊声明，用于告诉 make，all 和 setup 是伪目标（phony targets）
.PHONY: all setup create_venv install_deps install_dev_deps clean

# 默认的 make 命令，会执行 all 目标，而 all 目标又会去执行 setup 目标
all: setup

# setup 任务: 创建虚拟环境，安装依赖
setup: create_venv install_deps

# 创建 Python 虚拟环境
create_venv:
	@echo "--- Creating virtual environment..."
	python -m venv $(VENV_DIR)

# 安装依赖
install_deps:
	@echo "--- Activating virtual environment and installing dependencies..."
	@# 检查 requirements.txt 文件是否存在
	@if [ ! -f "$(REQUIREMENTS_FILE)" ]; then \
	  echo "Warning: $(REQUIREMENTS_FILE) not found, skipping dependency installation."; \
	  exit 0; \
	fi
	@# 激活虚拟环境并安装依赖
	@# 注意: 此处使用不同的激活命令以兼容不同系统
	@# Windows
	@if [ "$(OS)" == "Windows_NT" ]; then \
	  ./$(VENV_DIR)/Scripts/activate && \
	  python -m pip install --upgrade pip && \
	  python -m pip install -r $(REQUIREMENTS_FILE); \
	else \
	  # Linux and macOS \
	  source $(VENV_DIR)/bin/activate && \
	  python -m pip install --upgrade pip && \
	  python -m pip install -r $(REQUIREMENTS_FILE); \
	fi

# 安装开发依赖
install_dev_deps:
	@echo "--- Installing development dependencies..."
	@if [ ! -f "$(REQUIREMENTS_DEV_FILE)" ]; then \
	  echo "Warning: $(REQUIREMENTS_DEV_FILE) not found, skipping dev dependency installation."; \
	  exit 0; \
	fi
	@if [ "$(OS)" == "Windows_NT" ]; then \
	  ./$(VENV_DIR)/Scripts/activate && \
	  python -m pip install -r $(REQUIREMENTS_DEV_FILE); \
	else \
	  source $(VENV_DIR)/bin/activate && \
	  python -m pip install -r $(REQUIREMENTS_DEV_FILE); \
	fi

# 清理任务: 删除虚拟环境
clean:
	@echo "--- Cleaning up virtual environment..."
	@if [ -d "$(VENV_DIR)" ]; then \
	  rm -rf "$(VENV_DIR)"; \
	fi
	@echo "--- Virtual environment removed."

# sensitive: 将所有键的 value 进行脱敏并生成 .env.example
sensitive:
	@echo "正在脱敏并生成 $(ENV_EXAMPLE_FILE)..."
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(ENV_FILE) 文件不存在，无法生成 $(ENV_EXAMPLE_FILE)。" >&2; \
		exit 1; \
	fi
	@sed -E '/^#/!s/^(.*=).*/\1.../' $(ENV_FILE) > $(ENV_EXAMPLE_FILE)
	@echo "✅ 完成：$(ENV_EXAMPLE_FILE) 已生成。"

# copy-env: 复制 .env.example 为 .env 文件
copy-env:
	@echo "正在复制 $(ENV_EXAMPLE_FILE) 为 $(ENV_FILE)..."
	@if [ ! -f $(ENV_EXAMPLE_FILE) ]; then \
		echo "$(ENV_EXAMPLE_FILE) 文件不存在，无法复制。" >&2; \
		exit 1; \
	fi
	@cp $(ENV_EXAMPLE_FILE) $(ENV_FILE)
	@echo "✅ 完成：$(ENV_FILE) 已生成。"