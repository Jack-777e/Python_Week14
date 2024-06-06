class Query:
    @staticmethod
    def execute(client, student_name):
        parameters = {"name": student_name}
        client.send_command("query", parameters)
        raw_data = client.wait_response()
        
        if raw_data["status"] == "Fail":
            return None, {}
        scores = raw_data.get("scores", {})
        return raw_data["status"], scores
