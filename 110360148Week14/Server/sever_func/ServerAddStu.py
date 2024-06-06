from StudentInfoTable import StudentInfoTable
from SubjectInfoTable import SubjectInfoTable

class ServerAddStu:
    def __init__(self, add_student):
        self.add_student = add_student
    
    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.add_student['name'])

        if stu_id != []:
            reply_msg = {'status': 'Fail', 'reason': 'The name already exists.'}
        else:
            StudentInfoTable().insert_a_student(self.add_student['name'])
            stu_id = StudentInfoTable().select_a_student(self.add_student['name'])[0]

            for subject, score in self.add_student['scores'].items():
                SubjectInfoTable().insert_a_subject(stu_id, subject, score)

            reply_msg = {'status':'OK'}

        return reply_msg