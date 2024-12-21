create table User
(
    id       int primary key,
    type     tinyint  not null,
    name     char(20) not null default '暂无',
    gender   char(10)          default '暂无',
    college  char(20)          default '暂无',
    phone    char(20)          default '暂无',
    email    char(30)          default '暂无',
    address  varchar(255)      default '暂无',
    password varchar(255)      default '88888888'
);

create table Major
(
    Mid   int primary key auto_increment,
    Mname char(30) not null,
    csum  float    not null,
    esum  float    not null,
    gmsum float    not null,
    cmsum float    not null,
    cgsum float    not null,
    gsum  float    not null
);

create table Student
(
    Sid   int primary key,
    grade char(20) default '暂无',
    class char(20) default '暂无',
    Mid   int,
    FOREIGN KEY (Sid) REFERENCES User (id),
    FOREIGN KEY (Mid) REFERENCES Major (Mid)
);

create table Teacher
(
    Tid   int primary key,
    title char(20)     default '暂无',
    intro varchar(255) default '暂无',
    FOREIGN KEY (Tid) REFERENCES User (id)
);

create table Course
(
    Cid        int primary key auto_increment,
    Cname      char(20)  not null default '暂无',
    credits    float     not null default 0,
    pre_course varchar(255)       default '无',
    capacity   int       not null default 0,
    type       char(5)   not null default '暂无',
    category   char(5)   not null default '暂无',
    semester   char(20)  not null default '暂无',
    date       char(255) not null default '暂无',
    hours      smallint  not null default 0,
    room       char(10)  not null default '暂无',
    detail     varchar(255)       default '暂无'
);

