create table User
(
    id       int primary key,
    type     tinyint      not null,
    name     char(20),
    gender   char(10),
    college  char(20),
    password varchar(255) not null
);

create table Major
(
    Mid     int primary key auto_increment,
    Mname   char(30)     not null,
    credits float        not null,
    courses varchar(255) not null
);

create table Student
(
    Sid   int primary key,
    grade char(20),
    class char(20),
    phone char(20),
    Mid   int,
    FOREIGN KEY (Sid) REFERENCES User (id),
    FOREIGN KEY (Mid) REFERENCES Major (Mid)
);

create table Teacher
(
    Tid   int primary key,
    title char(20),
    email char(30),
    intro varchar(255),
    FOREIGN KEY (Tid) REFERENCES User (id)
);

create table Course
(
    Cid        int primary key,
    Cname      char(20) not null,
    credits    float    not null,
    pre_course varchar(255),
    capacity   int      not null,
    type       char(5)  not null,
    category   char(5)  not null,
    semester   char(20) not null,
    date       char(20) not null,
    hours      smallint not null,
    room       char(10) not null
);

create table Review
(
    Rid     int primary key auto_increment,
    Sid     int      not null,
    Cid     int      not null,
    rate    smallint not null,
    date    datetime not null default current_timestamp,
    content varchar(255),
    FOREIGN KEY (Sid) REFERENCES Student (Sid),
    FOREIGN KEY (Cid) REFERENCES Course (Cid)
);

create table Notice
(
    Nid     int primary key auto_increment,
    title   char(40) not null,
    sender  int      not null,
    date    datetime not null default current_timestamp,
    content varchar(255),
    FOREIGN KEY (sender) REFERENCES User (id)
);

create table Announce
(
    Aid     int primary key auto_increment,
    title   char(40) not null,
    date    datetime not null default current_timestamp,
    content varchar(255)
);

create table Question
(
    Qid     int primary key auto_increment,
    Sid     int          not null,
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


