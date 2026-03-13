# AI Creator Vault

一个服务于 AI 创作者的资产管理平台，帮助你安全地存储、组织和检索 AI 生成的图片、提示词等创作资产。通过知识图谱技术，可视化探索资产之间的关系，追踪创作演化路径。

## 功能特点

### 核心功能
- **提示词管理**：存储和管理 AI 创作提示词，支持评分和关联图片
- **图片管理**：上传和管理 AI 生成的图片，支持评分和关联提示词
- **主题管理**：围绕主题组织参考图片，支持拖拽上传和灵活分类

### 智能搜索
- **AI 图片分析**：自动分析图片内容并生成描述和嵌入向量
- **向量搜索**：支持基于语义相似度的文本搜图和以图搜图
- **语义检索**：通过自然语言描述找到最相关的图片

### 知识图谱 🌟
- **可视化图谱**：交互式图形界面展示资产及其关系
- **关系追踪**：追踪提示词、图片、衍生版本之间的关系链
- **路径发现**：查找资产间的最短关联路径
- **衍生管理**：支持编辑、变体、放大、裁剪等多种衍生类型
- **图谱遍历**：广度优先搜索邻居节点，发现创作网络

## 技术栈

- **后端**：Node.js + Express.js + Sequelize
- **数据库**：SQLite（默认）/ PostgreSQL（推荐生产环境）
- **前端**：React + Vite
- **AI 服务**：Python + FastAPI + OpenAI API

## 数据库支持

项目支持两种数据库：

| 数据库 | 适用场景 | 向量支持 |
|--------|----------|----------|
| SQLite | 开发、测试、小型部署 | JSON 存储 |
| PostgreSQL | 生产环境、大数据量 | pgvector 原生向量类型 |

### 配置方式

在 `backend/.env` 文件中设置：

```env
# 数据库类型：sqlite 或 postgres
DB_TYPE=sqlite

# SQLite 配置
DB_STORAGE=./database.db

# PostgreSQL 配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aigc_assistant
DB_USER=postgres
DB_PASSWORD=your_password
```

## 安装步骤

### 1. 克隆项目

```bash
git clone git@github.com:legendPerceptor/aicreatorvault.git
cd aicreatorvault
```

### 2. 安装依赖

```bash
npm install
cd frontend
npm install
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env
# 编辑 backend/.env 配置数据库

# 配置 AI 服务
cp image-service/.env.example image-service/.env
# 编辑 image-service/.env 配置 OpenAI API Key
```

### 4. PostgreSQL 设置（可选）

如果使用 PostgreSQL：

```bash
# 安装 PostgreSQL 和 pgvector
sudo apt install postgresql postgresql-16-pgvector

# 创建数据库和用户
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "CREATE DATABASE aigc_assistant OWNER postgres;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aigc_assistant TO postgres;"

# 启用 pgvector 扩展
PGPASSWORD='your_password' psql -h localhost -U postgres -d aigc_assistant -c "CREATE EXTENSION vector;"
```

### 5. 启动服务

```bash
# 启动所有服务
npm run dev:full

# 或分别启动
npm run start:backend    # 后端服务 (端口 3001)
npm run start:frontend   # 前端服务 (端口 5173)
npm run start:image-service  # AI 服务 (端口 8001)
```

### 6. 访问应用

- 前端：http://localhost:5173/
- 后端 API：http://localhost:3001/api
- AI 服务：http://localhost:8001/

## 项目结构

```
aigc-assistant/
├── backend/
│   ├── config/
│   │   └── database.js          # 数据库配置工厂
│   ├── models/
│   │   ├── index.js             # 数据库连接和模型导出
│   │   ├── Prompt.js            # 提示词模型
│   │   ├── Image.js             # 图片模型（含向量字段）
│   │   ├── Theme.js             # 主题模型
│   │   ├── ThemeImage.js        # 主题-图片关联模型
│   │   ├── Asset.js             # 统一资产模型（知识图谱）
│   │   └── AssetRelationship.js # 资产关系模型（知识图谱）
│   ├── routes/
│   │   ├── prompts.js           # 提示词 API
│   │   ├── images.js            # 图片 API
│   │   ├── themes.js            # 主题 API
│   │   ├── assets.js            # 资产管理 API（含衍生版本）
│   │   └── graph.js             # 知识图谱 API
│   ├── services/
│   │   ├── imageServiceClient.js # AI 服务客户端
│   │   └── graphService.js      # 图谱遍历服务
│   ├── utils/
│   │   └── vectorSearch.js      # 向量搜索工具
│   ├── migrations/              # 数据库迁移脚本
│   │   └── migrateToAssets.js   # 迁移到知识图谱
│   ├── uploads/                 # 上传的图片
│   ├── .env                     # 环境变量配置
│   ├── .env.example             # 环境变量模板
│   ├── server.js                # 后端服务器
│   └── database.db              # SQLite 数据库（默认）
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StarRating.jsx   # 评分组件
│   │   │   ├── ImageCard.jsx    # 图片卡片
│   │   │   ├── ImagePreviewModal.jsx  # 图片预览
│   │   │   └── graph/           # 知识图谱组件
│   │   │       ├── GraphCanvas.jsx    # 图谱画布
│   │   │       ├── GraphControls.jsx  # 图谱控制面板
│   │   │       └── GraphNodeDetails.jsx # 节点详情
│   │   ├── pages/
│   │   │   ├── PromptsPage.jsx       # 提示词管理
│   │   │   ├── ImagesPage.jsx        # 图片管理
│   │   │   ├── SearchPage.jsx        # 搜索页面
│   │   │   ├── ThemesPage.jsx        # 主题管理
│   │   │   └── KnowledgeGraphPage.jsx # 知识图谱
│   │   ├── hooks/
│   │   │   ├── usePrompts.js         # 提示词数据钩子
│   │   │   ├── useImages.js          # 图片数据钩子
│   │   │   ├── useThemes.js          # 主题数据钩子
│   │   │   ├── useAssets.js          # 资产数据钩子
│   │   │   └── useGraph.js           # 图谱数据钩子
│   │   ├── App.jsx              # 主应用组件
│   │   ├── main.jsx             # 入口文件
│   │   └── index.css            # 样式文件
│   └── public/                  # 前端静态文件
├── image-service/
│   ├── main.py                  # AI 服务入口
│   ├── image_processor.py       # 图片处理和嵌入生成
│   ├── requirements.txt         # Python 依赖
│   ├── .env                     # AI 服务环境变量
│   └── .env.example             # 环境变量模板
├── stop.sh                      # 停止服务脚本
├── package.json                 # 项目配置
├── CLAUDE.md                    # Claude Code 项目指南
├── KNOWLEDGE_GRAPH.md           # 知识图谱详细文档
├── developers.md                # 开发者指南
└── README.md                    # 项目说明
```

