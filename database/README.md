# 数据库初始化说明

## 快速初始化

### 方法1: 使用MySQL命令行

```bash
mysql -u root -p < init.sql
```

### 方法2: 在MySQL中执行

```sql
mysql -u root -p
source /path/to/init.sql;
```

## 重要说明

### 默认密码问题

`init.sql` 文件中的默认密码哈希是示例值。首次部署时，你有两个选择：

#### 选项A: 更新init.sql中的密码哈希（推荐）

1. 运行密码生成脚本：
```bash
python generate_password.py
```

2. 复制生成的哈希值

3. 更新 `init.sql` 中对应的 `password_hash` 字段

#### 选项B: 初始化后通过应用注册（简单）

1. 直接运行 `init.sql`（可以注释掉或删除默认用户的INSERT语句）

2. 启动应用后，通过注册页面创建账号

3. 手动将第一个注册用户的角色改为admin：
```sql
UPDATE users SET role='admin' WHERE username='your_username';
```

## 数据库结构

### 表说明

#### users (用户表)
- `id`: 主键
- `username`: 用户名（唯一）
- `password_hash`: 密码哈希
- `role`: 角色（student/teacher/admin）
- `full_name`: 真实姓名
- `email`: 邮箱
- `created_at`: 创建时间
- `updated_at`: 更新时间

#### courses (课程表)
- `id`: 主键
- `course_name`: 课程名称
- `course_code`: 课程代码（唯一）
- `teacher_id`: 教师ID（外键）
- `description`: 课程描述
- `semester`: 学期
- `is_active`: 是否激活
- `created_at`: 创建时间
- `updated_at`: 更新时间

#### emoji_records (表情记录表)
- `id`: 主键
- `course_id`: 课程ID（外键）
- `emoji`: 表情符号
- `emoji_name`: 表情名称
- `session_date`: 日期
- `session_time`: 时间
- `comment`: 备注
- `created_at`: 创建时间
- **注意**: 此表不包含user_id，以保证匿名性

#### user_courses (选课关联表)
- `id`: 主键
- `user_id`: 用户ID（外键）
- `course_id`: 课程ID（外键）
- `enrolled_at`: 选课时间

#### user_emoji_records (用户表情记录关联表)
- `id`: 主键
- `user_id`: 用户ID（外键）
- `emoji_record_id`: 表情记录ID（外键）
- **用途**: 允许用户查看自己的历史记录，但不暴露给教师/管理员

## 数据库维护

### 清空所有数据（保留结构）

```sql
USE emoji_checker_db;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE user_emoji_records;
TRUNCATE TABLE emoji_records;
TRUNCATE TABLE user_courses;
TRUNCATE TABLE courses;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;
```

### 完全重置数据库

```sql
DROP DATABASE IF EXISTS emoji_checker_db;
```

然后重新执行 `init.sql`。

## 安全建议

1. **修改默认密码**: 首次部署后立即修改所有默认账号密码
2. **创建专用用户**: 不要使用root用户运行应用
```sql
CREATE USER 'emoji_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON emoji_checker_db.* TO 'emoji_user'@'localhost';
FLUSH PRIVILEGES;
```
3. **备份数据**: 定期备份数据库
```bash
mysqldump -u root -p emoji_checker_db > backup_$(date +%Y%m%d).sql
```

## 故障排除

### 字符编码问题

如果遇到表情符号无法保存：

```sql
ALTER DATABASE emoji_checker_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE emoji_records CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 外键约束错误

如果删除数据时遇到外键约束：

```sql
SET FOREIGN_KEY_CHECKS = 0;
-- 执行删除操作
SET FOREIGN_KEY_CHECKS = 1;
```

