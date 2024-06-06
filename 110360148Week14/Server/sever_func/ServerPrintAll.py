from StudentInfoTable import StudentInfoTable
from SubjectInfoTable import SubjectInfoTable

class ServerPrintAll:
    def __init__(self, reply_msg):
        self.student_dict = dict()
        self.reply_msg = reply_msg
    
    def execute(self):
        for stu_id, stu_name in StudentInfoTable().select_all_student().items():
            scores = SubjectInfoTable().select_a_subject(stu_id)
            self.student_dict[stu_name] = {'name': stu_name, 'scores': scores}

        self.reply_msg = {'status':'OK', 'parameters':self.student_dict}
        return self.reply_msg
