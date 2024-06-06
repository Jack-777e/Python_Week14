class AddStu:
    @staticmethod
    def execute(client, student_dict):

        client.send_command('add', student_dict)
        raw_data = client.wait_response()
        return raw_data
