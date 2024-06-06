from my_sqlite.StudentInfoTable import StudentInfoTable
from my_sqlite.StudentSubjectTable import StudentSubjectTable

class ServerQueryStu :
    def execute(self,message) :
        reply_msg={}
        name=message['parameters']['name']
        stu_id=StudentInfoTable().select_a_student(name)
        if stu_id==[]:
            reply_msg['status']="Fail"
            reply_msg['reason']="The name is not found."
        else:
            stu_id=stu_id[0]
            reply_msg['status']="OK"
            scores = StudentSubjectTable().select_subject_info(stu_id)
            reply_msg['scores'] = scores
        return reply_msg