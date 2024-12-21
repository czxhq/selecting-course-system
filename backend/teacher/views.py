from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import db
import pandas as pd
from django.http import HttpResponse

def enroll_students(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')

        students = db.enroll_student(course_id)
        student_list = []
        for student in students:
            student_list.append({
                "id": student[0],
                "name": student[1]
            })

        return JsonResponse({"data": student_list})
    return JsonResponse({"result": "failed"}, status=400)



def parse_course_time(course_time):
    # 解析课程时间格式
    day, period, weeks = course_time.split(' ')
    weekday = int(day)  # 星期几
    start_period, end_period = map(int, period.split('-'))  # 节次区间
    start_week, end_week = map(int, weeks.split('-'))  # 周次区间
    return weekday, start_period, end_period, start_week, end_week


def is_conflicting(course1, course2):
    # 解析两门课的时间
    weekday1, start_period1, end_period1, start_week1, end_week1 = parse_course_time(course1)
    weekday2, start_period2, end_period2, start_week2, end_week2 = parse_course_time(course2)

    # 判断是否在同一天
    if weekday1 != weekday2:
        return False

    # 判断是否在相同节次区间
    if not (end_period1 < start_period2 or end_period2 < start_period1):
        # 判断是否在相同周次区间
        if not (end_week1 < start_week2 or end_week2 < start_week1):
            return True

    return False

def publish_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_name = body.get('courseName')
        time = '@'.join(body.get('time'))
        location = body.get('location')
        capacity = body.get('capacity')
        type = body.get('type')
        category = body.get('category')
        course_details = body.get('courseDetails')
        teacher = body.get('teacherId')
        credits = body.get('credits')

        courses = db.get_teacher_courses(teacher)
        course_times = set()
        for course in courses:
            for tmp in course[2].split('@'):
                course_times.add(tmp)

        for single_time in body.get('time'):
            for course_time in course_times:
                if is_conflicting(single_time, course_time):
                    return JsonResponse({"result": "failed"}, status=200)

        # 创建课程
        db.publish_course(teacher, course_name, credits, time, location, capacity, type, category, course_details)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def publish_notice(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        course_id = body.get('courseId')
        title = body.get('title')
        content = body.get('content')

        # 创建通知
        db.publish_course_notice(course_id, title, content)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def alter_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        teacher_id = body.get('teacherId')
        course_id = body.get('courseId')
        course_name = body.get('courseName')
        time = '@'.join(body.get('time'))
        location = body.get('location')
        capacity = body.get('capacity')
        type = body.get('type')
        category = body.get('category')
        course_details = body.get('courseDetails')
        credits = body.get('credits')

        courses = db.get_teacher_courses(teacher_id)
        course_times = set()
        for course in courses:
            if course[0] == int(course_id):
                continue
            for tmp in course[2].split('@'):
                course_times.add(tmp)

        for single_time in body.get('time'):
            for course_time in course_times:
                if is_conflicting(single_time, course_time):
                    return JsonResponse({"result": "failed"}, status=200)
                
        # 修改课程
        db.alter_course(course_id, course_name, credits, time, location, capacity, type, category, course_details)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def delete_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')

        db.delete_course(course_id)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def answer_question(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        question_id = body.get('id')
        answer = body.get('answer')

        db.answer_question(question_id, answer)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def get_questions(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')

        questions = db.get_questions(course_id)

        question_list = []
        for question in questions:
            question_list.append({
                "id": question[0],
                "question": question[1]
            })

        return JsonResponse({"result": question_list})
    return JsonResponse({"result": "failed"}, status=400)

def export_students(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body.get('courseId')

        students = db.export_student(course_id)
        student_id = []
        student_name = []
        student_major = []
        student_phone = []
        student_email = []
        for student in students:
            student_id.append(student[0])
            student_name.append(student[1])
            student_major.append(student[2])
            student_phone.append(student[3])
            student_email.append(student[4])
        
        data = {
            "学号": student_id,
            "姓名": student_name,
            "专业": student_major,
            "电话": student_phone,
            "邮箱": student_email
        }

        df = pd.DataFrame(data)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="stu_info_{course_id}.xlsx"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    return JsonResponse({"result": "failed"}, status=400)