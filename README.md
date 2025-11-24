# 表情符号检查器系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)](https://www.mysql.com/)

## 📊 项目简介

表情符号检查器是一个学生情绪反馈系统，允许教师在课程期间实时监控学生的情绪反应。学生通过选择表情符号来表达对课程内容的感受，帮助教师了解教学效果并及时调整教学策略。

## ✨ 核心功能

### 学生端
- ✅ 用户注册与登录
- ✅ 课程浏览与选课
- ✅ 表情反馈提交
- ✅ 历史记录查看
- ✅ 密码修改

### 教师/管理员端
- ✅ 用户管理（管理员）
- ✅ 课程管理
- ✅ 表情数据查看（匿名）
- ✅ 统计分析与可视化
- ✅ 数据导出（Excel）
- ✅ 密码修改

## 🔒 安全特性

- **数据匿名性**: 表情评价完全匿名，教师无法追踪到具体学生
- **访问控制**: 基于角色的权限管理（学生/教师/管理员）
- **密码加密**: 使用 Werkzeug 进行密码哈希加密
- **防越权**: 学生只能评价已选课程，只能查看自己的历史记录

## 🛠️ 技术栈

- **后端框架**: Flask 2.3+
- **数据库**: MySQL 5.7+
- **认证**: Flask-Login
- **前端**: HTML5, CSS3, JavaScript
- **图表**: Chart.js
- **架构模式**: MVC（Model-View-Controller）

## 📦 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- pip（Python包管理器）

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd emoji_project_team

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
mysql -u root -p < database/init.sql

# 5. 配置数据库连接
# 编辑 config.py，修改 MYSQL_PASSWORD 为你的MySQL密码

# 6. 运行应用
python app.py
```

### 3. 访问应用

打开浏览器访问: `http://localhost:5000`


**⚠️ 重要**: 首次部署后请立即修改所有默认密码！

## 📁 项目结构

```
emoji_project_team/
├── app.py                    # Flask应用主入口
├── config.py                 # 配置文件
├── requirements.txt          # Python依赖包
├── models/                   # 数据模型层
│   ├── user.py              # 用户模型
│   ├── course.py            # 课程模型
│   └── emoji_record.py      # 表情记录模型
├── routes/                   # 路由控制器层
│   ├── auth.py              # 认证路由
│   ├── student.py           # 学生路由
│   └── admin.py             # 管理员路由
├── templates/                # 视图模板层
│   ├── base.html            # 基础模板
│   ├── student/             # 学生页面
│   └── admin/               # 管理员页面
├── static/                   # 静态资源
│   ├── css/style.css        # 样式文件
│   └── js/main.js           # JavaScript脚本
└── database/                 # 数据库脚本
    └── init.sql             # 初始化SQL
```

## 🎯 使用场景

1. **课堂实时反馈**: 学生在课程中随时提交情绪反馈
2. **教学效果评估**: 教师通过统计分析了解教学效果
3. **课程改进**: 基于学生情绪数据优化课程内容
4. **学生关怀**: 及时发现学生学习困难并提供帮助

## 📊 表情符号说明

| 表情 | 含义 | 说明                     |
| ---- | ---- | ------------------------ |
| 😊    | 开心 | 对课程内容满意，理解良好 |
| 😃    | 兴奋 | 对课程内容非常感兴趣     |
| 😐    | 一般 | 感觉一般，没有特别的反应 |
| 🤔    | 思考 | 内容有难度，需要思考     |
| 😕    | 困惑 | 对内容感到困惑           |
| 😢    | 难过 | 学习遇到困难             |
| 😡    | 生气 | 对课程不满意             |
| 😴    | 困倦 | 感到疲倦或无聊           |

## 🔧 配置说明

### 数据库配置（config.py）

```python
MYSQL_HOST = 'localhost'       # 数据库主机
MYSQL_USER = 'root'            # 数据库用户
MYSQL_PASSWORD = 'your_password'  # 数据库密码
MYSQL_DB = 'emoji_checker_db'  # 数据库名
```

### 应用配置

```python
SECRET_KEY = 'your-secret-key'  # 会话密钥
DEBUG = True                     # 调试模式（生产环境设为False）
```

## 🐛 常见问题

详细的问题解决方案请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

### MySQL连接失败
- 检查MySQL服务是否启动
- 验证config.py中的密码是否正确

### 依赖包安装失败
- Windows用户安装mysqlclient可能需要预编译包
- 可使用PyMySQL作为替代方案

### 端口被占用
- 修改app.py中的端口号（默认5000）

## 📈 数据库设计

### 核心表结构

- **users**: 用户信息表
- **courses**: 课程信息表
- **emoji_records**: 表情记录表（匿名）
- **user_courses**: 用户选课关联表
- **user_emoji_records**: 用户表情记录关联表

## 🤝 贡献指南

欢迎提交Issue和Pull Request！


## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
