from .models import *
# from .serializers import UserSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime 

@csrf_exempt
def send_email_subject_user(request,pk):
    if request.method == 'GET':
        sub = get_object_or_404(Subject,id=pk)
        users = sub.userdata_set.all()
        out = {'status': 'succsess', 
                'data': {
                    'subject' : sub.__detail__(),
                    'email_list' : [ i.user.email for i in users ]
        }}
        return JsonResponse(out)
    elif request.method == 'POST':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})