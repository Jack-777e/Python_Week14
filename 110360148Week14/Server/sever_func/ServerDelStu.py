from StudentInfoTable import StudentInfoTable
from SubjectInfoTable import SubjectInfoTable

class ServerDelStu:
    def __init__(self, del_student):
        self.del_student = del_student
    
    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.del_student['name'])[0]
        StudentInfoTable().delete_a_student(stu_id)
        SubjectInfoTable().delete_a_subject(stu_id)
        reply_msg = {'status':'OK'}
        return reply_msg