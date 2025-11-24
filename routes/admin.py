"""管理员/教师相关路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models.user import User
from models.course import Course
from models.emoji_record import EmojiRecord
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_or_teacher_required(f):
    """管理员或教师权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        if not (current_user.is_admin() or current_user.is_teacher()):
            flash('需要管理员或教师权限', 'error')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """仅管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('需要管理员权限', 'error')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def init_admin_routes(mysql):
    """初始化管理员路由"""
    
    @admin_bp.route('/dashboard')
    @login_required
    @admin_or_teacher_required
    def dashboard():
        """管理员主页"""
        # 获取统计数据
        users_count = len(User.get_all_users(mysql))
        courses = Course.get_all_courses(mysql)
        courses_count = len(courses)
        
        # 获取最近7天的数据
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        stats = EmojiRecord.get_statistics(mysql, start_date=start_date, end_date=end_date)
        
        return render_template('admin/dashboard.html',
                             users_count=users_count,
                             courses_count=courses_count,
                             emoji_stats=stats)
    
    @admin_bp.route('/users')
    @login_required
    @admin_required
    def users():
        """用户管理"""
        role_filter = request.args.get('role', None)
        users_list = User.get_all_users(mysql, role=role_filter)
        return render_template('admin/users.html', users=users_list, role_filter=role_filter)
    
    @admin_bp.route('/courses')
    @login_required
    @admin_or_teacher_required
    def courses():
        """课程管理"""
        if current_user.is_teacher():
            courses_list = Course.get_all_courses(mysql, teacher_id=current_user.id)
        else:
            courses_list = Course.get_all_courses(mysql)
        return render_template('admin/courses.html', courses=courses_list)
    
    @admin_bp.route('/emoji_data')
    @login_required
    @admin_or_teacher_required
    def emoji_data():
        """表情数据查看"""
        course_id = request.args.get('course_id', None, type=int)
        
        # 获取课程列表
        if current_user.is_teacher():
            courses = Course.get_all_courses(mysql, teacher_id=current_user.id)
        else:
            courses = Course.get_all_courses(mysql)
        
        # 获取表情记录
        if course_id:
            records = EmojiRecord.get_course_records(mysql, course_id)
        else:
            records = EmojiRecord.get_all_records(mysql, limit=500)
        
        return render_template('admin/emoji_data.html', 
                             records=records, 
                             courses=courses,
                             selected_course_id=course_id)
    
    @admin_bp.route('/statistics')
    @login_required
    @admin_or_teacher_required
    def statistics():
        """统计数据"""
        course_id = request.args.get('course_id', None, type=int)
        days = request.args.get('days', 30, type=int)
        
        # 获取课程列表
        if current_user.is_teacher():
            courses = Course.get_all_courses(mysql, teacher_id=current_user.id)
        else:
            courses = Course.get_all_courses(mysql)
        
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # 获取统计数据
        stats = EmojiRecord.get_statistics(mysql, course_id=course_id, 
                                          start_date=start_date, end_date=end_date)
        
        return render_template('admin/statistics.html',
                             stats=stats,
                             courses=courses,
                             selected_course_id=course_id,
                             days=days)
    
    @admin_bp.route('/export')
    @login_required
    @admin_or_teacher_required
    def export():
        """导出数据为CSV"""
        course_id = request.args.get('course_id', None, type=int)
        days = request.args.get('days', 30, type=int)
        
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # 获取数据
        records = EmojiRecord.export_records(mysql, course_id=course_id,
                                           start_date=start_date, end_date=end_date)
        
        # 转换为DataFrame
        df = pd.DataFrame(records)
        
        if df.empty:
            flash('没有可导出的数据', 'warning')
            return redirect(url_for('admin.emoji_data'))
        
        # 创建Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='表情数据')
        output.seek(0)
        
        # 生成文件名
        filename = f'emoji_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        return send_file(output, 
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        as_attachment=True,
                        download_name=filename)
    
    @admin_bp.route('/api/chart_data')
    @login_required
    @admin_or_teacher_required
    def api_chart_data():
        """获取图表数据API"""
        course_id = request.args.get('course_id', None, type=int)
        days = request.args.get('days', 30, type=int)
        
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # 获取统计数据
        stats = EmojiRecord.get_statistics(mysql, course_id=course_id,
                                          start_date=start_date, end_date=end_date)
        
        # 格式化数据
        emoji_labels = [item['emoji_name'] for item in stats['emoji_stats']]
        emoji_values = [item['count'] for item in stats['emoji_stats']]
        
        date_labels = [str(item['session_date']) for item in stats['date_stats']]
        date_values = [item['count'] for item in stats['date_stats']]
        
        return jsonify({
            'emoji_chart': {
                'labels': emoji_labels,
                'values': emoji_values
            },
            'date_chart': {
                'labels': date_labels,
                'values': date_values
            },
            'total': stats['total']
        })
    
    return admin_bp

