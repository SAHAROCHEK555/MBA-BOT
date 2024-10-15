import json


class Tasks:
    @staticmethod
    def get_users():
        with open('app/tasks/data-base.json', 'r', encoding='utf-8') as f:
            result = json.load(f).keys()
            return list(result)
    
    def get_active_tasks(user_id):
        with open('app/tasks/data-base.json', 'r', encoding='utf-8') as f:
            struct = json.load(f)[user_id]["tasks"]
            first_parts = ["day", "week"]
            second_parts = ["one", "two", "three", "four"]
            result_dct = {}
            for i in range(2):
                for j in range(4):
                    key = f"{first_parts[i]}_{second_parts[j]}"
                    val = struct[key]
                    if val["state"] == 1:
                        result_dct[key] = val["name"]

            return result_dct
    
    @staticmethod
    def finish_task(user_id, task_id):
        with open('app/tasks/data-base.json', 'r+', encoding='utf-8') as f:
            struct = json.load(f)
            struct[user_id]["tasks"][task_id]["state"] = 0
            f.seek(0)
            json.dump(struct, f, indent=4)
        return
    
    @staticmethod
    def start_task(user_id, task_id):
        with open('app/tasks/data-base.json', 'r+', encoding='utf-8') as f:
            struct = json.load(f)
            struct[user_id]["tasks"][task_id]["state"] = 1
            f.seek(0)
            json.dump(struct, f, indent=4)
        return
    
    @staticmethod
    def create_user(user_id):        
        with open('app/tasks/pattern.json', 'r', encoding='utf-8') as f:
            task_struct = json.load(f)
        standart_struct_for_user = {user_id: task_struct}
        with open('app/tasks/data-base.json', 'r+', encoding='utf-8') as f:
            struct = json.load(f)
            struct = standart_struct_for_user
            f.seek(0)
            json.dump(struct, f, indent=4)
        return
