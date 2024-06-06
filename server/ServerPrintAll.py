from my_sqlite.StudentInfoTable import StudentInfoTable
from my_sqlite.StudentSubjectTable import StudentSubjectTable

class ServerPrintAll :
    def execute(self,message) :
        reply_msg={}
        name_dict={}
        score_dict={}
        merge_dict={}
        name_dict = name_rows_to_dict(StudentInfoTable().select_all_students())
        score_dict = score_rows_to_dict(StudentSubjectTable().select_all_subject_info())
        for stu_id, student_info in name_dict.items():
            student_name = student_info['name']
            merge_dict[student_name] = {'name': student_name, 'scores': {}}
            for subject, score in score_dict[stu_id].items():
                merge_dict[student_name]['scores'][subject] = score


        reply_msg['status']="OK"
        reply_msg['parameters']=merge_dict
        return reply_msg
    

def name_rows_to_dict(rows):
    result = {}
    for row in rows:
        result[row['stu_id']] = dict(row)
    return result

def score_rows_to_dict(rows):
    result = {}
    for row in rows:
        row_dict = dict(row)
        stu_id, subject, score = row_dict.get('stu_id'), row_dict.get('subject'), row_dict.get('score')
        if stu_id not in result:
            result[stu_id] = {}
        if subject is not None:
            result[stu_id][subject] = score
    return result