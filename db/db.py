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
        self.cursor.close()
        self.conn.close()

    def add_student(self, id, password, name="null", gender="null", college="null", grade="null", class_id="null",
                    phone="null", mid="null"):
        with self as cursor:
            cursor.execute("insert into user values(%s, 0, %s, %s, %s, %s)", [id, name, gender, college, password])
            cursor.execute("insert into student values(%s, %s, %s, %s, %s)", [id, grade, class_id, phone, mid])
            self.conn.commit()

    def update_student_phone(self, student, phone):
        with self as cursor:
            cursor.execute("update student set phone = %s where Sid = %s", [phone, student])
            self.conn.commit()

    def add_teacher(self, id, password, name="null", gender="null", college="null", title="null", email="null",
                    intro="null"):
        with self as cursor:
            cursor.execute("insert into user values(%s, 1, %s, %s, %s, %s)", [id, name, gender, college, password])
            cursor.execute("insert into teacher values(%s, %s, %s, %s, %s)", [id, title, email, intro])
            self.conn.commit()

    def update_teacher_email(self, teacher, email):
        with self as cursor:
            cursor.execute("update teacher set email = %s where Tid = %s", [email, teacher])
            self.conn.commit()

    def update_teacher_intro(self, teacher, intro):
        with self as cursor:
            cursor.execute("update teacher set intro = %s where Tid = %s", [intro, teacher])
            self.conn.commit()

    def update_user_password(self, id, password):
        with self as cursor:
            cursor.execute("update user set password = %s where id = %s", [password, id])
            self.conn.commit()

    def add_course(self, id, name, credit, capacity, type, category, semester, date, hours, room, pre_course="null"):
        with self as cursor:
            cursor.execute("insert into course values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [id, name, credit, pre_course, capacity, type, category, semester, date, hours, room])
            self.conn.commit()

    def update_course_info(self, id, name, credit, capacity, type, category, semester, date, hours, room,
                           pre_course="null"):
        with self as cursor:
            cursor.execute(
                "update course set name = %s, credit = %s, capacity = %s, type = %s, category = %s, semester = %s, date = %s, hours = %s, room = %s, pre_course = %s where Cid = %s)",
                [name, credit, pre_course, capacity, type, category, semester, date, hours, room, id])
            self.conn.commit()

    def add_review(self, student, course, rate, content="null"):
        with self as cursor:
            cursor.execute("insert into review (Sid, Cid, rate, content) values(%s, %s, %s, %s)",
                           [student, course, rate, content])
            self.conn.commit()

    def add_notice(self, title, sender, content="null"):
        with self as cursor:
            cursor.execute("insert into notice (title, sender, content) values(%s, %s, %s)",
                           [title, sender, content])
            self.conn.commit()

    def add_announce(self, title, content="null"):
        with self as cursor:
            cursor.execute("insert into announce (title, content) values(%s, %s)",
                           [title, content])
            self.conn.commit()

    def add_question(self, student, course, content):
        with self as cursor:
            cursor.execute("insert into question (Sid, Cid, content) values(%s, %s, %s)",
                           [student, course, content])
            self.conn.commit()

    def add_answer(self, question, teacher, content):
        with self as cursor:
            cursor.execute("update question set Tid = %s, content = %s where Qid = %s",
                           [teacher, content, question])
            self.conn.commit()

    def add_sc(self, student, course):
        with self as cursor:
            cursor.execute("insert into sc values(%s, %s)", [student, course])
            self.conn.commit()

    def add_score(self, student, course, score):
        with self as cursor:
            cursor.execute("update sc set score = %s where Sid = %s and Cid = %s", [score, student, course])
            self.conn.commit()

    def add_tc(self, teacher, course):
        with self as cursor:
            cursor.execute("insert into tc values(%s, %s)", [teacher, course])
            self.conn.commit()

    def add_un(self, notice, user):
        with self as cursor:
            cursor.execute("insert into un values(%s, %s)", [notice, user])
            self.conn.commit()

    def add_cn(self, notice, course):
        with self as cursor:
            cursor.execute("insert into cn values(%s, %s)", [notice, course])
            self.conn.commit()

    def del_student(self, id):
        with self as cursor:
            cursor.execute("delete from user where id = %s", [id])
            cursor.execute("delete from student where Sid = %s", [id])
            self.conn.commit()

    def del_teacher(self, id):
        with self as cursor:
            cursor.execute("delete from user where id = %s", [id])
            cursor.execute("delete from teacher where Tid = %s", [id])
            self.conn.commit()

    def del_course(self, id):
        with self as cursor:
            cursor.execute("delete from course where Cid = %s", [id])
            self.conn.commit()

    def del_notice(self, id):
        with self as cursor:
            cursor.execute("delete from notice where Nid = %s", [id])
            self.conn.commit()

    def del_announce(self, id):
        with self as cursor:
            cursor.execute("delete from announce where Aid = %s", [id])
            self.conn.commit()

    def del_question(self, id):
        with self as cursor:
            cursor.execute("delete from question where Qid = %s", [id])
            self.conn.commit()

    def del_sc(self, student, course):
        with self as cursor:
            cursor.execute("delete from sc where Sid = %s and Cid = %s", [student, course])
            self.conn.commit()

    def del_tc(self, teacher, course):
        with self as cursor:
            cursor.execute("delete from tc where Tid = %s and Cid = %s", [teacher, course])
            self.conn.commit()

    def del_un(self, notice, user):
        with self as cursor:
            cursor.execute("delete from un where Nid = %s and id = %s", [notice, user])
            self.conn.commit()

    def del_cn(self, notice, course):
        with self as cursor:
            cursor.execute("delete from cn where Nid = %s and Cid = %s", [notice, course])
            self.conn.commit()

    def get_course_reviews(self, course):
        with self as cursor:
            cursor.execute("select * from review where Cid = %s", [course])
            return cursor.fetchall()

    def get_user_notices(self, id):
        with self as cursor:
            cursor.execute("select * from notice where Nid in (select Nid from un where id = %s)", [id])
            notices = cursor.fetchall()
            cursor.execute("select * from announce")
            announces = cursor.fetchall()
            return notices + announces

    def get_course_notices(self, course):
        with self as cursor:
            cursor.execute("select * from notice where Nid in (select Nid from cn where Cid = %s)", [course])
            return cursor.fetchall()

    def get_course_questions(self, course):
        with self as cursor:
            cursor.execute("select * from question where Cid = %s", [course])
            return cursor.fetchall()

    def get_select_courses(self, student):
        with self as cursor:
            cursor.execute("select * from course where Cid in (select Cid from sc where Sid = %s)", [student])
            return cursor.fetchall()

    def get_teach_courses(self, teacher):
        with self as cursor:
            cursor.execute("select * from course where Cid in (select Cid from tc where Tid = %s)", [teacher])
            return cursor.fetchall()

    def get_course_students(self, course):
        with self as cursor:
            cursor.execute("select * from student where Sid in (select Sid from sc where Cid = %s)", [course])
            return cursor.fetchall()

# data = cursor.fetchone()
# cursor.execute('SELECT * FROM tablename')
# result = cursor.fetchall()
