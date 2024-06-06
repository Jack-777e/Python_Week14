from my_sqlite.StudentInfoTable import StudentInfoTable
from my_sqlite.StudentSubjectTable import StudentSubjectTable

class ServerDelStu :
    def execute(self,message) :
        reply_msg={}
        stu_id=StudentInfoTable().select_a_student(message['parameters']['name'])[0]
        StudentInfoTable().delete_a_student(stu_id)
        StudentSubjectTable().delete_subject_info(stu_id)
        reply_msg['status']="OK"
        return reply_msg
    
