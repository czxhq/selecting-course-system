# login/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import db  # 导入数据库类


def student_login(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('id')
        password = body.get('password')

        # 调用db.py中的接口函数验证用户密码
        stored_password = db.get_student_password(user_id)
        if stored_password and stored_password == password:
            return JsonResponse({"result": "success"})
        else:
            return JsonResponse({"result": "failed"})
    return JsonResponse({"result": "failed"}, status=400)
