import json
    

class Resources:
    def __init__(self):
        with open('app/resources/resources.json', 'r', encoding='utf-8') as f:
            self.resources = json.load(f)
        pass

    def get_question(self, resources_id):
        return self.resources[resources_id]