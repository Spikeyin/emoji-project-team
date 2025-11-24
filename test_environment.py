"""环境测试脚本 - 验证系统配置是否正确"""
import sys

def test_python_version():
    """测试Python版本"""
    print("1. 测试Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python版本: {version.major}.{version.minor}.{version.micro} (符合要求)")
        return True
    else:
        print(f"   ✗ Python版本: {version.major}.{version.minor}.{version.micro} (需要3.8+)")
        return False

def test_imports():
    """测试必要的包是否已安装"""
    print("\n2. 测试依赖包...")
    packages = {
        'flask': 'Flask',
        'flask_mysqldb': 'Flask-MySQLdb',
        'flask_login': 'Flask-Login',
        'werkzeug': 'Werkzeug',
        'pandas': 'Pandas'
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} (未安装)")
            all_ok = False
    
    return all_ok

def test_mysql_connection():
    """测试MySQL连接"""
    print("\n3. 测试MySQL连接...")
    try:
        try:
            import MySQLdb
        except ImportError:
            import pymysql
            pymysql.install_as_MySQLdb()
            import MySQLdb
        
        from config import Config
        
        # 尝试连接数据库
        try:
            conn = MySQLdb.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                charset='utf8mb4'
            )
            print(f"   ✓ 成功连接到数据库: {Config.MYSQL_DB}")
            
            # 测试表是否存在
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            expected_tables = ['users', 'courses', 'emoji_records', 'user_courses', 'user_emoji_records']
            found_tables = [table[0] for table in tables]
            
            print(f"   ✓ 找到 {len(found_tables)} 个表:")
            for table in found_tables:
                print(f"     - {table}")
            
            missing_tables = set(expected_tables) - set(found_tables)
            if missing_tables:
                print(f"   ⚠ 缺少表: {', '.join(missing_tables)}")
                print("     请运行: mysql -u root -p < database/init.sql")
            
            cursor.close()
            conn.close()
            return len(missing_tables) == 0
            
        except MySQLdb.Error as e:
            print(f"   ✗ 数据库连接失败: {e}")
            print("     请检查:")
            print("     1. MySQL服务是否启动")
            print("     2. config.py中的数据库配置是否正确")
            print("     3. 数据库是否已创建: CREATE DATABASE emoji_checker_db;")
            return False
            
    except ImportError as e:
        print(f"   ✗ 无法导入MySQL模块: {e}")
        print("     请安装: pip install mysqlclient 或 pip install PyMySQL")
        return False

def test_config():
    """测试配置文件"""
    print("\n4. 测试配置文件...")
    try:
        from config import Config
        
        # 检查关键配置
        if Config.MYSQL_PASSWORD == 'your_password':
            print("   ⚠ 警告: 数据库密码使用默认值 'your_password'")
            print("     请在config.py中修改为实际的MySQL密码")
        else:
            print("   ✓ 数据库密码已配置")
        
        if Config.SECRET_KEY == 'emoji-checker-secret-key-2024':
            print("   ⚠ 警告: 使用默认SECRET_KEY")
            print("     生产环境请修改为随机密钥")
        else:
            print("   ✓ SECRET_KEY已自定义")
        
        print(f"   ✓ 数据库主机: {Config.MYSQL_HOST}")
        print(f"   ✓ 数据库用户: {Config.MYSQL_USER}")
        print(f"   ✓ 数据库名称: {Config.MYSQL_DB}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ 配置文件错误: {e}")
        return False

def test_file_structure():
    """测试项目文件结构"""
    print("\n5. 测试项目结构...")
    import os
    
    required_paths = [
        'app.py',
        'config.py',
        'requirements.txt',
        'models',
        'routes',
        'templates',
        'static',
        'database/init.sql'
    ]
    
    all_ok = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"   ✓ {path}")
        else:
            print(f"   ✗ {path} (不存在)")
            all_ok = False
    
    return all_ok

def main():
    """主测试函数"""
    print("=" * 60)
    print("表情符号检查器 - 环境测试")
    print("=" * 60)
    
    results = []
    
    results.append(("Python版本", test_python_version()))
    results.append(("依赖包", test_imports()))
    results.append(("配置文件", test_config()))
    results.append(("项目结构", test_file_structure()))
    results.append(("MySQL连接", test_mysql_connection()))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:15} : {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ 所有测试通过！可以运行应用:")
        print("  python app.py")
        print("\n然后访问: http://localhost:5000")
    else:
        print("\n✗ 存在问题，请根据上述提示解决")
        print("\n常见解决方案:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 初始化数据库: mysql -u root -p < database/init.sql")
        print("3. 配置数据库密码: 编辑 config.py")
        print("\n详细指南请查看: START_GUIDE.md")
    
    print("\n")
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

