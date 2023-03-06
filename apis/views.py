# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
# from .serializers import UserSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime 
from django.conf import settings

# from django.core.mail import send_mail
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from openpyxl import Workbook
from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def handle_users(request):
    if request.method == 'GET':
        user_data = UserData.objects.all()
        if user_data is None :
            return JsonResponse({'status': 'error', 'data': 'Users NOT Found.'})
        else:
            return JsonResponse({'status': 'succsess',
                                 'data' : {
                                    'users' : [ i.__detail__()  for i in user_data ]
                                 }
                                })
    elif request.method == 'POST':
        # create a new user with given data 
        req_user_data = json.loads(request.body)

        new_user = User.objects.create(username=req_user_data['email_id'])
        new_user.email = req_user_data['email_id']
        new_user.save()

        new_user_data = UserData.objects.create(user=new_user)
        new_user_data.first_name = req_user_data['first_name']
        new_user_data.last_name = req_user_data['last_name']
        new_user_data.start_term = Term.objects.get(id=req_user_data['start_term_id'])
        new_user_data.expected_end_term = Term.objects.get(id=req_user_data['expected_end_term_id'])

        for t_id in req_user_data['enrolled_subjects_ids']:
            new_user_data.enrolled_subjects.add(Subject.objects.get(id=t_id))

        new_user_data.save()

        return JsonResponse({'status': 'OK', 'data': 'added user.'})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})

@csrf_exempt
def handle_one_user(request,pk):
    if request.method == 'GET':
        # user_data = UserData.objects.get(user = User.objects.get(id=pk))
        user_data = get_object_or_404(UserData,user=get_object_or_404(User, id = pk))
        # if user_data is None :
        #     return JsonResponse({'status': '404', 'data': 'User NOT Found.'})
        # else:
        # subs = [ { 'id' : i.id, 'name' : i.__detail__() } for i in user_data.enrolled_subjects.all() ]
        return JsonResponse({'status': 'succsess',
                                 'data' : {
                                    'user' : user_data.__detail__(),
                                    # 'start_term' : user_data.start_term.__detail__()
                                 }
                                })
    elif request.method == 'PUT':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})

@csrf_exempt
def handle_user_subject(request,pk):
    if request.method == 'GET':
        # user_data = UserData.objects.get(user = User.objects.get(id=pk))
        user_data = get_object_or_404(UserData,user=get_object_or_404(User, id = pk))
        # if user_data is None :
        #     return JsonResponse({'status': '404', 'data': 'User NOT Found.'})
        # else:
        subs = [ { 'id' : i.id, 'name' : i.__detail__() } for i in user_data.enrolled_subjects.all() ]
        return JsonResponse({'status': 'succsess',
                                 'data' : {
                                    'user' : user_data.__detail__(),
                                    'enroll_subs' : subs,
                                 }
                                })
    elif request.method == 'POST':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})



@csrf_exempt
def handle_subject(request):
    if request.method == 'GET':
        subs = Subject.objects.all()
        ln = len(subs)
        if ln <= 0 :
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            subs = [ i.__detail__() for i in subs ]
            return JsonResponse({'status': 'succsess', 'data': subs})
    elif request.method == 'POST':
        req_sub = json.loads(request.body)
        sub = Subject.objects.create()
        sub.name = req_sub['name']
        sub.code = req_sub['code']
        sub.prof_name = Professor.objects.get(id=req_sub['prof_id'])
        sub.term = Term.objects.get(id=req_sub['term_id'])
        sub.credits = req_sub['credits']
        sub.save()
        return JsonResponse({'status': 'OK', 'data': 'added subject.'})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

@csrf_exempt
def handle_professor(request):
    if request.method == 'GET':
        prof = Professor.objects.all()
        ln = len(prof)
        if ln <= 0 :
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            prof = [ i.__detail__() for i in prof ]
            return JsonResponse({'status': 'succsess', 'data': prof})
    elif request.method == 'POST':
        print("POST")
        req_prof = json.loads(request.body)
        prof = Professor.objects.create()
        prof.first_name = req_prof['first_name']
        prof.last_name = req_prof['last_name']
        prof.email_id = req_prof['email_id']
        prof.phone_no = req_prof['phone_no']

        prof.save()
        return JsonResponse({'status': 'OK', 'data': 'added Professor.'})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    
