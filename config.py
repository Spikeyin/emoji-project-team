import os
from datetime import timedelta

class Config:
    """应用配置类"""
    
    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'emoji-checker-secret-key-2024'
    
    # MySQL 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '2004.2.5Yym'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'emoji_checker_db'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Session 配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # 用户角色定义
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'
    
    # 表情符号列表
    EMOJI_LIST = ['😊', '😐', '😕', '😢', '😡', '🤔', '😴', '😃']
    EMOJI_NAMES = {
        '😊': '开心',
        '😐': '一般',
        '😕': '困惑',
        '😢': '难过',
        '😡': '生气',
        '🤔': '思考',
        '😴': '困倦',
        '😃': '兴奋'
    }

