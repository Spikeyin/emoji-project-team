"""课程模型"""

class Course:
    """课程类"""
    
    @staticmethod
    def create_course(mysql, course_name, course_code, teacher_id, description=None, semester=None):
        """创建课程"""
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO courses (course_name, course_code, teacher_id, description, semester) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (course_name, course_code, teacher_id, description, semester))
        mysql.connection.commit()
        course_id = cursor.lastrowid
        cursor.close()
        return course_id
    
    @staticmethod
    def get_by_id(mysql, course_id):
        """根据ID获取课程"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        course = cursor.fetchone()
        cursor.close()
        return course
    
    @staticmethod
    def get_all_courses(mysql, teacher_id=None, is_active=True):
        """获取所有课程"""
        cursor = mysql.connection.cursor()
        if teacher_id:
            cursor.execute("""SELECT c.*, u.full_name as teacher_name 
                            FROM courses c 
                            LEFT JOIN users u ON c.teacher_id = u.id
                            WHERE c.teacher_id = %s AND c.is_active = %s""", 
                          (teacher_id, is_active))
        else:
            cursor.execute("""SELECT c.*, u.full_name as teacher_name 
                            FROM courses c 
                            LEFT JOIN users u ON c.teacher_id = u.id
                            WHERE c.is_active = %s""", (is_active,))
        courses = cursor.fetchall()
        cursor.close()
        return courses
    
    @staticmethod
    def get_student_courses(mysql, user_id):
        """获取学生已选课程"""
        cursor = mysql.connection.cursor()
        sql = """SELECT c.*, u.full_name as teacher_name 
                 FROM courses c
                 INNER JOIN user_courses uc ON c.id = uc.course_id
                 LEFT JOIN users u ON c.teacher_id = u.id
                 WHERE uc.user_id = %s AND c.is_active = TRUE"""
        cursor.execute(sql, (user_id,))
        courses = cursor.fetchall()
        cursor.close()
        return courses
    
    @staticmethod
    def enroll_student(mysql, user_id, course_id):
        """学生选课"""
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", 
                          (user_id, course_id))
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            mysql.connection.rollback()
            cursor.close()
            return False
    
    @staticmethod
    def is_student_enrolled(mysql, user_id, course_id):
        """检查学生是否已选该课程"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM user_courses WHERE user_id = %s AND course_id = %s", 
                      (user_id, course_id))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

