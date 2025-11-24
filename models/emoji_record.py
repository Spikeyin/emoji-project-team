"""表情符号记录模型"""
from datetime import datetime, date

class EmojiRecord:
    """表情符号记录类"""
    
    @staticmethod
    def create_record(mysql, user_id, course_id, emoji, emoji_name, comment=None):
        """创建表情记录（匿名化存储）"""
        cursor = mysql.connection.cursor()
        
        # 获取当前日期和时间
        session_date = date.today()
        session_time = datetime.now().time()
        
        # 在emoji_records表中插入匿名记录
        sql = """INSERT INTO emoji_records (course_id, emoji, emoji_name, session_date, session_time, comment) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (course_id, emoji, emoji_name, session_date, session_time, comment))
        emoji_record_id = cursor.lastrowid
        
        # 在user_emoji_records表中关联用户和记录（用于用户查看自己的历史）
        sql = "INSERT INTO user_emoji_records (user_id, emoji_record_id) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, emoji_record_id))
        
        mysql.connection.commit()
        cursor.close()
        return emoji_record_id
    
    @staticmethod
    def get_user_records(mysql, user_id):
        """获取用户自己的表情历史记录"""
        cursor = mysql.connection.cursor()
        sql = """SELECT er.*, c.course_name, c.course_code
                 FROM emoji_records er
                 INNER JOIN user_emoji_records uer ON er.id = uer.emoji_record_id
                 INNER JOIN courses c ON er.course_id = c.id
                 WHERE uer.user_id = %s
                 ORDER BY er.created_at DESC"""
        cursor.execute(sql, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        
        # 处理时间格式
        for record in records:
            if record['session_time'] and hasattr(record['session_time'], 'seconds'):
                hours = record['session_time'].seconds // 3600
                minutes = (record['session_time'].seconds // 60) % 60
                seconds = record['session_time'].seconds % 60
                record['time_formatted'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                record['time_formatted'] = ""
                
        return records
    
    @staticmethod
    def get_course_records(mysql, course_id, start_date=None, end_date=None):
        """获取课程的所有表情记录（匿名）"""
        cursor = mysql.connection.cursor()
        
        if start_date and end_date:
            sql = """SELECT emoji, emoji_name, session_date, session_time, comment, created_at
                     FROM emoji_records
                     WHERE course_id = %s AND session_date BETWEEN %s AND %s
                     ORDER BY session_date DESC, session_time DESC"""
            cursor.execute(sql, (course_id, start_date, end_date))
        else:
            sql = """SELECT emoji, emoji_name, session_date, session_time, comment, created_at
                     FROM emoji_records
                     WHERE course_id = %s
                     ORDER BY session_date DESC, session_time DESC"""
            cursor.execute(sql, (course_id,))
        
        records = cursor.fetchall()
        
        # 处理时间格式
        for record in records:
            if record['session_time'] and hasattr(record['session_time'], 'seconds'):
                hours = record['session_time'].seconds // 3600
                minutes = (record['session_time'].seconds // 60) % 60
                seconds = record['session_time'].seconds % 60
                record['time_formatted'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                record['time_formatted'] = ""
        
        cursor.close()
        return records
    
    @staticmethod
    def get_all_records(mysql, limit=1000):
        """获取所有表情记录（管理员用）"""
        cursor = mysql.connection.cursor()
        sql = """SELECT er.*, c.course_name, c.course_code
                 FROM emoji_records er
                 INNER JOIN courses c ON er.course_id = c.id
                 ORDER BY er.created_at DESC
                 LIMIT %s"""
        cursor.execute(sql, (limit,))
        records = cursor.fetchall()
        
        # 处理时间格式
        for record in records:
            if record['session_time'] and hasattr(record['session_time'], 'seconds'):
                hours = record['session_time'].seconds // 3600
                minutes = (record['session_time'].seconds // 60) % 60
                seconds = record['session_time'].seconds % 60
                record['time_formatted'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                record['time_formatted'] = ""
        
        cursor.close()
        return records
    
    @staticmethod
    def get_statistics(mysql, course_id=None, start_date=None, end_date=None):
        """获取表情统计数据"""
        cursor = mysql.connection.cursor()
        
        conditions = []
        params = []
        
        if course_id:
            conditions.append("course_id = %s")
            params.append(course_id)
        
        if start_date and end_date:
            conditions.append("session_date BETWEEN %s AND %s")
            params.extend([start_date, end_date])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # 按表情统计
        sql = f"""SELECT emoji, emoji_name, COUNT(*) as count
                  FROM emoji_records
                  WHERE {where_clause}
                  GROUP BY emoji, emoji_name
                  ORDER BY count DESC"""
        cursor.execute(sql, params)
        emoji_stats = cursor.fetchall()
        
        # 按日期统计
        sql = f"""SELECT session_date, COUNT(*) as count
                  FROM emoji_records
                  WHERE {where_clause}
                  GROUP BY session_date
                  ORDER BY session_date DESC"""
        cursor.execute(sql, params)
        date_stats = cursor.fetchall()
        
        # 总数统计
        sql = f"""SELECT COUNT(*) as total FROM emoji_records WHERE {where_clause}"""
        cursor.execute(sql, params)
        total = cursor.fetchone()['total']
        
        cursor.close()
        
        return {
            'emoji_stats': emoji_stats,
            'date_stats': date_stats,
            'total': total
        }
    
    @staticmethod
    def export_records(mysql, course_id=None, start_date=None, end_date=None):
        """导出表情记录数据（用于CSV导出）"""
        cursor = mysql.connection.cursor()
        
        conditions = []
        params = []
        
        if course_id:
            conditions.append("er.course_id = %s")
            params.append(course_id)
        
        if start_date and end_date:
            conditions.append("er.session_date BETWEEN %s AND %s")
            params.extend([start_date, end_date])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        sql = f"""SELECT c.course_name, c.course_code, er.emoji, er.emoji_name, 
                        er.session_date, er.session_time, er.comment, er.created_at
                  FROM emoji_records er
                  INNER JOIN courses c ON er.course_id = c.id
                  WHERE {where_clause}
                  ORDER BY er.session_date DESC, er.session_time DESC"""
        
        cursor.execute(sql, params)
        records = cursor.fetchall()
        cursor.close()
        return records

