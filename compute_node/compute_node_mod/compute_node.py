import httplib2
import json
from random import randint
from datetime import datetime

from .new_leader_mod import new_leader

class Compute_Node:
    __instance = None
    __my_addrs = None
    __next_addrs = None
    __successor_addrs = None
    __node_leader = None
    __message_broker_addrs = None
    __sequence = None
    __recv_sequence = None
    __recv_sequence_addrs = None
    __clk = None
    __counter = None
    __http_header = 'http://'
    __election_api = "/node/election/"
    __elected_api = "/node/elected/"
    __heartbeat_alive_api = "/node/heartbeat/alive/"
    __node_failed_api = "/node/failure/"
    __ELECTION_KEY = 'election'
    __LEADER_ELECTED_KEY = 'elected'
    
    ###########################################################
    # Setters functions
    ###########################################################
    def __new__(cls):
        if(cls.__instance == None):
            cls.__instance = super(Compute_Node,cls).__new__(cls)
            cls.__node_leader = new_leader.Leader()
            cls.__sequence = randint(1,84600)
        return cls.__instance
    
    def set_node_addrs(self,address):
        self.reset_counter()
        self.__my_addrs = address
        
    def set_next_addrs(self,address):
        self.reset_counter()
        self.__next_addrs = address
    
    def set_successor_addrs(self,address):
        self.reset_counter()
        self.__successor_addrs = address
    
    def set_leader_addrs(self,address):
        self.reset_counter()
        self.__node_leader.set_leader_addrs(address)
        
    def set_message_broker(self,brkr_addrs):
        self.__message_broker = brkr_addrs
        
    def set_recv_sequence(self,sequence,addrs):
        self.reset_counter()
        self.__clk = datetime.utcnow()
        self.__recv_sequence_addrs = addrs
        self.__recv_sequence = sequence
        
        
    #########################################################################
    # Sender functions
    ########################################################################
    
    
    def send_election_msg(self,msg):
        http = httplib2.Http()
        is_leader_alive = True
        is_leader_elected = True
        if(self.__node_leader.get_leader_addrs() == None):
            next_api = self.__http_header + self.__next_addrs + self.__election_api
            is_leader_elected = False
        elif(self.__next_addrs == self.__node_leader.get_leader_addrs()):
            successor_api = self.__http_header + self.__successor_addrs + self.__election_api
            is_leader_alive = False
        if(is_leader_elected):
            http.request(next_api,method="POST",body=json.dumps(msg))
        if((is_leader_elected == False) and (is_leader_alive == False)):
            http.request(successor_api,method="POST",body=json.dumps(msg))
        
    def send_elected_msg(self,msg):
        http = httplib2.Http()
        next_api = self.__http_header + self.__next_addrs + self.__election_api
        if(self.__successor_addrs != None):
            successor_api = self.__http_header + self.__successor_addrs + self.__elected_api
        if((self.__node_leader.get_leader_addrs() != None) and
           (self.__next_addrs == self.__node_leader.get_leader_addrs())):
            http.request(successor_api,method="POST",body=json.dumps(msg))
        else:
            http.request(next_api,method="POST",body=json.dumps(msg))
     
    def send_alive_ping(self):
        http = httplib2.Http()
        alive = self.__http_header + self.__next_addrs + self.__heartbeat_alive_api
        data = {'heartbeat': self.__sequence}
        http.request(alive,method="POST",body=json.dumps(data))
    
    def send_node_failure_msg(self,addrs):
        http = httplib2.Http()
        leader_addrs = self.__node_leader.get_leader_addrs()
        failure_api = self.__http_header + self.__node_failed_api
        data = {'Failed_node': addrs}
        http.request(failure_api,method="POST",body=json.dumps(data))
    
    #################################################################################
    # Heartbeat functions
    #################################################################################
    
    def recv_ping(self, heartbeat):
        if((self.__sequence) == heartbeat):
            self.__counter = 0
            self.__clk = datetime.utcnow()
    
    def check_hearbeat(self):
        if((datetime.utcnow()-self.__clk).total_seconds() < 300):
            self.__counter += 1
        if(self.__counter > 3):
            return False
        return True
        
    def reset_counter(self):
        self.__counter = 0
        
    ################################################################################
    # Leader functions
    ################################################################################
    
    def initiate_leader_election(self):
        self.elect_leader(address=None)
    
    def elect_leader(self, address = None):
        if(address is None):
            data = {self.__ELECTION_KEY:self.__my_addrs}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address < self.__my_addrs):
            data = {self.__ELECTION_KEY:address}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address > self.__my_addrs):
            data = {self.__ELECTION_KEY:self.__my_addrs}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address == self.__my_addrs):
            self.__node_leader.update_leader_IP(address)
            self.leader_elected(None)
            
    
    def leader_elected(self, node_list = None):
        if(node_list is None):
            nodes = []
            nodes.append(self.__my_addrs)
            data = {self.__LEADER_ELECTED_KEY : self.__my_addrs, 'Nodes': nodes}
            self.reset_counter()
            self.send_elected_msg(data)
        elif(node_list is not None):
            leader_ip = node_list[self.__LEADER_ELECTED_KEY]
            if(self.__my_addrs != leader_ip):
                self.__node_leader = leader_ip
                nodes = node_list
                nodes.append(self.__my_addrs)
                data = {self.__LEADER_ELECTED_KEY : self.__my_addrs, 'Nodes': nodes}
                self.reset_counter()
                self.send_elected_msg(data)
            else:
                self.__node_leader.compose_ring_node(nodes_list= node_list)
                self.__node_leader.broadcast_ring_node()
    
    def node_failed(self, addrs):
        if(addrs == self.__node_leader.get_leader_addrs()):
            self.initiate_leader_election()
        else:
            self.send_node_failure_msg(addrs)
    
    def check_node_failure(self):
        if(self.check_hearbeat() != True):
            self.node_failed(self.__recv_sequence)
            
    def handle_failure(self,addrs):
        self.__node_leader.update_failed_node(addrs)
        
    def assign_task(self,task):
        self.__node_leader.assign_task_worker(task)
        
    def send_email(self):
        if(self.__my_addrs == self.__node_leader.get_leader_addrs()):
            self.__node_leader.send_email()