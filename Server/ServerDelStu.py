from StudentInfoTable import StudentInfoTable
from StudentSubjectTable import StudentSubjectTable


class ServerDelStu :
    def execute(self,message) :
        reply_msg={}
        stu_id=StudentInfoTable().select_a_student(message['parameters']['name'])[0]
        StudentInfoTable().delete_a_student(stu_id)
        StudentSubjectTable().delete_subject_info(stu_id)
        reply_msg['status']="OK"
        return reply_msg
    

"""
{"command": "query", "parameters": {"name": "Test2"}}
    server received: {'command': 'query', 'parameters': {'name': 'Test2'}} from ('127.0.0.1', 58661)
    Query Test2 success
{"command": "delete", "parameters": {"name": "Test2"}}
    server received: {'command': 'delete', 'parameters': {'name': 'Test2'}} from ('127.0.0.1', 58661)
"""