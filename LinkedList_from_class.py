from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # Complexity Time: O(n)
    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.data, end=' ')
            temp = temp.next

    # Complexity Time: O(1)
    def add_new_head(self,data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Complexity Time: O(n)
    def add_at_end(self,data):
        new_node = Node(data)
        temp = self.head
        if temp is None:
            temp = new_node
            return    #end of func
        else:
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node

    # Complexity Time: O(1)
    def is_empty(self):
        temp = self.head
        if temp is None:
            return True  #empty
        else:
            return False    #not empty

    # Complexity Time: O(n)
    def count(self):
        temp = self.head
        counter = 0  #empty
        while temp is not None:  #not empty
            counter = counter + 1
            temp = temp.next
        return counter

    # Complexity Time: O(n)
    def sum_list(self):
        temp = self.head
        if temp is None:
            return 0  #empty
        else:
            sum = 0
            while temp is not None:
                sum = sum + temp.data
                temp = temp.next
            return sum

    # Complexity Time: O(1)
    def delete_the_head(self):
        temp = self.head
        if temp is None:
            print(None)
        else:
            new_head = temp.next
            self.head = new_head
            return temp.data

    # Complexity Time: O(1)
    def who_is_the_head(self):
        temp = self.head
        if temp is None:
            return None
        else:
            return temp.data

    # Complexity Time: O(n)
    def is_palindrome(self):
        S = []  # empty
        Q = deque()  # empty
        temp = self.head
        while temp is not None:
            S.append(temp.data)
            Q.append(temp.data)
            temp = temp.next
        flag = True
        while len(S) > 0 and len(Q) > 0:
            if S.pop() != Q.popleft():
                flag = False
                break
        return flag

    # Complexity Time: O(n)
    def create_sub_list(self,index):
        temp = self.head
        if temp is None:
            return None      # the list is empty
        elif (index > self.count()) or (index < 0):   # O(n)
            return "your index is out of range..."
        else:
            sub = []
            sub_list = LinkedList()
            for i in range(index):
                sub.append(temp.data)
                temp = temp.next
            size_sub = len(sub)
            while size_sub > 0:
                sub_list.add_new_head(sub[size_sub-1])
                size_sub = size_sub - 1
            return sub_list.print_list()

    # Complexity Time: O(n)
    def create_string(self):
        temp = self.head
        if temp is None:
            return None
        else:
            string = ""
            while temp is not None:
                string = string + temp.data
                temp = temp.next
            return string

    # Complexity Time: O(n)
    def create_reverse_string(self):
        reverse_string = self.create_string()
        if reverse_string is None:
            return None
        else:
            return reverse_string[::-1]
        #O(n)
    def create_list(self):
        temp = self.head
        ll_to_list = []
        while temp is not None:
            ll_to_list = ll_to_list + [temp.data]
            temp = temp.next
        return ll_to_list

    def delete_node(self, node):
        temp = self.head
        if temp is not None:
            if temp.data == node:
                self.delete_the_head()
                return
        while temp is not None:
            if temp.data == node:
                break
            prev = temp
            temp = temp.next
        if temp is None:
            return
        prev.next = temp.next

