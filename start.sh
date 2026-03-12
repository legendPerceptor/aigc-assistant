#!/bin/bash

echo "🚀 启动 AIGC Assistant 完整服务..."
echo ""

# 检查 .env 文件
if [ ! -f "image-service/.env" ]; then
    echo "⚠️  未找到 image-service/.env 文件"
    echo "📝 正在从 .env.example 创建 .env 文件..."
    cp image-service/.env.example image-service/.env
    echo "✅ 已创建 image-service/.env"
    echo "⚠️  请编辑 image-service/.env 并填入你的 OPENAI_API_KEY"
    echo ""
fi

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ uv 未安装"
    echo "📦 请运行以下命令安装 uv:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "📦 安装 Python 依赖..."
cd image-service
uv sync
cd ..

echo "📦 安装 Node.js 依赖..."
npm install

echo ""
echo "🔄 启动所有服务..."
echo "   - Node.js Backend: http://localhost:3001"
echo "   - React Frontend: http://localhost:5173"
echo "   - Python Image Service: http://localhost:8001"
echo ""

npm run dev:full