@csrf_exempt
def handle_one_professor(request,pk):
    if request.method == 'GET':
        prof = get_object_or_404(Professor,id=pk)
        # prof = prof.__detail__() if type(prof) == 'apis.models.Professor' else prof
        return JsonResponse({'status': 'succsess',
                                 'data' : prof.__detail__()
                            })
    elif request.method == 'POST':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    


@csrf_exempt
def handle_professor_subject(request,pk):
    if request.method == 'GET':
        prof = Professor.objects.get(id=pk)
        sub = Subject.objects.filter(prof_name = prof)
        out = {'status': 'succsess', 
                'data': {
                    'professor' : prof.__detail__(),
                    'subject' : [ i.__detail__() for i in sub ]
        }}
        return JsonResponse(out)
    elif request.method == 'POST':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

@csrf_exempt
def handle_term(request):
    if request.method == 'GET':
        term = Term.objects.all()
        ln = len(term)
        if ln <= 0 :
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            term = [ i.__detail__() for i in term ]
            return JsonResponse({'status': 'succsess', 'data': term})
    elif request.method == 'POST':
        print("POST")
        req_term = json.loads(request.body)
        term = Term.objects.create()
        term.name = req_term['name']
        term.end_date = datetime.strptime(req_term['end_date'],'%Y-%m-%d')
        term.start_date = datetime.strptime(req_term['start_date'],'%Y-%m-%d')
        term.year = datetime.strptime(f"{req_term['year']}-01-01",'%Y-%m-%d' ) 

        term.save()
        return JsonResponse({'status': 'OK', 'data': 'added term.'})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

@csrf_exempt
def handle_subject_user(request,pk):
    if request.method == 'GET':
        sub = get_object_or_404(Subject,id=pk)
        users = sub.userdata_set.all()
        out = {'status': 'succsess', 
                'data': {
                    'subject' : sub.__detail__(),
                    'users' : [ i.__detail__() for i in users ]
        }}
        return JsonResponse(out)
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    
    
@csrf_exempt
def handle_subject_user_email_list(request,pk):
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

@csrf_exempt
def handle_subject_professor(request,pk):
    if request.method == 'GET':
        sub = get_object_or_404(Subject,id=pk)
        all_subs_with_same_code = Subject.objects.filter(code = sub.code, term = sub.term)

        out = {'status': 'succsess', 
                'data': {
                    'subject' : sub.__comm_detail__(),
                    'professor' : [ i.prof_name.__detail__() for i in all_subs_with_same_code ]
        }}
        return JsonResponse(out)
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})

@csrf_exempt
def handle_one_subject(request,pk):
    if request.method == 'GET':
        sub = get_object_or_404(Subject,id=pk)
        # sub = sub.__detail__() if type(sub) == 'apis.models.Subject' else sub
        # print(sub)
        return JsonResponse({'status': 'succsess',
                                  'data' : sub.__detail__()
                            })
    elif request.method == 'POST':
        print("xyz")
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

@csrf_exempt
def send_email_subject_user(request,pk):
    if request.method == 'GET':
        sub = get_object_or_404(Subject,id=pk)
        comm_users = sub.userdata_set.all()
        # email_list = [ user.user.email for user in comm_users]
        from_email_id=config('EMAIL_HOST_USER')
        
        for user in comm_users :
            ( html_message , plain_message ) = create_mail_body(user, sub)
            attachment_file = create_mail_attachment(user, comm_users, sub)
            # print(f'Subject : {sub.__str__()},\nMessage : {plain_message}\n, from : {from_email_id},\n to email : {user.user.email}')

            send_email_with_attachment(f'Subject : {sub.__str__()}', plain_message, html_message, from_email_id, [user.user.email], attachment_file )
            # send_mail(
            # f'Subject : {sub.__str__()}',
            # plain_message,
            # from_email_id,
            # [user.user.email],
            # html_message=html_message
            # )
            os.system(f"rm -rf {attachment_file}")
        return JsonResponse({'status': 'success', 'data': f'sent mail to all user with enrolled sub : {sub.__str__()}'})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
        

