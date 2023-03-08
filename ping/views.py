
from django.http import HttpResponse
from ping.ping_mod import ping

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

import json

# import threading
# import time
# import schedule
# from datetime import datetime


# Create your views here.
content = {'title':'Hello'}

def home(request):
    print(f"\n{request}")
    return HttpResponse("Hello")

server_alive = ping.PING_ACK()

@csrf_exempt
def set_up_server(request):
    #Need to deduce this from api
    if(request.method == "POST"):
        data = json.loads(request.body)
        destination_host = data['destination_host']
        message_Broker = data['message_Broker']
        server_Leader = data['server_Leader']
        server_alive.set_server(destination_host,message_Broker,server_Leader)

        return JsonResponse({'status': 'OK', 'data': 'set_up_server Completed.'}) 

@csrf_exempt
def set_up_heartbeat(request):
    #Need to deduce this from api
    if(request.method == "POST"):
        data = json.loads(request.body)
        recv_sequence = data['recv_sequence']
        server_alive.set_sequence(recv_sequence)
        return JsonResponse({'status': 'OK', 'data': 'set_up_heartbeat Completed.'}) 
    
@csrf_exempt    
def recv_ping(request):
    if(request.method == "GET"):
        data = json.loads(request.body)
        heartbeat = data['heartbeat']
        server_alive.recv_ping(heartbeat)
        return JsonResponse({'status': 'OK', 'data': 'recv'}) 

@csrf_exempt    
def send_alive_ping(request):
    server_alive.send_ping()
    return JsonResponse({'status': 'OK', 'data': 'alive.'})

@csrf_exempt
def check_neighbour(request):
    server_alive.check_failure()

@csrf_exempt
def check_failure(request):
    status_code,ip = server_alive.check_failure()

    if (status_code < 0) :
        #do failure handling
        print("Failed NODE")