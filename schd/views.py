from django.shortcuts import render

from compute_node.compute_node_mod import compute_node

import schedule
import threading
import time

# Create your views here.

def sending_emails():
    print(f"\nSending Email\n")
    compute_node.Compute_Node().send_email()

def sending_hearbeat():
    print(f"\nSending Heartbeat\n")
    compute_node.Compute_Node().send_alive_ping()
    
def checking_failure():
    print(f"\nChecking Node Failure\n")
    compute_node.Compute_Node().check_node_failure()
    
def start_scheduling():
    
    def threader(job):
        job_thread = threading.Thread(target=job)
        job_thread.start()
        
    schedule.every(10).seconds.do(threader,sending_hearbeat)
    schedule.every(15).seconds.do(threader,checking_failure)
    schedule.every(2).minute.do(threader,sending_emails)

    while True:
        schedule.run_pending()
        time.sleep(20)