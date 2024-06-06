from StudentInfoTable import StudentInfoTable
from SubjectInfoTable import SubjectInfoTable

class ServerQuery:
    def __init__(self, student_name):
        self.student_name = student_name
    
    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.student_name)
        print(stu_id)

        if stu_id != []:
            scores = SubjectInfoTable().select_a_subject(stu_id[0])
            reply_msg = {'status': 'OK', 'scores': scores}
        else:
            reply_msg = {'status': 'Fail', 'reason': 'The name is not found.'}

        return reply_msg