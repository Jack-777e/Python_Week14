class DelStu:
    @staticmethod
    def execute(client, student_dict):
        client.send_command("del", student_dict)
        raw_data = client.wait_response()
        return raw_data     
