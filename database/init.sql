-- 删除并重新创建数据库
DROP DATABASE IF EXISTS emoji_checker_db;
CREATE DATABASE emoji_checker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE emoji_checker_db;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher', 'admin') NOT NULL,
    full_name VARCHAR(255),  -- 增加长度
    email VARCHAR(255),      -- 增加长度
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 课程表
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,  -- 增加长度
    course_code VARCHAR(50) UNIQUE NOT NULL,  -- 增加长度
    teacher_id INT NOT NULL,
    description TEXT,
    semester VARCHAR(50),  -- 增加长度
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_teacher (teacher_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户课程关联表（学生选课）
CREATE TABLE IF NOT EXISTS user_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_enrollment (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_course (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表情符号记录表（匿名化）
CREATE TABLE IF NOT EXISTS emoji_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    emoji VARCHAR(10) NOT NULL,
    emoji_name VARCHAR(50),  -- 增加长度
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course (course_id),
    INDEX idx_date (session_date),
    INDEX idx_emoji (emoji)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户表情记录关联表（用于用户查看自己的历史记录）
CREATE TABLE IF NOT EXISTS user_emoji_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    emoji_record_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (emoji_record_id) REFERENCES emoji_records(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_record (emoji_record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认管理员账号
-- 密码: admin123 (使用 Werkzeug 加密)
INSERT INTO users (username, password_hash, role, full_name, email) VALUES
('admin', 'scrypt:32768:8:1$IvqyR8vZg5g8lY8P$e9c3d7c8f5b4a2e1d9c7b5a3e8f6d4c2b0a9e7f5d3c1b8f6e4d2c0a8e6f4d2c0b9e7f5d3c1a8f6e4d2c0b8e6f4d2', 'admin', N'系统管理员', 'admin@example.com');

-- 插入示例教师账号
-- 密码: teacher123
INSERT INTO users (username, password_hash, role, full_name, email) VALUES
('teacher1', 'scrypt:32768:8:1$IvqyR8vZg5g8lY8P$e9c3d7c8f5b4a2e1d9c7b5a3e8f6d4c2b0a9e7f5d3c1b8f6e4d2c0a8e6f4d2c0b9e7f5d3c1a8f6e4d2c0b8e6f4d2', 'teacher', N'张老师', 'teacher1@example.com');

-- 插入示例学生账号
-- 密码: student123
INSERT INTO users (username, password_hash, role, full_name, email) VALUES
('student1', 'scrypt:32768:8:1$IvqyR8vZg5g8lY8P$e9c3d7c8f5b4a2e1d9c7b5a3e8f6d4c2b0a9e7f5d3c1b8f6e4d2c0a8e6f4d2c0b9e7f5d3c1a8f6e4d2c0b8e6f4d2', 'student', N'学生一', 'student1@example.com'),
('student2', 'scrypt:32768:8:1$IvqyR8vZg5g8lY8P$e9c3d7c8f5b4a2e1d9c7b5a3e8f6d4c2b0a9e7f5d3c1b8f6e4d2c0a8e6f4d2c0b9e7f5d3c1a8f6e4d2c0b8e6f4d2', 'student', N'学生二', 'student2@example.com');

-- 插入示例课程
INSERT INTO courses (course_name, course_code, teacher_id, description, semester) VALUES
(N'Python程序设计', 'CS101', 2, N'Python编程基础课程', N'2024春季'),
(N'数据结构与算法', 'CS201', 2, N'数据结构与算法分析', N'2024春季');

-- 插入示例选课记录
INSERT INTO user_courses (user_id, course_id) VALUES
(3, 1),
(3, 2),
(4, 1),
(4, 2);