import json


class User_File_Handler:
    def __init__(self, path):
        self.path = path

    def load(self):
        content = []
        with open(self.path) as file:
            content = json.load(file)
        return content

    def save(self, content):
        with open(self.path, "w") as file:
            json.dump(content, file, indent=4)

    def add(self, obj):

        content = self.load()
        content.append(obj.to_dict())
        self.save(content)

    def remove(self, user_id):

        users = self.load()
        new_content = [row for row in users if row["id"] != user_id]
        self.save(new_content)

    def update(self, user):

        users = self.load()
        for row in users:
            if row.get("id") == user.id:
                row.update(user)
        self.save(users)

    def get(self, user_id):

        content = self.load()

        for row in content:

            if row.get("id") == user_id:
                return row
        return None

    def get_by_username(self, username):

        content = self.load()

        for row in content:

            if row.get("username") == username:
                return row
        return None
