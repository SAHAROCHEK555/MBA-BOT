import json
    

class Questions:
    def __init__(self):
        with open('app/questions/questions.json', 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
        pass

    def get_question(self, questions_id):
        return self.questions[questions_id]
