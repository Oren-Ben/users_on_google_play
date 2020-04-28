from collections import deque


class Student:
    def __init__(self, student_id, first_name, last_name, age, gender, average):
        if len(str(student_id)) == 9:
            self.student_id = student_id
        else:
            self.student_id = None
            print("ID must be 9 digits")
        # ---
        self.first_name = first_name
        self.last_name = last_name
        # ---
        if age > 0:
            self.age = age
        else:
            self.age = None
            print("Age must be more than 0")
        # ---
        if gender == 0 or gender == 1:
            if gender == 0:
                self.gender = "Female"
            else:
                self.gender = "Male"
        else:
            self.gender = None
            print("Gender must be 0 for Female or 0 for Male")
        # ---
        if 0 <= average <= 100:
            self.average = average
        else:
            self.average = None
            print("Average must be between 0 to 100")
        # ---
        self.next = None

    def __str__(self):
        return "ID: " + str(self.student_id) + "\nFirst Name: " + str(self.first_name) + "\nLast Name: " + str(self.last_name) +\
               "\nAge: " + str(self.age) + "\nGender: " + str(self.gender) + "\nAverage: " + str(self.average)


class SortedStack:
    def __init__(self):
        self.head = None
        self.size = 0

    # Complexity Time: O(n)
    def push(self, student):
        if student.student_id is None or student.age is None or student.gender is None or student.average is None:
            print("so this is ERROR, try again")
        else:
            self.size += 1
            temp = self.head
            if temp is None:
                self.head = student
                return

            if temp.average < student.average:
                student.next = temp
                self.head = student
                return

            while temp.next is not None:
                if temp.next.average < student.average:
                    break
                temp = temp.next
            student.next = temp.next
            temp.next = student
            return


    # Complexity Time: O(n)
    def print_list(self):
        temp = self.head
        while temp is not None:
            # print(temp.average, end=' ')
            print("ID: " + str(temp.student_id) + "\nFirst Name: " + str(temp.first_name) + "\nLast Name: " + str(temp.last_name) +\
               "\nAge: " + str(temp.age) + "\nGender: " + str(temp.gender) + "\nAverage: " + str(temp.average) + "\n-----------")
            temp = temp.next


    # Complexity Time: O(1)
    def is_empty(self):
        temp = self.head
        if temp is None:
            return True  # empty
        else:
            return False  # not empty


    # Complexity Time: O(1)
    def pop(self):
        temp = self.head
        if temp is None:
            print(None)
        else:
            self.size -= 1
            new_head = temp.next
            self.head = new_head
            return temp

    # Complexity Time: O(1)
    def top(self):
        temp = self.head
        if temp is None:
            return None
        else:
            return temp


