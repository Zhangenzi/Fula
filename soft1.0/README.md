# soft1.0 开发日志





# 智能面试系统 (Soft Interview System)

一个基于 Vue 3 + Flask 的智能面试练习平台，帮助求职者进行模拟面试训练和技能评估。

## 📋 项目概述

本项目是一个全栈的智能面试系统，包含前端用户界面和后端API服务。系统提供多种岗位的模拟面试，支持文字、语音、视频等多种交互方式，并提供详细的面试分析和历史记录管理。

## 🚀 主要功能

### ✅ 已实现功能

#### 用户认证模块
- ✅ 用户注册/登录
- ✅ 用户信息管理
- ✅ Session 会话管理

#### 面试系统核心
- ✅ 多岗位面试选择（前端、后端、数据分析等）
- ✅ 智能问题生成和管理
- ✅ 实时面试进行（计时器、进度跟踪）
- ✅ 多种回答方式支持（文字、语音、视频）
- ✅ 面试记录保存和管理

#### 数据分析模块
- ✅ 面试历史记录查看
- ✅ 成绩统计和分析
- ✅ 技能评估报告
- ✅ 数据可视化展示

#### 用户界面
- ✅ 响应式设计
- ✅ Element Plus UI 组件库
- ✅ 现代化的用户体验

### 🔄 待完善功能

#### 后端优化
- ⏳ AI 智能评分算法
- ⏳ 语音识别和分析
- ⏳ 视频面试分析
- ⏳ 更完善的数据库设计
- ⏳ Redis 缓存优化
- ⏳ JWT 认证替换 Session

#### 功能扩展
- ⏳ 实时面试官 AI 对话
- ⏳ 面试报告导出（PDF）
- ⏳ 社交功能（面试经验分享）
- ⏳ 移动端适配
- ⏳ 企业版功能

#### 系统优化
- ⏳ 单元测试覆盖
- ⏳ 性能优化
- ⏳ 错误处理完善
- ⏳ 日志系统
- ⏳ 监控和告警

## 🛠️ 技术栈

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **图表**: ECharts
- **多媒体**: vue-webcam, vue-audio-recorder

### 后端
- **框架**: Flask (Python)
- **数据库**: MySQL
- **跨域**: Flask-CORS
- **密码加密**: Werkzeug
- **数据库连接**: mysql-connector-python

## 📁 项目结构

```
soft1.0/
├── backend/                 # 后端 Flask 应用
│   ├── app.py              # 主应用文件
│   └── requirements.txt    # Python 依赖
├── src/                    # 前端源码
│   ├── views/              # 页面组件
│   │   ├── auth/           # 认证相关页面
│   │   ├── interview/      # 面试相关页面
│   │   └── user/           # 用户相关页面
│   ├── utils/              # 工具函数
│   │   └── api.ts          # API 接口定义
│   ├── stores/             # Pinia 状态管理
│   ├── router/             # 路由配置
│   └── components/         # 公共组件
├── public/                 # 静态资源
└── package.json           # 前端依赖配置
```

## 🚀 快速开始

### 环境要求

- **Node.js**: >= 18.0.0
- **Python**: >= 3.8
- **MySQL**: >= 8.0
- **Git**: 最新版本

### 1. 克隆项目

```bash
git clone https://github.com/Zhangenzi/Fula.git
cd Fula/soft1.0
```

### 2. 数据库配置

详情请见require-add.txt



#### 修改数据库配置
编辑 `backend/app.py` 中的数据库配置：
```python
db_config = {
    'host': 'localhost',
    'user': 'your_username',      # 修改为你的数据库用户名
    'password': 'your_password',  # 修改为你的数据库密码
    'database': 'interview',
    'auth_plugin': 'mysql_native_password'
}
```

### 3. 后端环境配置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
终端进入backend文件夹    运行  python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 4. 前端环境配置

```bash
# 在项目根目录 (soft1.0/)
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 5. 访问应用

打开浏览器访问 `http://localhost:5173`，即可开始使用智能面试系统。

## 📝 开发指南

### 开发环境启动

```bash
# 启动后端 (终端1)
cd backend
.venv\Scripts\activate  # Windows
python app.py

# 启动前端 (终端2)
npm run dev
```

### 代码规范

```bash
# 代码格式化
npm run format

# 代码检查
npm run lint

# 类型检查
npm run type-check
```

### 测试

```bash
# 单元测试
npm run test:unit

# E2E 测试
npm run test:e2e
```

### 构建部署

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 🤝 协作开发

### 分支管理

- `main`: 主分支，稳定版本

- `develop`: 开发分支，功能集成

- `feature/*`: 功能分支

  

### 提交规范

```bash
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 开发流程

1. 从 `develop` 分支创建功能分支
2. 完成开发并测试
3. 提交 Pull Request 到 `develop`
4. 代码审查通过后合并
5. 定期将 `develop` 合并到 `main`

## 🐛 已知问题

1. **Element Plus 图标导入问题**: 某些图标名称可能不存在，需要检查官方文档
2. **数据库连接**: 需要确保 MySQL 服务正在运行
3. **跨域问题**: 确保后端 CORS 配置正确
4. **Session 管理**: 当前使用内存存储，重启服务会丢失登录状态

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

---

**注意**: 这是一个开发中的项目，部分功能仍在完善中。欢迎贡献代码和提出建议！
        
