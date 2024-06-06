class PrintAll:
    @staticmethod
    def execute(client):
        client.send_command('show', {})
        raw_data = client.wait_response()
        return raw_data
