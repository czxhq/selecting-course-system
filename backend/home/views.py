from django.http import JsonResponse
import json

import db


def get_courses(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        student_id = body.get('studentId')

        # 根据学生ID获取其选修的课程
        courses = db.get_courses(student_id)
        courses = [list(course) for course in courses]
        results = {}
        for course in courses:
            if course[0] in results:
                results[course[0]][4] += ', ' + course[4]
            else:
                results[course[0]] = course

        course_list = []
        for course in results.values():
            course_list.append({
                "courseId": course[0],
                "courseName": course[1],
                "teacher": course[4],
                "location": course[2],
                "time": course[3].split('@'),
            })

        return JsonResponse({"data": {"courses": course_list}})
    return JsonResponse({"result": "failed"}, status=400)


def course_details(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')

        # 根据学生ID获取其选修的课程
        courses = db.course_details(student_id)

        courses = [list(course) for course in courses]
        results = {}
        for course in courses:
            if course[1] in results:
                results[course[1]][9] += ', ' + course[9]
            else:
                results[course[1]] = course

        course_list = []
        for course in results.values():
            course_list.append({
                "courseId": course[1],
                "courseName": course[2],
                "teacher": course[9],
                "location": course[3],
                "time": course[4].split('@'),
                "type": course[5],
                "category": course[6],
                "capacity": course[7],  # 总容量/已选人数
                "credits": course[8],
            })

        return JsonResponse({"courses": course_list})
    return JsonResponse({"result": "failed"}, status=400)

def get_credit_progress(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('studentId')
        major = db.get_major_credits(student_id)
        credits = db.get_student_credits(student_id)

        return JsonResponse({"result": {
            "C": f"{credits[0]}/{major[2]}",
            "E": f"{credits[1]}/{major[3]}",
            "GM": f"{credits[2]}/{major[4]}",
            "CM": f"{credits[3]}/{major[5]}", 
            "CG": f"{credits[4]}/{major[6]}",
            "G": f"{credits[5]}/{major[7]}"
        }})
    return JsonResponse({"result": "failed"}, status=400)


def get_messages(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('id')

        messages = db.get_user_messages(user_id)

        return JsonResponse({"data": {"messages": messages}})
    return JsonResponse({"result": "failed"}, status=400)


def get_teacher_courses(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        teacher_id = body.get('TeacherId')

        courses = db.get_teacher_courses(teacher_id)

        course_list = []

        for course in courses:
            course_list.append({
                "courseId": course[0],
                "courseName": course[1],
                "time": course[2].split('@'),
                "location": course[3]
            })

        return JsonResponse({"data": {"courses": course_list}})
    return JsonResponse({"result": "failed"}, status=400)
