# courses/views.py

from django.http import JsonResponse
import json

import db

from functools import lru_cache
from collections import defaultdict


@lru_cache(maxsize=None)
def parse_course_time(course_time):
    """
    解析课程时间格式
    返回一个元组 (weekday, start_period, end_period, start_week, end_week)
    """
    day, period, weeks = course_time.split(' ')
    weekday = int(day)  # 星期几
    start_period, end_period = map(int, period.split('-'))  # 节次区间
    start_week, end_week = map(int, weeks.split('-'))  # 周次区间
    return weekday, start_period, end_period, start_week, end_week


def is_conflicting(course1, course2):
    """
    判断两门课程是否存在时间冲突
    course1 和 course2 是时间字符串，如 "1 1-2 3-4"
    """
    weekday1, start_p1, end_p1, start_w1, end_w1 = parse_course_time(course1)
    weekday2, start_p2, end_p2, start_w2, end_w2 = parse_course_time(course2)

    # 判断是否在同一天
    if weekday1 != weekday2:
        return False

    # 判断节次是否有重叠
    if end_p1 < start_p2 or end_p2 < start_p1:
        return False

    # 判断周次是否有重叠
    if end_w1 < start_w2 or end_w2 < start_w1:
        return False

    return True


def hide_conflict_courses(select_courses, courses):
    """
    隐藏与学生已选课程时间冲突的课程
    """
    # 按星期分组学生的课程时间
    student_course_times_by_weekday = {}
    for course in select_courses:
        for time in course[3].split('@'):
            weekday, start_p, end_p, start_w, end_w = parse_course_time(time)
            if weekday not in student_course_times_by_weekday:
                student_course_times_by_weekday[weekday] = []
            student_course_times_by_weekday[weekday].append((start_p, end_p, start_w, end_w))

    # 使用集合存储需要隐藏的课程
    hide_courses = set()

    for course in courses:
        course_times = course[3].split('@')
        conflict_found = False  # 标记是否存在冲突
        for time in course_times:
            weekday, start_p, end_p, start_w, end_w = parse_course_time(time)
            if weekday in student_course_times_by_weekday:
                for sc_start_p, sc_end_p, sc_start_w, sc_end_w in student_course_times_by_weekday[weekday]:
                    # 判断节次是否重叠
                    if not (end_p < sc_start_p or sc_end_p < start_p):
                        # 判断周次是否重叠
                        if not (end_w < sc_start_w or sc_end_w < start_w):
                            hide_courses.add(course)
                            conflict_found = True
                            break  # 退出当前课程的时间检查
                if conflict_found:
                    break  # 退出当前课程的所有时间检查

    # 过滤掉需要隐藏的课程
    filtered_courses = [course for course in courses if course not in hide_courses]

    return filtered_courses

def search_courses(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')
        query = body.get('query')
        search_type = int(body.get('type'))  # 0表示按课程名，1表示按教师名
        hide_conflict = body.get('hide-conflict')

        if search_type == 0:
            courses = db.search_courses_by_name(query)
        else:
            courses = db.search_courses_by_teacher(query)

        select_courses = db.get_courses(student_id)
        if hide_conflict:
            courses = hide_conflict_courses(select_courses, courses)
        
        courses = [list(course) for course in courses]
        selected_ids = {ele[0] for ele in select_courses}
        results = {}
        for course in courses:
            if course[0] in results:
                results[course[0]][8] += ', ' + course[8]
            else:
                results[course[0]] = course

        course_list = []
        for course in results.values():
            course_info = {
                "courseId": course[0],
                "courseName": course[1],
                "teacher": course[8],
                "location": course[2],
                "time": course[3].split('@'),
                "type": course[4],
                "category": course[5],
                "capacity": course[6],  # 总容量/已选人数
                "credits": course[7],
                "isSelect": course[0] in selected_ids
            }
            course_list.append(course_info)

        return JsonResponse({"courses": course_list})
    return JsonResponse({"result": "failed"}, status=400)


def get_course_details(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')

        # 获取课程基本信息
        course_info, reviews, questions = db.get_course_details(course_id)

        if not course_info:
            return JsonResponse({"result": "failed", "message": "课程不存在"})

        # 获取课程评价
        course_reviews = []
        for review in reviews:
            course_reviews.append({
                "student": review[0],
                "rating": review[1],
                "comment": review[2]
            })

        # 获取课程问答
        course_qna = []
        for question in questions:
            answer = question[6] if question[6] else "暂无回答"
            course_qna.append({
                "id": question[0],
                "question": question[5],
                "answer": answer
            })

        course = course_info[0]
        teacher = ""
        for t in course_info:
            if teacher == "":
                teacher += t[9]
            else:
                teacher += ', ' + t[9]
        
        course_details = {
            "courseName": course[1],
            "teacher": teacher,
            "location": course[2],
            "credits": course[3],
            "time": course[4].split('@'),
            "type": course[5],
            "category": course[6],
            "capacity": course[7],  # 总容量/已选人数
            "courseDetails": course[8],
            "teacherInfo": course[10],  # 如果有教师信息，可通过 Teacher 表获取
            "courseReview": course_reviews,
            "courseQnA": course_qna
        }

        return JsonResponse({"data": course_details})
    return JsonResponse({"result": "failed"}, status=400)


def cancel_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')
        course_id = body.get('courseId')

        # 取消选课
        db.cancel_course(student_id, course_id)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def all_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        student_id = body.get('studentId')
        hide_conflict = body.get('hide-conflict')
        courses = db.get_all_courses()

        select_courses = db.get_courses(student_id)
        if hide_conflict:
            courses = hide_conflict_courses(select_courses, courses)

        courses = [list(course) for course in courses]
        selected_ids = {ele[0] for ele in select_courses}
        results = {}
        for course in courses:
            if course[0] in results:
                results[course[0]][8] += ', ' + course[8]
            else:
                results[course[0]] = course
            
        course_list = []
        for course in results.values():
            course_list.append({
                "courseId": course[0],
                "courseName": course[1],
                "teacher": course[8],
                "location": course[2],
                "time": course[3].split('@'),
                "type": course[4],
                "category": course[5],
                "capacity": course[6],
                "isSelect": course[0] in selected_ids,
                "credits": course[7]
            })

        return JsonResponse({"courses": course_list})
    return JsonResponse({"result": "failed"}, status=400)


def publish_question(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')
        question = body.get('question')

        # 提问
        db.publish_question(course_id, question)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def enroll_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')
        course_id = body.get('courseId')

        courses, time = db.enroll_course_info(student_id, course_id)
        selected_times = set()
        for course in courses:
            for t in course[0].split('@'):
                selected_times.add(t)

        for t in time.split('@'):
            for s in selected_times:
                if is_conflicting(s, t):
                    return JsonResponse({"result": "failed", "message": "时间冲突"})

 
        if db.enroll_course(student_id, course_id):
            return JsonResponse({"result": "success"})
        else:
            return JsonResponse({"result": "failed"})
    return JsonResponse({"result": "failed"}, status=400)

def add_review(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')
        course_id = body.get('courseId')
        rating = body.get('rating')
        comment = body.get('comment')

        db.add_review(student_id, course_id, rating, comment)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)
