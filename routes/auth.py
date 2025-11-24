"""认证相关路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(mysql):
    """初始化认证路由"""
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        """登录"""
        if current_user.is_authenticated:
            # 已登录，根据角色跳转
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif current_user.is_teacher():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.get_by_username(mysql, username)
            
            if user and user.check_password(password):
                login_user(user, remember=True)
                flash('登录成功！', 'success')
                
                # 根据角色跳转
                if user.is_admin() or user.is_teacher():
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('student.dashboard'))
            else:
                flash('用户名或密码错误', 'error')
        
        return render_template('login.html')
    
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        """注册"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            role = request.form.get('role', 'student')
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            
            # 验证
            if not username or not password:
                flash('用户名和密码不能为空', 'error')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('两次输入的密码不一致', 'error')
                return render_template('register.html')
            
            # 检查用户名是否已存在
            if User.get_by_username(mysql, username):
                flash('用户名已存在', 'error')
                return render_template('register.html')
            
            # 创建用户
            try:
                User.create_user(mysql, username, password, role, full_name, email)
                flash('注册成功！请登录', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash(f'注册失败：{str(e)}', 'error')
        
        return render_template('register.html')
    
    @auth_bp.route('/logout')
    @login_required
    def logout():
        """登出"""
        logout_user()
        flash('已退出登录', 'info')
        return redirect(url_for('auth.login'))
    
    @auth_bp.route('/change_password', methods=['GET', 'POST'])
    @login_required
    def change_password():
        """修改密码"""
        if request.method == 'POST':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # 验证旧密码
            if not current_user.check_password(old_password):
                flash('原密码错误', 'error')
                return render_template('change_password.html')
            
            # 验证新密码
            if new_password != confirm_password:
                flash('两次输入的新密码不一致', 'error')
                return render_template('change_password.html')
            
            # 更新密码
            User.update_password(mysql, current_user.id, new_password)
            flash('密码修改成功！', 'success')
            return redirect(url_for('student.dashboard' if current_user.is_student() else 'admin.dashboard'))
        
        return render_template('change_password.html')
    
    return auth_bp