## API 端点

### 提示词 API

- `GET /api/prompts` - 获取所有提示词
- `GET /api/prompts/unused` - 获取未使用的提示词
- `POST /api/prompts` - 创建新提示词
- `PUT /api/prompts/:id/score` - 更新提示词评分
- `DELETE /api/prompts/:id` - 删除提示词

### 图片 API

- `GET /api/images` - 获取所有图片
- `POST /api/images` - 上传图片（自动分析）
- `POST /api/images/:id/analyze` - 分析图片
- `POST /api/images/batch-analyze` - 批量分析图片
- `PUT /api/images/:id/score` - 更新图片评分
- `PUT /api/images/:id/prompt` - 更新图片关联的提示词
- `DELETE /api/images/:id` - 删除图片
- `POST /api/images/search` - 文本搜索图片
- `POST /api/images/search-by-image` - 以图搜图

### 主题 API

- `GET /api/themes` - 获取所有主题
- `POST /api/themes` - 创建新主题
- `POST /api/themes/:id/images` - 为主题添加图片
- `DELETE /api/themes/:id/images/:imageId` - 从主题中移除图片

### 资产管理 API（知识图谱）

- `GET /api/assets` - 获取所有资产
- `GET /api/assets/:id` - 获取单个资产详情
- `POST /api/assets` - 创建新资产
- `POST /api/assets/:id/derived` - 创建衍生版本（编辑/变体/放大/裁剪）
- `PUT /api/assets/:id` - 更新资产信息
- `DELETE /api/assets/:id` - 删除资产
- `GET /api/assets/:id/versions` - 获取资产的所有衍生版本

### 知识图谱 API

- `GET /api/graph/nodes` - 获取图谱所有节点
- `GET /api/graph/edges` - 获取图谱所有边
- `GET /api/graph/neighbors/:id` - 获取节点的邻居
- `GET /api/graph/path/:fromId/:toId` - 查找两节点间最短路径
- `GET /api/graph/traverse/:id` - 广度优先遍历图谱
- `GET /api/graph/components` - 获取连通组件
- `POST /api/graph/relationship` - 创建资产关系
- `DELETE /api/graph/relationship/:id` - 删除资产关系

## 开发指南

### 代码规范

项目使用 Prettier 进行代码格式化，并通过 Husky 在提交前自动格式化代码。

```bash
# 手动格式化代码
npx prettier --write "**/*.js"
```

### 停止服务

```bash
./stop.sh
```

### 架构说明

- **组件化设计**：将 UI 拆分为可复用的组件（StarRating、ImageCard、GraphCanvas）
- **页面分离**：每个功能模块独立为页面组件
- **状态管理**：使用自定义 Hooks 封装数据获取和状态逻辑
- **单一职责**：每个文件只负责一个功能，便于维护和测试
- **数据库抽象**：通过 Sequelize ORM 支持多种数据库
- **向量搜索**：PostgreSQL 使用 pgvector，SQLite 使用 JSON 回退
- **统一资产模型**：提示词、图片、衍生图片统一为 Asset，便于关系管理
- **图谱服务**：独立的图遍历服务，支持 BFS、最短路径等算法
- **关系追踪**：记录资产间的生成、衍生、版本、灵感等关系类型

## 知识图谱

AI Creator Vault 引入了知识图谱功能，将所有创作资产（提示词、图片、衍生版本）统一管理，并追踪它们之间的关系。

### 核心概念

- **资产类型**：
  - `prompt` - AI 创作提示词
  - `image` - AI 生成的原始图片
  - `derived_image` - 衍生图片（编辑、变体、放大、裁剪）

- **关系类型**：
  - `generated` - 提示词生成图片
  - `derived_from` - 从原始资产衍生
  - `version_of` - 版本关系
  - `inspired_by` - 灵感来源

- **衍生类型**：
  - `edit` - 编辑修改
  - `variant` - 风格变体
  - `upscale` - 放大增强
  - `crop` - 裁剪

### 数据迁移

如果你已经在使用旧版本的提示词和图片管理，可以运行迁移脚本将数据导入知识图谱：

```bash
node backend/migrations/migrateToAssets.js
```

### 详细文档

查看 [KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md) 了解知识图谱的详细使用方法和 API 示例。

## 开发者指南

更多开发相关的信息，包括测试方法和数据库查询命令，请查看 [开发者指南](developers.md)。
