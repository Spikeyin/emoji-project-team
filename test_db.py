"""数据库连接测试脚本"""
import pymysql
from config import Config

def test_connection():
    """测试数据库连接"""
    try:
        # 尝试连接
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        # 测试查询
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            print("连接成功:", result)
            
            # 测试查询用户表
            cursor.execute("SELECT * FROM users LIMIT 1")
            user = cursor.fetchone()
            if user:
                print(f"成功查询用户: ID={user['id']}, 用户名={user['username']}, 角色={user['role']}")
            else:
                print("用户表为空")
        
        conn.close()
        print("数据库连接测试通过!")
        return True
        
    except Exception as e:
        print(f"连接失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试数据库连接...")
    test_connection()
