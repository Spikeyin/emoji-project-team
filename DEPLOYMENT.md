# 表情符号检查器 - 部署指南

## 项目简介

表情符号检查器是一个基于 Flask + MySQL 的学生情绪反馈系统，允许教师实时监控学生在课程中的情绪反应。

## 系统要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+
- Windows/Linux/MacOS

## 本地部署步骤

### 1. 安装 Python

确保已安装 Python 3.8 或更高版本：

```bash
python --version
```

如果未安装，请访问 [Python官网](https://www.python.org/downloads/) 下载安装。

### 2. 安装 MySQL

#### Windows:
1. 下载 MySQL Community Server: https://dev.mysql.com/downloads/mysql/
2. 运行安装程序，记住设置的 root 密码
3. 确保 MySQL 服务已启动

#### 检查 MySQL 服务状态:
```bash
# Windows (PowerShell管理员模式)
Get-Service MySQL*

# 如果未启动，执行：
Start-Service MySQL80  # 或你的MySQL服务名
```

### 3. 克隆/下载项目

如果使用 Git：
```bash
git clone <repository-url>
cd emoji_project_team
```

或直接下载项目文件到本地目录。

### 4. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 5. 安装依赖包

```bash
pip install -r requirements.txt
```

**注意**: 如果在 Windows 上安装 `mysqlclient` 遇到问题，可以：

方法1: 下载预编译的 wheel 文件
```bash
# 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
# 下载对应Python版本的 .whl 文件
pip install mysqlclient-*.whl
```

方法2: 使用 PyMySQL 替代
```bash
pip uninstall mysqlclient
pip install PyMySQL
```

然后在 `app.py` 顶部添加：
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 6. 配置数据库

#### 6.1 登录 MySQL

```bash
mysql -u root -p
# 输入你的 MySQL root 密码
```

#### 6.2 执行初始化脚本

```sql
-- 在 MySQL 命令行中执行：
source database/init.sql;
```

或者直接导入：
```bash
mysql -u root -p < database/init.sql
```

#### 6.3 验证数据库创建

```sql
USE emoji_checker_db;
SHOW TABLES;
SELECT * FROM users;
```

### 7. 配置应用

修改 `config.py` 中的数据库连接信息：

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_mysql_password'  # 修改为你的MySQL密码
MYSQL_DB = 'emoji_checker_db'
```

### 8. 运行应用

```bash
python app.py
```

如果一切正常，你会看到：
```
 * Running on http://0.0.0.0:5000
```

### 9. 访问应用

打开浏览器访问：
```
http://localhost:5000
```

## 默认账号

### 管理员账号
- 用户名: `admin`
- 密码: `admin123`

### 教师账号
- 用户名: `teacher1`
- 密码: `teacher123`

### 学生账号
- 用户名: `student1`
- 密码: `student123`
- 用户名: `student2`
- 密码: `student123`

## 常见问题解决

### 问题1: ModuleNotFoundError: No module named 'MySQLdb'

**解决方案**:
```bash
pip install mysqlclient
# 或
pip install PyMySQL
```

### 问题2: Access denied for user 'root'@'localhost'

**解决方案**: 
1. 检查 MySQL 密码是否正确
2. 修改 `config.py` 中的 `MYSQL_PASSWORD`

### 问题3: Can't connect to MySQL server

**解决方案**:
1. 确保 MySQL 服务已启动
2. 检查端口 3306 是否开放
```bash
netstat -an | findstr 3306
```

### 问题4: 密码加密问题

数据库初始化脚本中的密码哈希需要重新生成：

```python
from werkzeug.security import generate_password_hash

# 生成新的密码哈希
password = "admin123"
hash_value = generate_password_hash(password)
print(hash_value)
```

然后更新 `database/init.sql` 中的 `password_hash` 字段。

### 问题5: 端口 5000 已被占用

**解决方案**: 修改 `app.py` 中的端口：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为其他端口
```

## 功能测试清单

### 学生端功能
- [ ] 注册新学生账号
- [ ] 学生登录
- [ ] 查看可选课程
- [ ] 选择课程
- [ ] 发送表情反馈
- [ ] 查看历史反馈记录
- [ ] 修改密码

### 教师/管理员功能
- [ ] 教师/管理员登录
- [ ] 查看课程列表
- [ ] 查看表情数据（匿名）
- [ ] 统计分析（图表）
- [ ] 导出数据（Excel）
- [ ] 查看用户列表（仅管理员）
- [ ] 修改密码

## 数据匿名性验证

确保系统符合匿名性要求：

1. 在 `emoji_records` 表中不应有 `user_id` 字段
2. 教师查看表情数据时，无法追踪到具体学生
3. 学生只能查看自己的历史记录

## 项目结构

```
emoji_project_team/
├── app.py                  # 主应用入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖包列表
├── models/                 # 数据模型
│   ├── user.py
│   ├── course.py
│   └── emoji_record.py
├── routes/                 # 路由控制器
│   ├── auth.py            # 认证路由
│   ├── student.py         # 学生路由
│   └── admin.py           # 管理员路由
├── templates/             # HTML模板
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student/          # 学生页面
│   └── admin/            # 管理员页面
├── static/               # 静态资源
│   ├── css/
│   └── js/
└── database/             # 数据库脚本
    └── init.sql
```

## 生产环境部署（可选）

### 使用 Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Nginx 反向代理

配置 Nginx：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 安全建议

1. **修改默认密码**: 首次部署后立即修改所有默认账号密码
2. **SECRET_KEY**: 在生产环境中使用随机生成的密钥
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
3. **关闭 Debug 模式**: 生产环境中设置 `debug=False`
4. **使用 HTTPS**: 在生产环境中启用 SSL/TLS
5. **数据库权限**: 创建专用数据库用户，不使用 root

## 技术支持

如有问题，请检查：
1. Python 和 MySQL 版本是否符合要求
2. 所有依赖包是否正确安装
3. 数据库连接配置是否正确
4. 防火墙是否阻止了端口访问

## 许可证

本项目仅供教学和学习使用。

