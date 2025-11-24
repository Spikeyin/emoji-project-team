"""生成密码哈希的辅助脚本"""
from werkzeug.security import generate_password_hash

def generate_hashes():
    """生成所有默认账号的密码哈希"""
    passwords = {
        'admin123': 'admin',
        'teacher123': 'teacher1',
        'student123': 'student1/student2'
    }
    
    print("=== 密码哈希生成器 ===\n")
    
    for password, username in passwords.items():
        hash_value = generate_password_hash(password)
        print(f"用户: {username}")
        print(f"密码: {password}")
        print(f"哈希: {hash_value}")
        print("-" * 80)
        print()

if __name__ == '__main__':
    generate_hashes()
    
    # 生成自定义密码
    print("\n=== 自定义密码生成 ===")
    custom_password = input("输入要生成哈希的密码（直接回车跳过）: ")
    if custom_password:
        hash_value = generate_password_hash(custom_password)
        print(f"\n密码: {custom_password}")
        print(f"哈希: {hash_value}")

