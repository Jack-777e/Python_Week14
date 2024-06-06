from my_sqlite.StudentInfoTable import StudentInfoTable
from my_sqlite.StudentSubjectTable import StudentSubjectTable

class ServerModifyStu:
    def execute(self, message):
        reply_msg = {}
        name = message['parameters']['name']
        scores_dict = message['parameters']['scores']
        stu_id = StudentInfoTable().select_a_student(name)[0]

        for subject, score in scores_dict.items():
            if self.check_subject_exist(stu_id, subject):
                StudentSubjectTable().update_subject_info(stu_id, subject, score)
            else:
                StudentSubjectTable().insert_subject_info(stu_id, subject, score)

        reply_msg['status'] = "OK"
        
        return reply_msg

    def check_subject_exist(self, stu_id, subject):
        scores_dict = StudentSubjectTable().select_subject_info(stu_id)
        return subject in scores_dict
