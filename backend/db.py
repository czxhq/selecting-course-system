import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class database:
    def _init_(self):
        pass

    def __enter__(self):
        self.conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def export_student(course_id):
    with database() as cursor:
        cursor.execute("SELECT SC.Sid, User.name, Major.Mname, User.phone, User.email FROM SC, User, Major, Student WHERE Cid = %s AND User.id = SC.Sid AND Student.Sid = SC.Sid AND Student.Mid = Major.Mid ORDER BY Sid ASC", [course_id])
        return cursor.fetchall()

def export_admin_students():
    with database() as cursor:
        cursor.execute("SELECT User.id, User.name, User.gender, Major.Mname, User.phone, User.email, User.address FROM User, Major, Student WHERE User.id = Student.Sid AND Student.Mid = Major.Mid AND User.type = 0 ORDER BY User.id ASC")
        return cursor.fetchall()

def export_admin_teachers():
    with database() as cursor:
        cursor.execute("""
            SELECT User.id, User.name, User.gender, User.phone, User.email, User.address, Teacher.intro
                FROM User,
                Teacher
            WHERE User.id = Teacher.Tid
                 AND User.type = 1
            ORDER BY User.id ASC
            """)
        return cursor.fetchall()


def get_major_credits(student_id):
    with database() as cursor:
        cursor.execute("select Mid from student where Sid = %s", [student_id])
        major = cursor.fetchone()[0]
        cursor.execute("select * from major where Mid = %s", [major])
        return cursor.fetchone()

def get_student_credits(student_id):
    with database() as cursor:
        result = []
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.type = '必修'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.type = '选修'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.category = '一般专业类'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.category = '核心专业类'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.category = '核心通识类'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        cursor.execute("select SUM(credits) from Course, SC where SC.Sid = %s AND SC.Cid = Course.Cid AND Course.category = '一般通识类'", [student_id])
        tmp = cursor.fetchone()[0]
        result.append(tmp if tmp else 0)
        return result
    
def add_major(name, csum, esum, gmsum, cmsum, cgsum, gsum):
    with database() as cursor:
        cursor.execute("insert into major (Mname, csum, esum, gmsum, cmsum, cgsum, gsum) values(%s, %s, %s, %s, %s, %s, %s)",
                       [name, csum, esum, gmsum, cmsum, cgsum, gsum])

def add_review(student, course, rate, content=None):
    with database() as cursor:
        cursor.execute("insert into review (Sid, Cid, rate, content) values(%s, %s, %s, %s)",
                       [student, course, rate, content])
        
def get_majors():
    with database() as cursor:
        cursor.execute("select * from major")
        return cursor.fetchall()

def alter_major(name, csum, esum, gmsum, cmsum, cgsum, gsum):
    with database() as cursor:
        cursor.execute("update major set csum = %s, esum = %s, gmsum = %s, cmsum = %s, cgsum = %s, gsum = %s where Mname = %s",
                       [csum, esum, gmsum, cmsum, cgsum, gsum, name])

def enroll_student(course_id):
    with database() as cursor:
        cursor.execute("SELECT Sid, name FROM SC, User WHERE SC.Cid = %s AND SC.Sid = User.id", [course_id])
        return cursor.fetchall()

