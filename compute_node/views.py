import json

from .compute_node_mod import compute_node
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


aws_node = compute_node.Compute_Node()


###########################################################
    # Setters functions
###########################################################

@csrf_exempt
def set_server(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)

        #set server IP
        addrs = data['node_addrs']
        aws_node.set_node_addrs(addrs)

        #set leader
        leader_adr = data['leader']
        aws_node.set_leader_addrs(leader_adr)

        #set broker
        addrs = data['broker']
        aws_node.set_message_broker(addrs)

        #set successor and next
        next_adrs = data['next'] if 'next' in data.keys() else None
        successor_adr = data['successor'] if 'successor' in data.keys() else None
        if(next_adrs != None):
            aws_node.set_next_addrs(next_adrs)
        if(successor_adr != None):
            aws_node.set_successor_addrs(successor_adr)
        
        #set sequence and address
        seq = data['sequence']
        addrs = data['address']
        aws_node.set_recv_sequence(seq,addrs)

        return JsonResponse({'status': 'OK'})


@csrf_exempt
def set_server_IP(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        addrs = data['node_addrs']
        aws_node.set_node_addrs(addrs)
        return JsonResponse({'status': 'OK'})

@csrf_exempt
def set_next_and_successor(http_req):
    next_adrs = None
    successor_adr = None
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        next_adrs = data['next'] if 'next' in data.keys() else None
        successor_adr = data['successor'] if 'successor' in data.keys() else None
        if(next_adrs != None):
            aws_node.set_next_addrs(next_adrs)
        if(successor_adr != None):
            aws_node.set_successor_addrs(successor_adr)
        return JsonResponse({'status': 'OK'})

@csrf_exempt        
def set_leader(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        leader_adr = data['leader']
        aws_node.set_leader_addrs(leader_adr)
        return JsonResponse({'status': 'OK'})

@csrf_exempt
def set_message_broker(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        addrs = data['broker']
        aws_node.set_message_broker(addrs)
        return JsonResponse({'status': 'OK'})

@csrf_exempt
def set_heartbeat(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        seq = data['sequence']
        addrs = data['address']
        aws_node.set_recv_sequence(seq,addrs)
        return JsonResponse({'status': 'OK'})   
        
#################################################################################
    # Heartbeat functions
#################################################################################

@csrf_exempt
def heartbeat_recv(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        heartbeat = data['heartbeat']
        aws_node.recv_ping(heartbeat)
        return JsonResponse({'status': 'OK'})

################################################################################
    # Leader functions
################################################################################

@csrf_exempt
def initiate_leader_election(self):
    aws_node.initiate_leader_election()
    return JsonResponse({'status': 'OK'})


@csrf_exempt
def leader_election(http_req):
    if(http_req.method == 'POST'):  
        data = json.loads(http_req.body)
        addrs = data['election']
        aws_node.elect_leader(addrs)
        return JsonResponse({'status': 'OK'})

@csrf_exempt
def leader_elected(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        addrs = data['elected']
        aws_node.set_leader_addrs(addrs)
        aws_node.leader_elected(data)
        return JsonResponse({'status': 'OK'})

@csrf_exempt        
def handle_failed_node(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        failed_node = data['Failed_node']
        aws_node.handle_failure(failed_node)
        return JsonResponse({'status': 'OK'})

@csrf_exempt        
def assign_task(http_req):
    if(http_req.method == 'POST'):
        data = json.loads(http_req.body)
        aws_node.assign_task(data)
        return JsonResponse({'status': 'OK'})