create table Review
(
    Rid     int primary key auto_increment,
    Sid     int      not null,
    Cid     int      not null,
    rate    smallint not null,
    date    datetime not null default current_timestamp,
    content varchar(255)      default '无',
    FOREIGN KEY (Sid) REFERENCES Student (Sid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

create table Notice
(
    Nid     int primary key auto_increment,
    title   char(40) not null,
    sender  int,
    date    datetime not null default current_timestamp,
    content varchar(255),
    FOREIGN KEY (sender) REFERENCES User (id)
);

create table Announce
(
    Aid     int primary key auto_increment,
    title   char(40) not null,
    date    datetime not null default current_timestamp,
    content varchar(255)      default '无'
);

create table Question
(
    Qid     int primary key auto_increment,
    Sid     int,
    Tid     int,
    Cid     int          not null,
    date    datetime     not null default current_timestamp,
    content varchar(255) not null,
    answer  varchar(255),
    FOREIGN KEY (Sid) REFERENCES Student (Sid),
    FOREIGN KEY (Tid) REFERENCES Teacher (Tid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

create table SC
(
    Sid   int not null,
    Cid   int not null,
    score int,
    PRIMARY KEY (Sid, Cid),
    FOREIGN KEY (Sid) REFERENCES Student (Sid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

create table TC
(
    Tid int not null,
    Cid int not null,
    PRIMARY KEY (Tid, Cid),
    FOREIGN KEY (Tid) REFERENCES Teacher (Tid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

create table UN
(
    Nid int not null,
    id  int not null,
    PRIMARY KEY (Nid, id),
    FOREIGN KEY (Nid) REFERENCES Notice (Nid),
    FOREIGN KEY (id) REFERENCES User (id)
);

create table CN
(
    Nid int not null,
    Cid int not null,
    PRIMARY KEY (Nid, Cid),
    FOREIGN KEY (Nid) REFERENCES Notice (Nid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

# DELIMITER $$
# CREATE TRIGGER before_delete_course
#     BEFORE DELETE
#     ON Course
#     FOR EACH ROW
# BEGIN
#     DELETE FROM SC WHERE Cid = OLD.Cid;
#     DELETE FROM TC WHERE Cid = OLD.Cid;
#     DELETE FROM CN WHERE Cid = OLD.Cid;
#     DELETE
#     FROM UN
#     WHERE Nid IN (SELECT Nid FROM CN WHERE Cid = OLD.Cid);
#     DELETE FROM Review WHERE Cid = OLD.Cid;
#     DELETE FROM Question WHERE Cid = OLD.Cid;
# END$$
# DELIMITER ;
# 
# CREATE VIEW StudentDetails AS
# SELECT s.Sid,
#        u.name  AS student_name,
#        u.gender,
#        u.college,
#        u.phone,
#        u.email,
#        u.address,
#        s.grade,
#        s.class,
#        m.Mname AS major_name
# FROM Student s
#          JOIN User u ON s.Sid = u.id
#          JOIN Major m ON s.Mid = m.Mid;
# 
# CREATE INDEX idx_user_email ON User (email);
# 
# CREATE INDEX idx_user_type ON User (type);

INSERT INTO User (id, type, name, gender, college, phone, email, address, password)
VALUES (999, 2, 'Admin', 'Female', 'Engineering', '123456', 'alice@example.com', 'Address A', '999'),
       (100, 0, 'Alice', 'Female', 'Engineering', '123456', 'alice@example.com', 'Address A', 'pwd100'),
       (101, 1, 'Bob', 'Male', 'ComputerSci', '234567', 'bob@example.com', 'Address B', 'pwd101'),
       (102, 0, 'Carol', 'Female', 'Mathematics', '345678', 'carol@example.com', 'Address C', 'pwd102'),
       (103, 1, 'David', 'Male', 'ComputerSci', '456789', 'david@example.com', 'Address D', 'pwd103'),
       (104, 0, 'Addy', 'Male', 'AdminOffice', '000000', 'admin@example.com', 'Admin Address', 'adminpw'),
       (105, 0, 'Eve', 'Female', 'Engineering', '567890', 'eve@example.com', 'Address E', 'pwd105'),
       (106, 0, 'Frank', 'Male', 'ComputerSci', '678901', 'frank@example.com', 'Address F', 'pwd106'),
       (107, 1, 'Grace', 'Female', 'Engineering', '789012', 'grace@example.com', 'Address G', 'pwd107'),
       (108, 0, 'Heidi', 'Female', 'Mathematics', '890123', 'heidi@example.com', 'Address H', 'pwd108'),
       (109, 1, 'Ivan', 'Male', 'Literature', '901234', 'ivan@example.com', 'Address I', 'pwd109'),
       (110, 0, 'Jack', 'Male', 'ComputerSci', '012345', 'jack@example.com', 'Address J', 'pwd110'),
       (111, 0, 'Kate', 'Female', 'Mathematics', '111111', 'kate@example.com', 'Address K', 'pwd111'),
       (112, 0, 'Leo', 'Male', 'Literature', '222222', 'leo@example.com', 'Address L', 'pwd112'),
       (113, 0, 'Mia', 'Female', 'ComputerSci', '333333', 'mia@example.com', 'Address M', 'pwd113'),
       (114, 0, 'Nick', 'Male', 'Mathematics', '444444', 'nick@example.com', 'Address N', 'pwd114'),
       (115, 1, 'Oscar', 'Male', 'Economics', '555555', 'oscar@example.com', 'Address O', 'pwd115'),
       (116, 1, 'Pat', 'Female', 'History', '666666', 'pat@example.com', 'Address P', 'pwd116'),
       (117, 1, 'Quinn', 'Male', 'Biology', '777777', 'quinn@example.com', 'Address Q', 'pwd117'),
       (118, 1, 'Rose', 'Female', 'Physics', '888888', 'rose@example.com', 'Address R', 'pwd118'),
       (119, 1, 'Sam', 'Male', 'Philosophy', '999999', 'sam@example.com', 'Address S', 'pwd119'),
       (120, 1, 'Tina', 'Female', 'Chemistry', '101010', 'tina@example.com', 'Address T', 'pwd120'),
       (121, 1, '张伟', '男', '计算机学院', '13800001121', 'zhangwei@example.com', '北京市海淀区', 'password1'),
       (122, 1, '李娜', '女', '数学学院', '13800001122', 'lina@example.com', '上海市浦东新区', 'password2'),
       (123, 1, '王强', '男', '物理学院', '13800001123', 'wangqiang@example.com', '广州市天河区', 'password3'),
       (124, 1, '赵敏', '女', '化学学院', '13800001124', 'zhaomin@example.com', '深圳市南山区', 'password4'),
       (125, 1, '刘洋', '男', '经济学院', '13800001125', 'liuyang@example.com', '成都市武侯区', 'password5'),
       (126, 1, '陈静', '女', '历史学院', '13800001126', 'chenjing@example.com', '杭州市西湖区', 'password6'),
       (127, 1, '孙磊', '男', '生物学院', '13800001127', 'sunlei@example.com', '南京市鼓楼区', 'password7'),
       (128, 1, '周婷', '女', '哲学学院', '13800001128', 'zhouting@example.com', '重庆市渝中区', 'password8'),
       (129, 1, '吴刚', '男', '工程学院', '13800001129', 'wugang@example.com', '武汉市武昌区', 'password9'),
       (130, 1, '郑丽', '女', '文学学院', '13800001130', 'zhengli@example.com', '西安市碑林区', 'password10');

INSERT INTO Major (Mname, csum, esum, gmsum, cmsum, cgsum, gsum)
VALUES ('Computer Science', 120.0, 100, 100, 100, 100, 100),
       ('Mathematics', 100.0, 90, 90, 90, 90, 90),
       ('Literature', 90.0, 80, 80, 80, 80, 80),
       ('Physics', 110.0, 70, 70, 70, 70, 70),
       ('Chemistry', 100.0, 60, 60, 60, 60, 60),
       ('Biology', 110.0, 50, 50, 50, 50, 50),
       ('Economics', 90.0, 80, 80, 80, 80, 80),
       ('History', 80.0, 90, 90, 90, 90, 90),
       ('Music', 70.0, 90, 90, 90, 90, 90),
       ('Philosophy', 60.0, 100, 100, 100, 100, 100);

INSERT INTO Student (Sid, grade, class, Mid)
VALUES (100, '2024', 'ClassA', 1),
       (102, '2024', 'ClassB', 2),
       (104, '2024', 'ClassC', 3),
       (105, '2024', 'ClassA', 1),
       (106, '2024', 'ClassB', 2),
       (108, '2024', 'ClassC', 3),
       (110, '2025', 'ClassD', 4),
       (111, '2025', 'ClassD', 5),
       (112, '2025', 'ClassE', 6),
       (113, '2025', 'ClassF', 7),
       (114, '2025', 'ClassG', 8);

INSERT INTO Teacher (Tid, title, intro)
VALUES (101, 'Professor', 'Expert in Computer Science'),
       (103, 'Associate Prof', 'Focus on Mathematics'),
       (107, 'Lecturer', 'Engineering basics'),
       (109, 'Assistant Prof', 'Literature critique'),
       (115, 'Professor', 'Economics guru'),
       (116, 'Senior Lecturer', 'History buff'),
       (117, 'Professor', 'Biology researcher'),
       (118, 'Professor', 'Physics theorist'),
       (119, 'Assoc Prof', 'Philosophy and ethics'),
       (120, 'Lecturer', 'Chemistry fundamentals'),
       (121, 'Professor', '人工智能专家'),
       (122, 'Associate Prof', '代数与几何研究'),
       (123, 'Lecturer', '量子物理研究'),
       (124, 'Assistant Prof', '有机化学专长'),
       (125, 'Professor', '宏观经济学'),
       (126, 'Senior Lecturer', '中国历史研究'),
       (127, 'Professor', '分子生物学'),
       (128, 'Assoc Prof', '伦理学与哲学'),
       (129, 'Lecturer', '土木工程'),
       (130, 'Professor', '现代文学研究');

INSERT INTO Course (Cid, Cname, credits, pre_course, capacity, type, category, semester, date, hours, room, detail)
VALUES (201, 'CS101', 3.0, '无', 50, '必修', '一般专业类', 'Fall2024', '1 1-2 1-3', 45, 'R101',
        'Introduction to Programming'),
       (202, 'CS102', 4.0, 'CS101', 40, '必修', '核心专业类', 'Spring2025', '2 1-2 1-3', 60, 'R102', 'Data Structures'),
       (203, 'MATH101', 3.0, '无', 50, '选修', '一般专业类', 'Fall2024', '3 1-2 1-3', 45, 'M201', 'Calculus I'),
       (204, 'MATH102', 4.0, 'MATH101', 40, '必修', '核心专业类', 'Spring2025', '4 1-2 1-3', 60, 'M202',
        'Advanced Calculus'),
       (205, 'PHYS101', 3.0, '无', 50, '选修', '核心通识类', 'Fall2024', '5 1-2 1-4', 45, 'P101', 'Intro to Physics'),
       (206, 'CHEM101', 3.0, '无', 50, '必修', '一般通识类', 'Fall2024', '5 5-6 1-4', 45, 'C101', 'Intro to Chemistry'),
       (207, 'BIO101', 3.0, '无', 50, '选修', '核心通识类', 'Fall2024', '4 11-12 1-4', 45, 'B101', 'Intro to Biology'),
       (208, 'ECO101', 3.0, '无', 50, '必修', '一般通识类', 'Fall2024', '3 7-8 1-15', 45, 'E101',
        'Principles of Economics'),
       (209, 'HIS101', 3.0, '无', 50, '选修', '核心通识类', 'Fall2024', '4 6-7 1-10', 45, 'H101', 'World History I'),
       (210, 'PHI101', 3.0, '无', 50, '选修', '一般通识类', 'Fall2024', '2 4-5 1-10', 45, 'PH101',
        'Intro to Philosophy'),
       (211, 'ENG101', 3.0, '无', 50, '选修', '核心通识类', 'Fall2024', '1 1-2 1-10', 45, 'E102',
        'Introduction to Engineering'),
       (212, 'BIO102', 4.0, 'BIO101', 40, '必修', '核心专业类', 'Spring2025', '2 3-4 1-10', 60, 'B102',
        'Advanced Biology'),
       (213, 'CHEM102', 3.0, 'CHEM101', 50, '选修', '一般通识类', 'Fall2024', '3 5-6 1-10', 45, 'C102',
        'Organic Chemistry'),
       (214, 'PHIL102', 3.0, 'PHI101', 50, '选修', '一般通识类', 'Fall2024', '4 7-8 1-10', 45, 'PH102',
        'Advanced Philosophy'),
       (215, 'ECON102', 3.0, 'ECO101', 50, '必修', '一般通识类', 'Fall2024', '5 9-10 1-10', 45, 'E102',
        'Microeconomics'),
       (216, 'HIST102', 3.0, 'HIS101', 50, '选修', '核心通识类', 'Fall2024', '6 11-12 1-10', 45, 'H102',
        'Modern History'),
       (217, 'MATH103', 4.0, 'MATH102', 40, '必修', '核心专业类', 'Spring2025', '1 1-2 1-10', 60, 'M203',
        'Linear Algebra'),
       (218, 'CS103', 3.0, 'CS102', 50, '选修', '一般专业类', 'Fall2024', '2 3-4 1-10', 45, 'R103', 'Algorithms'),
       (219, 'PHYS102', 4.0, 'PHYS101', 40, '必修', '核心专业类', 'Spring2025', '3 5-6 1-10', 60, 'P102',
        'Electromagnetism'),
       (220, 'ENG102', 3.0, 'ENG101', 50, '选修', '核心通识类', 'Fall2024', '4 7-8 1-10', 45, 'E103', 'Thermodynamics'),
       (221, 'BIO103', 3.0, 'BIO102', 50, '选修', '核心专业类', 'Fall2024', '5 9-10 1-10', 45, 'B103', 'Genetics'),
       (222, 'CHEM103', 4.0, 'CHEM102', 40, '必修', '核心专业类', 'Spring2025', '6 11-12 1-10', 60, 'C103',
        'Physical Chemistry'),
       (223, 'PHIL103', 3.0, 'PHIL102', 50, '选修', '一般通识类', 'Fall2024', '1 1-2 1-10', 45, 'PH103', 'Metaphysics'),
       (224, 'ECON103', 3.0, 'ECON102', 50, '选修', '一般通识类', 'Fall2024', '2 3-4 1-10', 45, 'E104',
        'Macroeconomics'),
       (225, 'HIST103', 4.0, 'HIST102', 40, '必修', '核心通识类', 'Spring2025', '3 5-6 1-10', 60, 'H103',
        'World War II'),
       (226, 'MATH104', 3.0, 'MATH103', 50, '选修', '一般专业类', 'Fall2024', '4 7-8 1-10', 45, 'M204',
        'Differential Equations'),
       (227, 'CS104', 4.0, 'CS103', 40, '必修', '核心专业类', 'Spring2025', '5 9-10 1-10', 60, 'R104',
        'Operating Systems'),
       (228, 'PHYS103', 3.0, 'PHYS102', 50, '选修', '一般专业类', 'Fall2024', '6 11-12 1-10', 45, 'P103',
        'Quantum Mechanics'),
       (229, 'ENG103', 4.0, 'ENG102', 40, '必修', '核心通识类', 'Spring2025', '1 1-2 1-10', 60, 'E105',
        'Fluid Mechanics'),
       (230, 'BIO104', 3.0, 'BIO103', 50, '选修', '核心专业类', 'Fall2024', '2 3-4 1-10', 45, 'B104', 'Cell Biology'),
       (231, 'CHEM104', 3.0, 'CHEM103', 50, '选修', '一般通识类', 'Fall2024', '3 5-6 1-10', 45, 'C104',
        'Inorganic Chemistry'),
       (232, 'PHIL104', 4.0, 'PHIL103', 40, '必修', '一般通识类', 'Spring2025', '4 7-8 1-10', 60, 'PH104', 'Logic'),
       (233, 'ECON104', 3.0, 'ECON103', 50, '选修', '一般通识类', 'Fall2024', '5 9-10 1-10', 45, 'E106',
        'International Economics'),
       (234, 'HIST104', 3.0, 'HIST103', 50, '选修', '核心通识类', 'Fall2024', '6 11-12 1-10', 45, 'H104',
        'Ancient Civilizations'),
       (235, 'MATH105', 4.0, 'MATH104', 40, '必修', '核心专业类', 'Spring2025', '1 1-2 1-10', 60, 'M205',
        'Probability Theory'),
       (236, 'CS105', 3.0, 'CS104', 50, '选修', '一般专业类', 'Fall2024', '2 3-4 1-10', 45, 'R105', 'Database Systems'),
       (237, 'PHYS104', 4.0, 'PHYS103', 40, '必修', '核心专业类', 'Spring2025', '3 5-6 1-10', 60, 'P104',
        'Thermodynamics'),
       (238, 'ENG104', 3.0, 'ENG103', 50, '选修', '核心通识类', 'Fall2024', '4 7-8 1-10', 45, 'E106',
        'Structural Engineering'),
       (239, 'BIO105', 3.0, 'BIO104', 50, '选修', '核心专业类', 'Fall2024', '5 9-10 1-10', 45, 'B105', 'Ecology'),
       (240, 'CHEM105', 4.0, 'CHEM104', 40, '必修', '一般通识类', 'Spring2025', '6 11-12 1-10', 60, 'C105',
        'Analytical Chemistry');

INSERT INTO Review (Sid, Cid, rate, content)
VALUES (100, 201, 5, 'Excellent course! Very helpful.'),
       (102, 201, 4, 'Good course, but tough.'),
       (100, 202, 5, 'Challenging but learned a lot.'),
       (105, 201, 3, 'It was okay.'),
       (106, 203, 5, 'Loved it!'),
       (108, 205, 4, 'Physics is interesting.'),
       (110, 206, 3, 'Chemistry is not my favorite.'),
       (111, 207, 5, 'Biology classes are fun.'),
       (112, 208, 4, 'Economics was quite informative.'),
       (113, 209, 4, 'History is always enlightening.'),
       (114, 210, 2, 'Philosophy is hard to understand.');

INSERT INTO Notice (title, sender, content)
VALUES ('System Maintenance', 104, 'System will be down on Sunday'),
       ('New Course Available', 104, 'New elective courses are open for enrollment'),
       ('Holiday Notice', 104, 'Campus closed on holidays'),
       ('Exam Schedule', 104, 'Midterm exams next week'),
       ('Library Notice', 104, 'Library renovation next month'),
       ('Sports Event', 104, 'Annual sports meet on Saturday'),
       ('Workshop Notice', 104, 'Attend the coding workshop'),
       ('Scholarship Info', 104, 'Apply for scholarships'),
       ('Orientation', 104, 'New student orientation'),
       ('Tech Talk', 104, 'Guest lecture on AI');


INSERT INTO Announce (title, content)
VALUES ('Semester Start', 'Welcome to the Fall 2024 semester!'),
       ('Holiday Announcement', 'No classes on National Day holiday'),
       ('Winter Break', 'Winter break starts December 20'),
       ('New Library', 'New library building is open'),
       ('Cultural Festival', 'Cultural fest next month'),
       ('Internship Fair', 'Internship opportunities available'),
       ('Health Checkup', 'Free health checkup on campus'),
       ('Career Counselling', 'Career guidance sessions'),
       ('Study Abroad', 'Opportunities to study abroad'),
       ('Art Exhibition', 'Art exhibitions in gallery');

INSERT INTO Question (Sid, Tid, Cid, content, answer)
VALUES (100, 101, 201, 'When is the final exam?', 'The final exam is scheduled on December 10th'),
       (102, 101, 201, 'Any recommended reading?', 'Read "Intro to Algorithms"'),
       (100, 103, 202, 'When are office hours?', 'Every Tuesday 2-4 PM'),
       (105, 107, 205, 'How to solve problem set 3?', 'Check the lecture notes.'),
       (106, 109, 203, 'What is the final project topic?', 'Research-based essay.'),
       (108, 115, 208, 'Any prerequisites?', 'Basic Econ knowledge'),
       (110, 116, 204, 'Is attendance mandatory?', 'Yes, it counts for 10% grade.'),
       (111, 117, 207, 'Can we form study groups?', 'Certainly.'),
       (112, 118, 210, 'Where to find lecture slides?', 'Posted on the course website.'),
       (113, 119, 209, 'Will there be a field trip?', 'Yes, next month.'),
       (114, 120, 206, 'Lab equipment availability?', 'Provided by the department.');

INSERT INTO SC (Sid, Cid, score)
VALUES (100, 201, 90),
       (102, 203, 85),
       (100, 202, 88),
       (105, 201, 77),
       (106, 202, 89),
       (108, 205, 90),
       (110, 206, 70),
       (111, 207, 95),
       (112, 208, 85),
       (113, 209, 80),
       (114, 210, 60);

INSERT INTO TC (Tid, Cid)
VALUES (101, 201),
       (101, 202),
       (103, 203),
       (107, 205),
       (109, 209),
       (115, 208),
       (116, 209),
       (117, 207),
       (118, 205),
       (119, 210),
       (120, 206),
       (103, 204),
       (121, 211),
       (122, 212),
       (123, 213),
       (124, 214),
       (125, 215),
       (126, 216),
       (127, 217),
       (128, 218),
       (129, 219),
       (130, 220),
       (121, 221),
       (122, 222),
       (123, 223),
       (124, 224),
       (125, 225),
       (126, 226),
       (127, 227),
       (128, 228),
       (129, 229),
       (130, 230),
       (121, 231),
       (122, 232),
       (123, 233),
       (124, 234),
       (125, 235),
       (126, 236),
       (127, 237),
       (128, 238),
       (129, 239),
       (130, 240);

INSERT INTO UN (Nid, id)
VALUES (1, 100),
       (1, 101),
       (2, 102),
       (3, 104),
       (4, 105),
       (5, 106),
       (6, 108),
       (7, 110),
       (8, 111),
       (9, 112);

INSERT INTO CN (Nid, Cid)
VALUES (2, 201),
       (1, 203),
       (3, 204),
       (4, 205),
       (5, 206),
       (6, 207),
       (7, 208),
       (8, 209),
       (9, 210),
       (10, 202);