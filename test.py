import pymysql

# 配置
host = 'localhost'
user = 'root'
password = '2004.2.5Yym'  # 使用你的实际密码
db = 'emoji_checker_db'

try:
    # 尝试连接
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # 测试查询
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print("连接成功:", result)
    
    conn.close()
    print("数据库连接测试通过!")
    
except Exception as e:
    print(f"连接失败: {e}")