def send_email_with_attachment(subject, message, html_message, from_email, recipient_list, attachment_path=None):
    # Create the email message object
    email_message = EmailMultiAlternatives(subject=subject, body=message, from_email=from_email, to=recipient_list)

    # Attach the HTML message
    email_message.attach_alternative(html_message, "text/html")

    # Attach the file if provided
    if attachment_path is not None:
        with open(attachment_path, 'rb') as attachment:
            file_data = attachment.read()
            file_name = attachment.name
            email_message.attach(file_name, file_data)

    # Send the email
    email_message.send()

def create_mail_body(user, sub):
    html_message = render_to_string('email_template.html', {'first_name' : user.first_name , 'subject' : sub.__str__() })
    plain_message = strip_tags(html_message)

    return ( html_message , plain_message )

def create_mail_attachment(current_user , common_users, sub):
    out_file = f"{current_user.id}_{sub.code}.xlsx"
    
    try :
        user_subs = Subject.objects.filter(userdata__id=current_user.id)
    except :
        user_subs = False
        cmd = f"touch '{out_file}'"
        os.system(cmd)
        return out_file
    
    # Create an Excel workbook and select the active worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Write the header row to the worksheet
    header_row = [ "First Name", "Last Name", "Email ID", "Start Term", "Common Subjects"]
    worksheet.append(header_row)

    for user in common_users:
        if user == current_user :
            continue
        common_subs = user_subs.filter(userdata__id=user.id)
        common_subs = [ sub.__for_xlx__() for sub in common_subs ]
        if common_subs:
            row = [user.first_name, user.last_name, user.user.email, user.start_term.__str__(), common_subs[0] ]
            worksheet.append(row)
            for i in range(1,len(common_subs)):
                row = ['', '', '', '', common_subs[i] ]
                worksheet.append(row)
            
            worksheet.append([])
        

    # Save the workbook to a file
    workbook.save(out_file)

    return out_file



    
# @csrf_exempt
# def get_user_subjects(request,pk):
#     if request.method == 'GET':
#         curr_user = User.objects.get(id=pk)
#         curr_udata = UserData.objects.get(user = curr_user)
#         user_subs = curr_udata.enrolled_subjects.all()
#         if curr_user is None and curr_udata is None :
#             return JsonResponse({'status': 'error', 'data': 'User NOT Found.'})
#         else:
#             out_json = {'status': 'succsess',
#                                     'id': pk,
#                                     'user' : curr_udata.__detail__(),
#                                     'subjects' : [ i.__detail__() for i in user_subs ]  
#                                     }
#             print(out_json)
#             return JsonResponse(out_json)
#     else:
#         return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})


@csrf_exempt
def get_term(request,pk):
    if request.method == 'GET':
        term = Term.objects.get(id=pk)
        if not term:
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            return JsonResponse({'status': 'succsess', 'data': term.__detail__()})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})


@csrf_exempt
def get_all_terms(request):
    if request.method == 'GET':
        terms = Term.objects.all()
        ln = len(terms)
        if ln <= 0 :
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            terms = [ i.__detail__() for i in terms ]
            return JsonResponse({'status': 'succsess', 'data': terms})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

@csrf_exempt
def handle_term_subject(request,pk):
    if request.method == 'GET':
        curr_term = Term.objects.get(id=pk)
        subs = Subject.objects.filter(term=curr_term)

        if not subs:
            return JsonResponse({'status': 'error', 'data': 'NOT Found.'})
        else:
            subs = [ i.__detail__() for i in subs ]
            return JsonResponse({'status': 'succsess', 'data': subs})
    else:
        return JsonResponse({'status': 'error', 'data': 'Invalid request method.'})
    

