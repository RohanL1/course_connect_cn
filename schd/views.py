from django.shortcuts import render
from django.http import HttpResponse

from ping.views import * 
# import ping_ack.ping_mod 
import threading
import time
import schedule
from django.views.decorators.csrf import csrf_exempt

# Create your views here

# def home(request):
#     if(request.find('/start')>0):
#         start_schd()
#     else:
#         return HttpResponse("Welcome to scheduler")

def check_failure_job ():
    server_alive.check_failure()
    return


def send_alive_ping_job ():
    server_alive.send_ping()
    return


@csrf_exempt
def test(req):
    return JsonResponse({'status': 'OK', 'data': 'TEST.'})

@csrf_exempt
def start_schd(req):

    def threader(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
        
    schedule.every(5).seconds.do(threader,check_failure_job)
    schedule.every(5).seconds.do(threader,send_alive_ping_job)
    # schedule.every(700).seconds.do(threader,check_neighbour)

    first_resp= True
    while True:
        schedule.run_pending()
        time.sleep(5)
        # if first_resp : 
        #     first_resp = False
        #     return JsonResponse({'status': 'OK', 'data': 'start.'})