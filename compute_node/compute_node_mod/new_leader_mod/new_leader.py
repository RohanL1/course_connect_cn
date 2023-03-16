import httplib2
import json

from .node_mod import system_node

class Leader:
    __instance = None
    __leader_IP = None
    __sys_node = None
    __sys_node_list = None
    __worker_counter = 0
    __total_sys_nodes = None
    __http_header = 'http://'
    __broadcast_api = "/node/set/neighbour/"
    __task_api = '/apis/task/'
    __send_email_api = '/apis/send_email/'
    
    def __new__(cls):
        if(cls.__instance == None):
            cls.__instance = super(Leader,cls).__new__(cls)
            cls.__sys_node = system_node.System_Node()
        return cls.__instance
    
    def get_leader_addrs(self):
        return self.__leader_IP
    
    def set_leader_addrs(self,node_addrs):
        self.__leader_IP = node_addrs
        
    def compose_ring_node(self,node_list):
        for nodes in node_list:
            self.__sys_node.add_node(nodes)
        print(f"\nFormed new communication channel for the system nodes")
            
    def broadcast_ring_node(self):
        print(f"\nUnicasting new communcation channel to all the nodes")
        curr_node = self.__sys_node.head
        nodes_list = []
        nodes_list.append(curr_node.data)
        next_node = curr_node.next
        while(next_node != curr_node):
            nodes_list.append(next_node.data)
            next_node = next_node.next
        print(nodes_list)
        self.__sys_node_list = nodes_list
        total_nodes = len(nodes_list)
        self.__total_sys_nodes = total_nodes
        
        http = httplib2.Http()
        for j in range(total_nodes):
            # j = i
            next_addr = nodes_list[((j+1)%total_nodes)]
            successor_addrs = nodes_list[((j+2)%total_nodes)]
            next_addr_api = self.__http_header + next_addr + self.__broadcast_api
            data = {'Next': next_addr, 'Successor':successor_addrs}
            http.request(next_addr_api,method="POST",body=json.dumps(data))
        print(f"\nUpdates all system nodes")
        
        
    def update_failed_node(self,node_addrs):
        self.__sys_node.remove_node(node_addrs)
        self.broadcast_ring_node()
        
    def assign_task_worker(self, task):
        index = (self.__worker_counter +1) % self.__total_sys_nodes
        worker_node_addrs = self.__sys_node_list[index]
        http = httplib2.Http()
        task_addrs = self.__http_header + worker_node_addrs + self.__task_api
        http.request(task_addrs,method="POST",body=json.dumps(task))
        print(f"Task successfully assigned to the worker node")

    def send_email(self):
        email_addrs = self.__http_header + self.__leader_IP + self.__send_email_api
        http = httplib2.Http()
        http.request(email_addrs,method="GET")
        