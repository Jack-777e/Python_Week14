from StudentInfoTable import StudentInfoTable
from StudentSubjectTable import StudentSubjectTable

class ServerAddStu :
    def execute(self,message) :
        reply_msg={}

        StudentInfoTable().insert_a_student(message['parameters']['name'])
        stu_id=StudentInfoTable().select_a_student(message['parameters']['name'])[0]
        for subject in message['parameters']['scores'].keys():
            score=message['parameters']['scores'][subject]
            StudentSubjectTable().insert_subject_info(stu_id,subject,score)
        reply_msg['status']="OK"
        reply_msg['parameters']=message['parameters']
        return reply_msg


"""
message={'command': 'add', 'parameters': {'name': 'Test1', 'scores': {'English': 99.0, 'Chinese': 88.0}}}
"""