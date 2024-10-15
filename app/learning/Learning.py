import json


class Learning:
    def __init__(self):
        with open('app/learning/lessons.json', 'r', encoding='utf-8') as f:
            self.lessons = json.load(f)
        pass

    def get_lesson(self, lesson_id):
        return self.lessons[lesson_id]
