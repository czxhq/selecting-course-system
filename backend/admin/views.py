from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User

import db
import pandas as pd
from django.http import HttpResponse

def import_batch_student(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        df = pd.read_excel(uploaded_file)
        result = df[['学号', '姓名', '专业']].values.tolist()
        for student in result:
            major = db.get_major_id(student[2])
            if major is None:
                return JsonResponse({"result": "failed"}, status=200)
            db.add_student(student[0], student[1], major)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)

def import_batch_teacher(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        df = pd.read_excel(uploaded_file)
        result = df[['教师号', '姓名']].values.tolist()
        for teacher in result:
            db.add_teacher(teacher[0], teacher[1])
        return JsonResponse({"result": "success"})

def reset_password(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_type = body.get('type')  # 0表示学生，1表示教师
        user_id = body.get('id')

        try:
            db.reset_user_password(user_id)
            return JsonResponse({"result": "success"})
        except User.DoesNotExist:
            return JsonResponse({"result": "failed"})
    return JsonResponse({"result": "failed"}, status=400)


def get_all_students(request):
    if request.method == 'POST':
        students = db.get_all_students()
        data = []
        for student in students:
            data.append({
                "Id": str(student[0]),
                "name": student[1],
                "major": student[2]
            })

        return JsonResponse({"data": data})
    return JsonResponse({"result": "failed"}, status=400)


def get_all_teachers(request):
    if request.method == 'POST':
        teachers = db.get_all_teachers()
        data = []
        for teacher in teachers:
            data.append({
                "Id": teacher[0],
                "name": teacher[1]
            })

        return JsonResponse({"data": data})
    return JsonResponse({"result": "failed"}, status=400)


def search(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        query = body.get('query')  # 0表示学生，1表示教师
        type = int(body.get('type'))
        by = int(body.get('by'))

        if by == 0:
            if type == 0:
                users = db.search_student_name(query)
            else:
                users = db.search_teacher_name(query)
        else:
            if type == 0:
                users = db.search_student_id(query)
            else:
                users = db.search_teacher_id(query)

        data = []
        for user in users:
            data.append({
                "Id": user[0],
                "name": user[1]
            })

        return JsonResponse({"data": data})
    return JsonResponse({"result": "failed"}, status=400)


def publish_notifications(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        title = body.get('title')
        content = body.get('content')

        db.add_announce(title, content)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def get_notifications(request):
    if request.method == 'POST':
        announces = db.get_announces()
        messages = []
        for announce in announces:
            messages.append({
                "title": announce[1],
                "date": announce[2],
                "content": announce[3]
            })

        return JsonResponse({"data": {"messages": messages}})
    return JsonResponse({"result": "failed"}, status=400)


def import_student(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('id')
        student_name = body.get('name')
        major = db.get_major_id(body.get('major'))
        if major is None:
            return JsonResponse({"result": "failed"}, status=200)
        db.add_student(student_id, student_name, major)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def import_teacher(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        teacher_id = body.get('id')
        teacher_name = body.get('name')
        db.add_teacher(teacher_id, teacher_name)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def delete_teacher(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        teacher_id = body.get('id')
        db.del_teacher(teacher_id)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def delete_student(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student_id = body.get('id')
        db.del_student(student_id)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)

def add_major(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        csum = body.get('csum')
        esum = body.get('esum')
        gmsum = body.get('gmsum')
        cmsum = body.get('cmsum')
        cgsum = body.get('cgsum')
        gsum = body.get('gsum')
        db.add_major(name, csum, esum, gmsum, cmsum, cgsum, gsum)
        
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)

def get_majors(request):
    if request.method == 'POST':
        majors = db.get_majors()
        data = []
        for major in majors:
            data.append({
                "name": major[1],
                "csum": major[2],
                "esum": major[3],
                "gmsum": major[4],
                "cmsum": major[5],
                "cgsum": major[6],
                "gsum": major[7]
            })

        return JsonResponse({"majors": data})
    return JsonResponse({"result": "failed"}, status=400)

def alter_major(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        csum = body.get('csum')
        esum = body.get('esum')
        gmsum = body.get('gmsum')
        cmsum = body.get('cmsum')
        cgsum = body.get('cgsum')
        gsum = body.get('gsum')
        db.alter_major(name, csum, esum, gmsum, cmsum, cgsum, gsum)
        
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)

def export_students(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        students = db.export_admin_students()
        id = []
        name = []
        gender = []
        major = []
        phone = []
        email = []
        address = []
        for student in students:
            id.append(student[0])
            name.append(student[1])
            gender.append(student[2])
            major.append(student[3])
            phone.append(student[4])
            email.append(student[5])
            address.append(student[6])
        
        data = {
            "学号": id,
            "姓名": name,
            "性别": gender,
            "专业": major,
            "电话": phone,
            "邮箱": email,
            "地址": address
        }
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="student_infos.xlsx"'
    
    # 将 DataFrame 写入 Excel 文件并返回响应
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    return JsonResponse({"result": "failed"}, status=400)

def export_teachers(request):
    if request.method == 'POST':
        teachers = db.export_admin_teachers()
        id = []
        name = []
        gender = []
        phone = []
        email = []
        address = []
        intro = []
        for teacher in teachers:
            id.append(teacher[0])
            name.append(teacher[1])
            gender.append(teacher[2])
            phone.append(teacher[3])
            email.append(teacher[4])
            address.append(teacher[5])
            intro.append(teacher[6])
        
        data = {
            "学号": id,
            "姓名": name,
            "性别": gender,
            "电话": phone,
            "邮箱": email,
            "地址": address,
            "简介": intro
        }
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="teacher_infos.xlsx"'
    
    # 将 DataFrame 写入 Excel 文件并返回响应
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    return JsonResponse({"result": "failed"}, status=400)
