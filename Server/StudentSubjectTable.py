from DBConnection import DBConnection

class StudentSubjectTable:
    def insert_subject_info(self, stu_id, subject, score):
        command = "INSERT INTO subject_info (stu_id, subject, score) VALUES ({}, '{}', {});".format(stu_id, subject, score)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_subject_info(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id={};".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()
        scores_dict = {record['subject']: record['score'] for record in records}
        return scores_dict

    def delete_subject_info(self, stu_id):
        command = "DELETE FROM subject_info WHERE stu_id={};".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_subject_info(self, stu_id, subject, new_score):
        command = "UPDATE subject_info SET score={} WHERE stu_id={} AND subject='{}';".format(new_score, stu_id, subject)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_all_subject_info(self):
        command = "SELECT * FROM subject_info;"
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()
        return records