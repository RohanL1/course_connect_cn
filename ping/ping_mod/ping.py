from datetime import datetime
import httplib2
import json
from random import randint
import os
from django.http import JsonResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class PING_ACK():
    __instance = None
    __sequence = None
    __own_sequence = None
    __host = None
    __clk = None
    __counter = None
    __msg_brkr = None
    __leader = None
    
    # def create_local_setup(self):
    #     local_settings = {  
    #                         "__sequence" : self.__sequence, 
    #                         "__own_sequence" : self.__own_sequence, 
    #                         "__host" : self.__host, 
    #                         "__clk" : self.__clk,
    #                         "__counter" : 0,
    #                         "__msg_brkr" : self.__msg_brkr,
    #                         "__leader" : self.__leader
    #                 }
    #     with open("local_settings.json", "w") as outfile:
    #         json.dump(local_settings, outfile)
    #     return 
    
    def local_setup(self):

        with open(str(BASE_DIR) + '/local_settings.json', 'r') as openfile:
            # Reading from json file
            local_settings = json.load(openfile)

        self.__sequence = local_settings["__sequence"]
        self.__host = local_settings["__host"]
        self.__clk = datetime.utcnow()
        self.__counter = local_settings["__counter"]
        self.__msg_brkr = local_settings["__msg_brkr"]
        self.__leader = local_settings["__leader"]
        return 

    def __new__(cls):
        if(cls.__instance == None):
            cls.__instance = super(PING_ACK,cls).__new__(cls)
            cls.__own_sequence = randint(1,84600)
        cls.local_setup(cls)
        print(f"\nHost:{cls.__host}\nmsg_brk:{cls.__msg_brkr}\nleader:{cls.__leader}")
        return cls.__instance
    
    def set_server(self,HOST, BROKER, LEADER):
        self.__host= HOST
        self.__msg_brkr = BROKER
        self.__leader = LEADER
        print(f"\nHost:{self.__host}\nmsg_brk:{self.__msg_brkr}\nleader:{self.__leader}")
        
    def set_sequence(self,value):
        self.__sequence = value
        self.__counter = 0
        self.__clk = datetime.utcnow()
        print(f"\nSeq:{self.__sequence}")
        
    def recv_ping(self, heartbeat):
        if((self.__sequence) == heartbeat):
                self.__counter = 0
                self.__clk = datetime.utcnow()
       
        print(f"__sequence : {self.__sequence}")
        
    def check_failure(self):
        if((datetime.utcnow()-self.__clk).total_seconds() < 5):
            self.__counter += 1
            self.__clk = datetime.utcnow()
            return self.__counter,-1
        if(self.__counter > 3):
            return -1,self.__host
        
        return 0,0
            
            
    def send_ping(self):
        req = httplib2.Http()
        alive = "/ping/recv_alive/"
        data = {'heartbeat' : self.__own_sequence}
        dest_host = self.__host + alive
        r, content = req.request(dest_host,method="GET",body=json.dumps(data))