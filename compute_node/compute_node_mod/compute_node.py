import httplib2
import json
from random import randint
from datetime import datetime
import websockets as ws
import asyncio
from .new_leader_mod import new_leader
import threading

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
    __websocket_header = 'ws://'
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
            print(f"\nCompute node initiated.\nCompute Node sequence : {cls.__sequence}")
        return cls.__instance
    
    def set_node_addrs(self,address):
        self.reset_counter()
        self.__my_addrs = address
        print(f"\nCompute node address: {self.__my_addrs}")
        
    def set_next_addrs(self,address):
        self.reset_counter()
        self.__next_addrs = address
        print(f"\nCompute node next address: {self.__next_addrs}")
    
    def set_successor_addrs(self,address):
        self.reset_counter()
        self.__successor_addrs = address
        print(f"\nCompute node next_next address: {self.__successor_addrs}")
    
    def set_leader_addrs(self,address):
        self.reset_counter()
        self.__node_leader.set_leader_addrs(address)
        print(f"\nSystem's leader address: {self.__node_leader.get_leader_addrs()}")
        
    def set_message_broker(self,brkr_addrs):
        self.__message_broker_addrs = brkr_addrs
        print(f"\nBroker address: {self.__message_broker_addrs} ")
        
    def set_recv_sequence(self,sequence,addrs):
        self.reset_counter()
        self.__recv_sequence_addrs = addrs
        self.__recv_sequence = sequence
        print(f"\nReceiving heartbeat from : {self.__recv_sequence_addrs}")
        print(f"\nReceiving heartbeat sequence : {self.__recv_sequence}")
        
    #########################################################################
    # Sender functions
    ########################################################################
    
    def send_leader_to_broker(self):
        self.send_data_to_broker(json.dumps(
            {
                'LDR' : self.__node_leader.get_leader_addrs()
            }
        ))

    async def send_data_websocket(self,data):
        ws_url = f'{self.__websocket_header}{self.__message_broker_addrs}'
        # conn = ws.create_connection(ws_url)
        # conn.send(data)
        # conn.close()
        # loop = asyncio.get_event_loop()
        async with ws.connect(ws_url) as websocket:
            await websocket.send(data)
    
    def send_data_to_broker(self,data):
        #Send data to broker
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            thread = threading.Thread(target=lambda: loop.run_until_complete(self.send_data_websocket(data)))
            thread.start()


    def send_election_msg(self,msg):
        http = httplib2.Http()
        next_api = self.__http_header + self.__next_addrs + self.__election_api
        successor_api = self.__http_header + self.__successor_addrs + self.__election_api

        if(self.__next_addrs == self.__node_leader.get_leader_addrs()):
            http.request(successor_api,method="POST",body=json.dumps(msg))
        else :
            http.request(next_api,method="POST",body=json.dumps(msg))
        print(f"\nForwarding election message to next node")
        
    def send_elected_msg(self,msg):
        http = httplib2.Http()
        next_api = self.__http_header + self.__next_addrs + self.__elected_api
        if(self.__successor_addrs != None):
            successor_api = self.__http_header + self.__successor_addrs + self.__elected_api
        if((self.__node_leader.get_leader_addrs() != None) and 
           (self.__next_addrs == self.__node_leader.get_leader_addrs())):
            print(f"\nForwarding election message to next.next node ip: {self.__successor_addrs}")
            http.request(successor_api,method="POST",body=json.dumps(msg))
            print("... DONE.\n")
        else:
            print(f"\nForwarding election message to next node ip: {self.__next_addrs}")
            http.request(next_api,method="POST",body=json.dumps(msg))
            print("... DONE.\n")
            
     
    def send_alive_ping(self):
        http = httplib2.Http()
        alive = self.__http_header + self.__next_addrs + self.__heartbeat_alive_api
        data = {'heartbeat': self.__sequence}
        http.request(alive,method="POST",body=json.dumps(data))
        print(f"\nSending hearbeat to : {self.__next_addrs}")
    
    def send_node_failure_msg(self,addrs):
        http = httplib2.Http()
        leader_addrs = self.__node_leader.get_leader_addrs()
        failure_api = self.__http_header + self.__node_failed_api
        data = {'Failed_node': addrs}
        http.request(failure_api,method="POST",body=json.dumps(data))
        print(f"\nNode failure detetced. Informing the system node leader")
    
    #################################################################################
    # Heartbeat functions
    #################################################################################
    
    def recv_ping(self, heartbeat):
        if((self.__sequence) == heartbeat):
            self.__counter = 0
            self.__clk = datetime.utcnow()
            print(f"\nHeartbeat received")
    
    def check_hearbeat(self):
        if((datetime.utcnow()-self.__clk).total_seconds() < 300):
            self.__counter += 1
        if(self.__counter > 3):
            print(f"\nNo heartbeat received for 3 consecutive beats. Node has failed")
            return False
        return True
        
    def reset_counter(self):
        self.__counter = 0
        
    ################################################################################
    # Leader functions
    ################################################################################
    
    def initiate_leader_election(self):
        print(f"\nInitiating leader election")
        self.elect_leader(address=None)
    
    def elect_leader(self, address = None):
        if(address is None):
            self.__node_leader.set_leader_addrs(None)
            data = {self.__ELECTION_KEY:self.__my_addrs}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address < self.__my_addrs):
            self.__node_leader.set_leader_addrs(None)
            data = {self.__ELECTION_KEY:address}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address > self.__my_addrs):
            self.__node_leader.set_leader_addrs(None)
            data = {self.__ELECTION_KEY:self.__my_addrs}
            self.reset_counter()
            self.send_election_msg(msg=data)
        elif(address == self.__my_addrs):
            self.__node_leader.set_leader_addrs(address)
            self.leader_elected(None)
            
    
    def leader_elected(self, req_data = None):
        if(req_data is None):
            nodes = []
            nodes.append(self.__my_addrs)
            data = {self.__LEADER_ELECTED_KEY : self.__my_addrs, 'nodes': nodes}
            print(data)
            self.reset_counter()
            self.send_elected_msg(data)
        elif(req_data is not None):
            print(req_data)
            leader_ip = req_data[self.__LEADER_ELECTED_KEY]
            if(self.__my_addrs != leader_ip):
                self.__node_leader = leader_ip
                nodes = req_data['nodes']
                nodes.append(self.__my_addrs)
                data = {self.__LEADER_ELECTED_KEY : self.__my_addrs, 'nodes': nodes}
                self.reset_counter()
                self.send_elected_msg(data)
            else:
                self.__node_leader.compose_ring_node(req_data['nodes'])
                self.__node_leader.broadcast_ring_node()
    
    def node_failed(self, addrs):
        if(addrs == self.__node_leader.get_leader_addrs()):
            self.initiate_leader_election()
            print(f"\nLeader failed. Initiating leader election")
        else:
            self.send_node_failure_msg(addrs)
            print(f"\nInforming leader about node failure.")
    
    def check_node_failure(self):
        if(self.check_hearbeat() != True):
            self.node_failed(self.__recv_sequence)
            
    def handle_failure(self,addrs):
        print(f"\nRecieved failed node information. Updating the system communication channel")
        self.__node_leader.update_failed_node(addrs)
        
    def assign_task(self,task):
        print(f"\nAssigning taks to worker node")
        self.__node_leader.assign_task_worker(task)
        
    def send_email(self):
        if(self.__my_addrs == self.__node_leader.get_leader_addrs()):
            print(f"\nSending emails to subscriber")
            self.__node_leader.send_email()
            