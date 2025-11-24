"""用户模型"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    """用户类"""
    
    def __init__(self, id, username, password_hash, role, full_name=None, email=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.full_name = full_name
        self.email = email
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """是否为管理员"""
        return self.role == 'admin'
    
    def is_teacher(self):
        """是否为教师"""
        return self.role == 'teacher'
    
    def is_student(self):
        """是否为学生"""
        return self.role == 'student'
    
    @staticmethod
    def hash_password(password):
        """密码加密"""
        return generate_password_hash(password)
    
    @staticmethod
    def create_user(mysql, username, password, role, full_name=None, email=None):
        """创建新用户"""
        cursor = mysql.connection.cursor()
        password_hash = User.hash_password(password)
        
        sql = """INSERT INTO users (username, password_hash, role, full_name, email) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (username, password_hash, role, full_name, email))
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        
        return user_id
    
    @staticmethod
    def get_by_id(mysql, user_id):
        """根据ID获取用户"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                role=user_data['role'],
                full_name=user_data.get('full_name'),
                email=user_data.get('email')
            )
        return None
    
    @staticmethod
    def get_by_username(mysql, username):
        """根据用户名获取用户"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                role=user_data['role'],
                full_name=user_data.get('full_name'),
                email=user_data.get('email')
            )
        return None
    
    @staticmethod
    def update_password(mysql, user_id, new_password):
        """更新用户密码"""
        cursor = mysql.connection.cursor()
        password_hash = User.hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", 
                      (password_hash, user_id))
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def get_all_users(mysql, role=None):
        """获取所有用户"""
        cursor = mysql.connection.cursor()
        if role:
            cursor.execute("SELECT id, username, role, full_name, email, created_at FROM users WHERE role = %s", (role,))
        else:
            cursor.execute("SELECT id, username, role, full_name, email, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users

