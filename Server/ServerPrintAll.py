from StudentInfoTable import StudentInfoTable
from StudentSubjectTable import StudentSubjectTable

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
        #reply_msg={'status': 'OK', 'parameters': {'Test1': {'name': 'Test1', 'scores': {'English': 99.0, 'Chinese': 88.0}}, 'Test2': {'name': 'Test2', 'scores': {'Python': 11.0}}}}
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


"""
        for stu_id, student_info in name_dict.items():
            merge_dict[student_info['name']] = {'name': student_info['name'],'scores': {}}

        for stu_id, score_info in score_dict.items():
            student_name = name_dict[stu_id]['name']
            subject = score_info['subject']
            score = score_info['score']
            merge_dict[student_name]['scores'][subject] = score
"""


"""
{'status': 'OK', 
'parameters': 
    {'Test1': 
        {'name': 'Test1'
        , 'scores': 
            {'English': 99.0, 'Chinese': 88.0}}
    , 'Test2': 
        {'name': 'Test2'
        , 'scores': 
            {'Python': 11.0}}}}
"""