def get_admin_password(user_id):
    with database() as cursor:
        cursor.execute("SELECT password FROM user WHERE id = %s AND type = 2", [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def search_student_name(name):
    with database() as cursor:
        cursor.execute("select id, name from user where name like %s and type = 0", ['%' + name + '%'])
        return cursor.fetchall()


def search_teacher_name(name):
    with database() as cursor:
        cursor.execute("select id, name from user where name like %s and type = 1", ['%' + name + '%'])
        return cursor.fetchall()


def search_student_id(id):
    with database() as cursor:
        cursor.execute("select id, name from user where id = %s and type = 0", [id])
        return cursor.fetchall()


def search_teacher_id(id):
    with database() as cursor:
        cursor.execute("select id, name from user where id = %s and type = 1", [id])
        return cursor.fetchall()


def add_student(id, name, mid, password='88888888', gender='暂无', college='暂无', grade='暂无', class_id='暂无',
                email='暂无', address='暂无',
                phone='暂无'):
    with database() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("insert into user values (%s, 0, %s, %s, %s, %s, %s, %s, %s)",
                           [id, name, gender, college, phone, email, address, password])
            cursor.execute("insert into student values (%s, %s, %s, %s)", [id, grade, class_id, mid])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")

def get_major_id(name):
    with database() as cursor:
        cursor.execute("select Mid from major where Mname = %s", [name])
        return cursor.fetchone()
    
def add_teacher(id, name, password='88888888', gender='暂无', college='暂无', title='暂无', email='暂无', phone='暂无',
                address='暂无',
                intro='暂无'):
    with database() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("insert into user values (%s, 1, %s, %s, %s, %s, %s, %s, %s)",
                           [id, name, gender, college, phone, email, address, password])
            cursor.execute("insert into teacher values(%s, %s, %s)", [id, title, intro])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")


def update_user_password(id, password):
    with database() as cursor:
        cursor.execute("update user set password = %s where id = %s", [password, id])


def add_announce(title, content=None):
    with database() as cursor:
        cursor.execute("insert into announce (title, content) values(%s, %s)",
                       [title, content])


def get_announces():
    with database() as cursor:
        cursor.execute("select * from announce")
        return cursor.fetchall()


def update_student_profile(id, email, phone, address):
    with database() as cursor:
        cursor.execute("update user set email = %s, phone = %s, address = %s where id = %s",
                       [email, phone, address, id])


def del_student(id):
    with database() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("delete from question where Sid = %s", [id])
            cursor.execute("delete from review where Sid = %s", [id])
            cursor.execute("delete from sc where Sid = %s", [id])
            cursor.execute("delete from un where id = %s", [id])
            cursor.execute("DELETE FROM CN WHERE Nid IN (SELECT Nid FROM Notice WHERE sender = %s)", [id])
            cursor.execute("DELETE FROM UN WHERE Nid IN (SELECT Nid FROM Notice WHERE sender = %s)", [id])
            cursor.execute("delete from Notice where sender = %s", [id])
            cursor.execute("delete from student where Sid = %s", [id])
            cursor.execute("delete from user where id = %s", [id])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")


def del_teacher(id):
    with database() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute(
                "SELECT Cid FROM (SELECT DISTINCT Cid, Tid FROM TC GROUP BY Cid HAVING COUNT(*) = 1) AS T WHERE Tid = %s",
                [id])
            courses = cursor.fetchall()
            for course in courses:
                delete_course(course[0])

            cursor.execute("delete from question where Tid = %s", [id])
            cursor.execute("DELETE FROM CN WHERE Nid IN (SELECT Nid FROM Notice WHERE sender = %s)", [id])
            cursor.execute("DELETE FROM UN WHERE Nid IN (SELECT Nid FROM Notice WHERE sender = %s)", [id])
            cursor.execute("delete from un where id = %s", [id])
            cursor.execute("delete from tc where Tid = %s", [id])
            cursor.execute("delete from Notice where Sender = %s", [id])
            cursor.execute("delete from teacher where Tid = %s", [id])
            cursor.execute("delete from user where id = %s", [id])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")


def get_course_reviews(course_id):
    with database() as cursor:
        cursor.execute("SELECT * FROM Review WHERE Cid = %s", [course_id])
        return cursor.fetchall()


def get_student_profile(student_id):
    with database() as cursor:
        cursor.execute("SELECT * FROM User WHERE id = %s", [student_id])
        result = cursor.fetchone()
        if result:
            student_profile = {
                'id': result[0],
                'name': result[2],
                'email': result[6],
                'phone': result[5],
                'address': result[7]
            }
            return student_profile
        else:
            return None


def update_teacher_profile(id, email, phone, address, intro):
    with database() as cursor:
        cursor.execute("update user set email = %s, phone = %s, address = %s where id = %s",
                       [email, phone, address, id])
        cursor.execute("update teacher set intro = %s where Tid = %s", [intro, id])


def get_teacher_profile(teacher_id):
    with database() as cursor:
        cursor.execute("SELECT * FROM User WHERE id = %s", [teacher_id])
        result = cursor.fetchone()
        cursor.execute("SELECT intro FROM Teacher WHERE Tid = %s", [teacher_id])
        intro = cursor.fetchone()
        teacher_profile = {
            'id': result[0],
            'name': result[2],
            'email': result[6],
            'phone': result[5],
            'address': result[7],
            'intro': intro
        }
        return teacher_profile
    
def get_course_answered_questions(course_id):
    with database() as cursor:
        cursor.execute("SELECT * FROM Question WHERE Cid = %s AND answer IS NOT NULL", [course_id])
        return cursor.fetchall()


def get_user_password(user_id):
    with database() as cursor:
        cursor.execute("SELECT password FROM user WHERE id = %s", [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def get_student_password(user_id):
    with database() as cursor:
        cursor.execute("SELECT password FROM user WHERE id = %s AND type=0", [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def get_teacher_password(user_id):
    with database() as cursor:
        cursor.execute("SELECT password FROM user WHERE id = %s AND type=1", [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def reset_user_password(user_id):
    with database() as cursor:
        cursor.execute("update user set password = 88888888 where id = %s", [user_id])


def get_all_students():
    with database() as cursor:
        cursor.execute("SELECT User.id, User.name, Major.Mname FROM User, Student, Major WHERE type = 0 AND Student.Sid = User.id AND Student.Mid = Major.Mid")
        return cursor.fetchall()


def get_all_teachers():
    with database() as cursor:
        cursor.execute("SELECT id, name FROM User WHERE type = 1")
        return cursor.fetchall()


def get_courses(user_id):
    with database() as cursor:
        cursor.execute(
            """
            SELECT C.Cid,
                C.Cname,
                C.room,
                C.date,
                U.name
            FROM (SELECT * FROM SC WHERE SC.Sid = %s) AS S
                LEFT JOIN
                Course C ON C.Cid = S.Cid
                LEFT JOIN
                TC TC ON C.Cid = TC.Cid
                LEFT JOIN
                User U ON TC.Tid = U.id
            """,
            [user_id])
        return cursor.fetchall()

def enroll_course_info(student_id, course_id):
    with database() as cursor:
        cursor.execute("""
        SELECT C.date
            FROM (SELECT * FROM SC WHERE SC.Sid = %s) AS S
            LEFT JOIN
            Course C ON C.Cid = S.Cid;"""
            , [student_id])
        times = cursor.fetchall()

        cursor.execute("SELECT date FROM Course WHERE Cid = %s", [course_id])
        time = cursor.fetchone()[0]
        return times, time

def course_details(student_id):
    with database() as cursor:
        cursor.execute(
            """
        SELECT *
        FROM (SELECT S.Sid,
             C.Cid,
             C.Cname,
             C.room,
             C.date,
             C.type,
             C.category,
             CONCAT(C.capacity, '/', COUNT(S.Sid)),
             C.credits,
             U.name
        FROM SC S
               LEFT JOIN
            Course C ON C.Cid = S.Cid
               LEFT JOIN
            TC TC ON C.Cid = TC.Cid
               LEFT JOIN
            User U ON TC.Tid = U.id
        GROUP BY C.Cid, U.name) AS T
        WHERE Sid = %s
            """, [student_id])
        return cursor.fetchall()


def cancel_course(student_id, course_id):
    with database() as cursor:
        cursor.execute("delete from sc where Sid = %s and Cid = %s", [student_id, course_id])

def get_course_details(course_id):
    with database() as cursor:
        cursor.execute("""
        SELECT C.Cid,
            C.Cname,
            C.room,
            C.credits,
            C.date,
            C.type,
            C.category,
            CONCAT(C.capacity, '/', COUNT(S.Sid)),
            C.detail,
            U.name,
            T.intro
        FROM (SELECT * FROM Course WHERE Cid = %s) AS C
                LEFT JOIN
            TC TC ON C.Cid = TC.Cid
                LEFT JOIN
            Teacher T ON TC.Tid = T.Tid
                LEFT JOIN
            User U ON T.Tid = U.id
                LEFT JOIN
            SC S ON C.Cid = S.Cid
        GROUP BY C.Cid, U.name;
        """, [course_id])
        course_info = cursor.fetchall()

        cursor.execute("""
            SELECT User.name,
            R.rate,
            R.content
            FROM (SELECT * FROM Review WHERE Cid = %s) AS R, User
            WHERE R.Sid = User.id;
            """, [course_id])
        reviews =  cursor.fetchall()

        cursor.execute("SELECT * FROM Question WHERE Cid = %s AND answer IS NOT NULL", [course_id])
        questions = cursor.fetchall()
    return course_info, reviews, questions

def get_course_info(course_id):
    with database() as cursor:
        cursor.execute("""
SELECT C.Cid,
       C.Cname,
       C.room,
       C.credits,
       C.date,
       C.type,
       C.category,
       CONCAT(C.capacity, '/', COUNT(S.Sid)),
       C.detail,
       U.name,
       T.intro
FROM (SELECT * FROM Course WHERE Cid = %s) AS C
         LEFT JOIN
     TC TC ON C.Cid = TC.Cid
         LEFT JOIN
     Teacher T ON TC.Tid = T.Tid
         LEFT JOIN
     User U ON T.Tid = U.id
         LEFT JOIN
     SC S ON C.Cid = S.Cid
GROUP BY C.Cid, U.name;
""", [course_id])
        return cursor.fetchall()
        

def publish_question(course_id, content):
    with database() as cursor:
        cursor.execute("INSERT INTO Question (Cid, content) VALUES (%s, %s)", [course_id, content])
        cursor.execute("INSERT INTO Notice (title, content) VALUES ('您有新的提问', %s)", [content])
        cursor.execute("INSERT INTO CN (Nid, Cid) VALUES (LAST_INSERT_ID(), %s)", [course_id])
        cursor.execute("INSERT INTO UN (Nid, id) SELECT LAST_INSERT_ID(), Tid FROM TC WHERE Cid = %s", [course_id])

def get_user_name(user_id):
    with database() as cursor:
        cursor.execute("SELECT name FROM User WHERE id = %s", [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def search_user_name(name):
    with database() as cursor:
        cursor.execute("SELECT * FROM User WHERE name LIKE %s", ['%' + name + '%'])
        return cursor.fetchall()


def search_courses_by_name(course_name):
    with database() as cursor:
        cursor.execute("""
SELECT C.Cid,
       C.Cname,
       C.room,
       C.date,
       C.type,
       C.category,
       CONCAT(C.capacity, '/', COUNT(S.Sid)),
       C.credits,
       U.name
FROM Course C
         LEFT JOIN
     TC TC ON C.Cid = TC.Cid
         LEFT JOIN
     User U ON TC.Tid = U.id
         LEFT JOIN
     SC S ON C.Cid = S.Cid
WHERE Cname LIKE %s
GROUP BY C.Cid, U.name
""", ['%' + course_name + '%'])
        return cursor.fetchall()


def search_courses_by_teacher(teacher_name):
    with database() as cursor:
        cursor.execute("""
        SELECT C.Cid,
            C.Cname,
            C.room,
            C.date,
            C.type,
            C.category,
            CONCAT(C.capacity, '/', COUNT(S.Sid)),
            C.credits,
            U.name
        FROM Course C
            LEFT JOIN
            TC TC ON C.Cid = TC.Cid
            LEFT JOIN
            User U ON TC.Tid = U.id
            LEFT JOIN
            SC S ON C.Cid = S.Cid
        WHERE U.name LIKE %s
        GROUP BY C.Cid, U.name;
        """, ['%' + teacher_name + '%'])
        return cursor.fetchall()


def get_course_enrollment(course_id):
    with database() as cursor:
        cursor.execute("SELECT COUNT(*) FROM SC WHERE Cid = %s", [course_id])
        result = cursor.fetchone()
        return result[0] if result else 0


def enroll_course(student_id, course_id):
    with database() as cursor:
        cursor.execute("SELECT COUNT(*) FROM SC WHERE Cid = %s", [course_id])
        cnt = cursor.fetchone()
        cursor.execute("SELECT capacity FROM Course WHERE Cid = %s", [course_id])
        capacity = cursor.fetchone()
        if cnt[0] >= capacity[0]:
            return False
        cursor.execute("INSERT INTO SC (Sid, Cid) VALUES (%s, %s)", [student_id, course_id])
    return True


def get_course_capacity(course_id):
    with database() as cursor:
        cursor.execute("SELECT capacity FROM Course WHERE Cid = %s", [course_id])
        result = cursor.fetchone()
        return result[0] if result else 0


def get_all_courses():
    with database() as cursor:
        cursor.execute(
        """
        SELECT C.Cid,
            C.Cname,
            C.room,
            C.date,
            C.type,
            C.category,
            CONCAT(C.capacity, '/', COUNT(S.Sid)),
            C.credits,
            U.name
        FROM Course C
            LEFT JOIN
            TC TC ON C.Cid = TC.Cid
            LEFT JOIN
            User U ON TC.Tid = U.id
            LEFT JOIN
            SC S ON C.Cid = S.Cid
        GROUP BY C.Cid, U.name;
        """)
        return cursor.fetchall()

def get_selected_id(student_id):
    with database() as cursor:
        cursor.execute("SELECT Cid FROM SC WHERE Sid = %s", [student_id])
        return cursor.fetchall()

def get_user_messages(user_id):
    with database() as cursor:
        # 获取用户相关的通知（Notice）
        cursor.execute("""
            SELECT N.Nid, N.title, N.date, N.content, Course.Cname FROM Notice N, CN, UN, Course where N.Nid = CN.Nid and CN.Cid = Course.Cid and UN.Nid = N.Nid and UN.id = %s
            ORDER BY N.date DESC
        """, [user_id])
        notices = cursor.fetchall()

        # 获取所有公告（Announce）
        cursor.execute("""
            SELECT Aid, title, date, content
            FROM Announce
            ORDER BY date DESC
        """)
        announces = cursor.fetchall()

        # 合并通知和公告
        messages = []
        for notice in notices:
            messages.append({
                'id': notice[0],
                'title': notice[1],
                'date': notice[2].strftime('%Y-%m-%d'),
                'content': notice[3],
                'from': notice[4]
            })
        for announce in announces:
            messages.append({
                'id': announce[0],
                'title': announce[1],
                'date': announce[2].strftime('%Y-%m-%d'),
                'content': announce[3],
                'from': '管理员'
            })
        return messages


def publish_course(teacher_id, course_name, credits, time, location, capacity, type, category, course_details):
    with database() as cursor:
        # 插入课程信息到 Course 表
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("""
                    INSERT INTO Course (Cname, credits, date, room, capacity, type, category, detail)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [course_name, credits, time, location, capacity, type, category, course_details])
            # 将教师和课程的关系添加到 TC 表
            cursor.execute("INSERT INTO TC (Tid, Cid) VALUES (%s, %s)",
                        [teacher_id, cursor.lastrowid])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")


def delete_course(course_id):
    with database() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("DELETE FROM SC WHERE Cid = %s", [course_id])
            cursor.execute("DELETE FROM TC WHERE Cid = %s", [course_id])

            cursor.execute("DELETE FROM UN WHERE Nid IN (SELECT Nid FROM CN WHERE Cid = %s)", [course_id])
            cursor.execute("DELETE FROM CN WHERE Cid = %s", [course_id])

            cursor.execute("DELETE FROM Review WHERE Cid = %s", [course_id])
            cursor.execute("DELETE FROM Question WHERE Cid = %s", [course_id])
            cursor.execute("DELETE FROM Course WHERE Cid = %s", [course_id])
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")


def publish_course_notice(course_id, title, content):
    with database() as cursor:
        cursor.execute("INSERT INTO Notice (title, content) VALUES (%s, %s)",
                       [title, content])
        cursor.execute("INSERT INTO CN (Nid, Cid) VALUES (LAST_INSERT_ID(), %s)", [course_id])
        cursor.execute("INSERT INTO UN (Nid, id) SELECT LAST_INSERT_ID(), Sid FROM SC WHERE Cid = %s", [course_id])


def get_teacher_courses(teacher_id):
    with database() as cursor:
        cursor.execute("""
            SELECT Course.Cid, Course.Cname, Course.date, Course.room
            FROM Course
            JOIN TC ON Course.Cid = TC.Cid
            WHERE TC.Tid = %s
        """, [teacher_id])
        return cursor.fetchall()


def is_course_enrolled(student_id, course_id):
    with database() as cursor:
        cursor.execute("SELECT * FROM SC WHERE Sid = %s AND Cid = %s", [student_id, course_id])
        return cursor.fetchone() is not None


def alter_course(course_id, course_name, credits, time, location, capacity, type, category, course_details):
    with database() as cursor:
        cursor.execute(
            "UPDATE Course SET Cname = %s, credits = %s, date = %s, room = %s, capacity = %s, type = %s, category = %s, detail = %s WHERE Cid = %s",
            [course_name, credits, time, location, capacity, type, category, course_details, course_id])


def answer_question(question_id, answer):
    with database() as cursor:
        cursor.execute("UPDATE Question SET answer = %s WHERE Qid = %s", [answer, question_id])
        cursor.execute("SELECT Nid FROM Notice WHERE content = (SELECT content FROM Question WHERE Qid = %s)", [question_id])
        notice_id = cursor.fetchone()[0]
        cursor.execute("DELETE FROM UN WHERE Nid = %s", [notice_id])
        cursor.execute("DELETE FROM CN WHERE Nid = %s", [notice_id])
        cursor.execute("DELETE FROM Notice WHERE Nid = %s", [notice_id])


def get_questions(course_id):
    with database() as cursor:
        cursor.execute("SELECT Qid, content FROM Question WHERE Cid = %s AND answer IS NULL", [course_id])
        return cursor.fetchall()