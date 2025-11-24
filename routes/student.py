"""学生相关路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models.course import Course
from models.emoji_record import EmojiRecord
from config import Config

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    """学生权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash('需要学生权限', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def init_student_routes(mysql):
    """初始化学生路由"""
    
    @student_bp.route('/dashboard')
    @login_required
    @student_required
    def dashboard():
        """学生主页"""
        courses = Course.get_student_courses(mysql, current_user.id)
        return render_template('student/dashboard.html', courses=courses)
    
    @student_bp.route('/courses')
    @login_required
    @student_required
    def courses():
        """查看所有可选课程"""
        all_courses = Course.get_all_courses(mysql)
        enrolled_courses = Course.get_student_courses(mysql, current_user.id)
        enrolled_ids = [c['id'] for c in enrolled_courses]
        
        return render_template('student/courses.html', 
                             courses=all_courses, 
                             enrolled_ids=enrolled_ids)
    
    @student_bp.route('/enroll/<int:course_id>', methods=['POST'])
    @login_required
    @student_required
    def enroll(course_id):
        """选课"""
        if Course.is_student_enrolled(mysql, current_user.id, course_id):
            flash('您已经选过这门课程了', 'warning')
        else:
            if Course.enroll_student(mysql, current_user.id, course_id):
                flash('选课成功！', 'success')
            else:
                flash('选课失败', 'error')
        
        return redirect(url_for('student.courses'))
    
    @student_bp.route('/send_emoji', methods=['GET', 'POST'])
    @login_required
    @student_required
    def send_emoji():
        """发送表情"""
        if request.method == 'POST':
            course_id = request.form.get('course_id')
            emoji = request.form.get('emoji')
            comment = request.form.get('comment', '')
            
            # 验证
            if not course_id or not emoji:
                flash('请选择课程和表情', 'error')
                return redirect(url_for('student.send_emoji'))
            
            # 检查是否已选该课程
            if not Course.is_student_enrolled(mysql, current_user.id, int(course_id)):
                flash('您未选择该课程，无法提交评价', 'error')
                return redirect(url_for('student.send_emoji'))
            
            # 获取表情名称
            emoji_name = Config.EMOJI_NAMES.get(emoji, '未知')
            
            # 创建记录
            EmojiRecord.create_record(mysql, current_user.id, course_id, emoji, emoji_name, comment)
            flash('表情提交成功！感谢您的反馈', 'success')
            return redirect(url_for('student.history'))
        
        # GET请求
        courses = Course.get_student_courses(mysql, current_user.id)
        emoji_list = Config.EMOJI_LIST
        emoji_names = Config.EMOJI_NAMES
        
        return render_template('student/send_emoji.html', 
                             courses=courses,
                             emoji_list=emoji_list,
                             emoji_names=emoji_names)
    
    @student_bp.route('/history')
    @login_required
    @student_required
    def history():
        """查看历史记录"""
        records = EmojiRecord.get_user_records(mysql, current_user.id)
        return render_template('student/history.html', records=records)
    
    return student_bp

