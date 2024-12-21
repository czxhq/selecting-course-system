from django.http import JsonResponse
import json
import db  # 导入数据库类


def change_password(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('id')
        old_password = body.get('oldPassword')
        new_password = body.get('newPassword')

        # 调用db.py中的接口函数验证旧密码
        stored_password = db.get_user_password(user_id)
        if stored_password and stored_password == old_password:
            # 调用db.py中的接口函数更新密码
            db.update_user_password(user_id, new_password)
            return JsonResponse({"result": "success"})
        else:
            return JsonResponse({"result": "failed"})
    return JsonResponse({"result": "failed"}, status=400)


def update_student_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        email = body.get('email')
        phone = body.get('phone')
        address = body.get('address')
        db.update_student_profile(id, email, phone, address)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def show_student_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        student = db.get_student_profile(id)
        return JsonResponse({"data": student})
    return JsonResponse({"result": "failed"}, status=400)


def update_teacher_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        email = body.get('email')
        phone = body.get('phone')
        address = body.get('address')
        info = body.get('teacherInfo')
        db.update_teacher_profile(id, email, phone, address, info)
        return JsonResponse({"result": "success"})
    return JsonResponse({"result": "failed"}, status=400)


def show_teacher_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        teacher = db.get_teacher_profile(id)
        return JsonResponse({"data": teacher})
    return JsonResponse({"result": "failed"}, status=400)
