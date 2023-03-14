
class System_Node:
    
    class Node:
        def __init__(self, value):
            self.data = value
            self.next = None
    
    def __init__(self) -> None:
        self.head = None
        self.tail = None
    
    def add_node(self,value):
        node = self.Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
            node.next = self.head
        elif value < self.head.data:
            node.next = self.head
            self.head = node
            self.tail.next = self.head
        elif value > self.tail.data:
            node.next = self.head
            self.tail.next = node
            self.tail = node
        else:
            curr = self.head
            while curr.next.data < value:
                curr = curr.next
            node.next = curr.next
            curr.next = node
                    
    def print_list(self):
        if self.head is None:
            return
        curr = self.head
        while True:
            print(curr.data, end='->')
            curr = curr.next
            if curr == self.head:
                break
    
    def remove_node(self, data):
        if self.head is None:
            return
        curr = self.head
        prev = self.tail
        while curr.data != data:
            prev = curr
            curr = curr.next
            if curr == self.head:
                return
        if curr == self.head:
            self.head = self.head.next
            self.tail.next = self.head
        elif curr == self.tail:
            prev.next = self.head
            self.tail = prev
        else:
            prev.next = curr.next
        curr = None
        
    def get_successor(self, data):
        if self.head is None:
           return None
        curr = self.head
        while curr.data != data:
            curr = curr.next
            if curr == self.head:
                return None
        return curr.next.data

    def get_predecessor(self, data):
        if self.head is None:
            return None
        curr = self.head
        prev = self.tail
        while curr.data != data:
            prev = curr
            curr = curr.next
            if curr == self.head:
                return None
        return prev.data
