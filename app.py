"""表情符号检查器 - 主应用"""
import pymysql
from flask import Flask, render_template, redirect, url_for, g
from flask_login import LoginManager, current_user
from config import Config
from models.user import User

# 创建应用
app = Flask(__name__)
app.config.from_object(Config)

# 使用 PyMySQL 直接连接
def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 创建一个与 Flask-MySQLdb 兼容的适配器类
class MySQLAdapter:
    """兼容 Flask-MySQLdb 的适配器"""
    @property
    def connection(self):
        return get_db()

# 创建适配器实例
mysql = MySQLAdapter()

# 初始化登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'

@login_manager.user_loader
def load_user(user_id):
    """加载用户"""
    return User.get_by_id(mysql, int(user_id))

# 导入并注册路由
from routes.auth import init_auth_routes
from routes.student import init_student_routes
from routes.admin import init_admin_routes

app.register_blueprint(init_auth_routes(mysql))
app.register_blueprint(init_student_routes(mysql))
app.register_blueprint(init_admin_routes(mysql))

@app.route('/')
def index():
    """首页"""
    if current_user.is_authenticated:
        # 根据用户角色重定向
        if current_user.is_admin() or current_user.is_teacher():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def page_not_found(e):
    """404错误处理"""
    return render_template('error.html', error_code=404, error_message='页面未找到'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """500错误处理"""
    return render_template('error.html', error_code=500, error_message='服务器内部错误'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)