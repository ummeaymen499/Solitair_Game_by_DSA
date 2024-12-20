class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None  

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node  

    def pop(self):
        if not self.head:
            return None
        if not self.head.next:  
            data = self.head.data
            self.head = None
            self.tail = None  
            return data
        second_last = self.head
        while second_last.next != self.tail:  
            second_last = second_last.next
        data = self.tail.data
        second_last.next = None
        self.tail = second_last  
        return data

    def is_empty(self):
        return self.head is None

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def get_last(self):
        if self.tail:
            return self.tail.data
        return None


    