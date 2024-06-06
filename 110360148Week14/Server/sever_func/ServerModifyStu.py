from StudentInfoTable import StudentInfoTable
from SubjectInfoTable import SubjectInfoTable

class ServerModifyStu:
    def __init__(self, modify_student):
        self.modify_student = dict(modify_student)
    
    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.modify_student['name'])[0]

        for subject, score in self.modify_student['scores_dict'].items():
            if subject in SubjectInfoTable().select_a_subject(stu_id).keys():
                SubjectInfoTable().update_a_subject(stu_id, subject, score)
            else:
                SubjectInfoTable().insert_a_subject(stu_id, subject, score)

        reply_msg = {'status':'OK'}
        return reply_msg