# 表情符号检查器 - 快速启动指南

## 🚀 10分钟快速部署

本指南将帮助你在10分钟内完成本地部署。

### 前提条件检查

在开始之前，请确保已安装：

- ✅ Python 3.8+ 
- ✅ MySQL 5.7+
- ✅ 浏览器（Chrome、Firefox等）

### 第一步：安装Python（如果尚未安装）

#### Windows用户：
1. 访问 https://www.python.org/downloads/
2. 下载并运行安装程序
3. **重要**: 勾选 "Add Python to PATH"
4. 验证安装：
```bash
python --version
```

#### Linux用户：
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 第二步：安装MySQL

#### Windows用户：

1. 下载 MySQL Community Server: https://dev.mysql.com/downloads/mysql/
2. 运行安装程序
3. **记住你设置的root密码**
4. 确保MySQL服务已启动：
   - 按 `Win + R`
   - 输入 `services.msc`
   - 找到 MySQL80（或类似名称）
   - 确保状态为"正在运行"

#### Linux用户：
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### 第三步：获取项目代码

```bash
# 进入你的工作目录
cd C:\Users\YourName\Documents  # Windows示例
# cd ~/projects  # Linux示例

# 如果使用Git
git clone <repository-url>
cd emoji_project_team

# 或者直接解压下载的项目文件到目录
```

### 第四步：设置Python虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows (PowerShell):
venv\Scripts\activate
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 看到 (venv) 前缀表示成功
```

### 第五步：安装依赖包

```bash
pip install -r requirements.txt
```

**如果遇到 mysqlclient 安装失败（Windows常见）：**

方法1 - 使用预编译包：
```bash
# 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
# 下载对应版本的.whl文件，例如：
# mysqlclient-2.2.0-cp311-cp311-win_amd64.whl (Python 3.11, 64位)
pip install mysqlclient-2.2.0-cp311-cp311-win_amd64.whl
```

方法2 - 使用PyMySQL替代：
```bash
pip install PyMySQL
```
然后在 `app.py` 最顶部添加：
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 第六步：初始化数据库

#### 步骤6.1: 登录MySQL

```bash
mysql -u root -p
# 输入你设置的MySQL密码
```

#### 步骤6.2: 创建数据库和表

在MySQL命令行中执行：

```sql
-- 创建数据库
CREATE DATABASE emoji_checker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE emoji_checker_db;

-- 退出MySQL
exit;
```

#### 步骤6.3: 导入表结构和数据

返回命令行，执行：

```bash
mysql -u root -p emoji_checker_db < database/init.sql
```

或者在MySQL中执行：
```sql
mysql -u root -p
USE emoji_checker_db;
source C:/path/to/emoji_project_team/database/init.sql;  # Windows路径
```

#### 步骤6.4: 验证数据库

```bash
mysql -u root -p emoji_checker_db
```

```sql
-- 查看所有表
SHOW TABLES;

-- 查看用户数据
SELECT id, username, role FROM users;

-- 应该看到4个用户：admin, teacher1, student1, student2
-- 退出
exit;
```

### 第七步：配置应用

编辑 `config.py` 文件，修改数据库密码：

```python
# 找到这一行：
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'your_password'

# 将 'your_password' 改为你的MySQL root密码
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '你的MySQL密码'
```

### 第八步：启动应用

```bash
python app.py
```

你应该看到类似输出：
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

### 第九步：访问应用

打开浏览器，访问：
```
http://localhost:5000
```

### 第十步：登录测试

使用默认账号登录：

**学生账号测试：**
- 用户名: `student1`
- 密码: `student123`

**教师账号测试：**
- 用户名: `teacher1`
- 密码: `teacher123`

**管理员账号测试：**
- 用户名: `admin`
- 密码: `admin123`

## ✅ 功能测试清单

### 学生端测试

1. ✅ 使用 student1 登录
2. ✅ 查看"我的课程"（应该有2门课）
3. ✅ 点击"选课"查看所有课程
4. ✅ 点击"发送表情"
   - 选择一门课程
   - 选择一个表情（如😊）
   - 添加备注（可选）
   - 提交
5. ✅ 点击"历史记录"查看刚才提交的反馈
6. ✅ 点击"修改密码"测试密码修改功能

### 教师/管理员测试

1. ✅ 退出学生账号
2. ✅ 使用 admin 登录
3. ✅ 查看仪表盘统计
4. ✅ 点击"用户管理"查看所有用户
5. ✅ 点击"课程管理"查看课程列表
6. ✅ 点击"表情数据"查看学生反馈（注意：匿名显示）
7. ✅ 点击"统计分析"查看图表
8. ✅ 点击"导出数据"下载Excel文件

## 🐛 常见问题快速解决

### 问题1: pip install 很慢

**解决方案**: 使用国内镜像
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 问题2: MySQL连接被拒绝

**解决方案**:
1. 确保MySQL服务正在运行
2. 检查config.py中的密码是否正确
3. 尝试在命令行连接：`mysql -u root -p`

### 问题3: 端口5000被占用

**解决方案**: 修改 `app.py` 最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为5001或其他端口
```

### 问题4: 页面显示乱码

**解决方案**: 确保数据库使用UTF8MB4编码
```sql
ALTER DATABASE emoji_checker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 问题5: 默认密码无法登录

**原因**: init.sql中的密码哈希可能不匹配

**解决方案A**: 重新生成密码哈希
```bash
cd database
python generate_password.py
# 复制生成的哈希值，更新init.sql
```

**解决方案B**: 使用注册功能创建新账号
1. 访问 http://localhost:5000/register
2. 注册一个新账号
3. 在MySQL中修改角色：
```sql
UPDATE users SET role='admin' WHERE username='your_new_username';
```

### 问题6: 虚拟环境激活失败（Windows PowerShell）

**解决方案**: 修改执行策略
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 然后重新激活虚拟环境
venv\Scripts\activate
```

## 📱 使用提示

### 最佳实践

1. **学生使用建议**：
   - 每次课后及时提交情绪反馈
   - 添加具体的备注说明
   - 定期查看历史记录

2. **教师使用建议**：
   - 每天查看学生反馈
   - 关注负面情绪（😢😡😕）的比例
   - 定期导出数据进行分析

3. **系统维护建议**：
   - 定期备份数据库
   - 修改所有默认密码
   - 监控系统性能

### 安全提醒

⚠️ **首次部署后必做**：
1. 修改所有默认账号密码
2. 修改 config.py 中的 SECRET_KEY
3. 生产环境关闭 DEBUG 模式

## 🎓 学习资源

- Flask官方文档: https://flask.palletsprojects.com/
- MySQL官方文档: https://dev.mysql.com/doc/
- Python官方教程: https://docs.python.org/zh-cn/3/

## 💡 下一步

系统部署成功后，你可以：

1. 📖 阅读 [DEPLOYMENT.md](DEPLOYMENT.md) 了解详细配置
2. 🔧 阅读 [database/README.md](database/README.md) 了解数据库管理
3. 🚀 尝试添加新功能或定制界面
4. 📊 分析学生反馈数据，优化教学

## 🆘 获取帮助

如果遇到无法解决的问题：

1. 查看错误信息和日志
2. 检查 [DEPLOYMENT.md](DEPLOYMENT.md) 的故障排除部分
3. 在GitHub上提交Issue
4. 发送邮件寻求帮助

---

**祝你使用愉快！ 🎉**

