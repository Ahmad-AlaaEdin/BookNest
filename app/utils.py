import json
class Text_File_Handler :
    def __init__(self,path):
        self.path = path
    def load(self):
        content = []
        with open(self.path) as file:   
            content = json.load(file)
        return content
    def save(self,content):
        with open(self.path,'w') as file:
            json.dump(content,file,indent=4)

    def add(self,obj):
        
        content = self.load()
        content.append(obj.dict())
        self.save(content)

    def remove(self,condition):
        key , value = list(condition.items())[0]
        content = self.load()
        new_content = [row  for row in content if row[key] != value]
        self.save(new_content)

    def update(self,condition,obj):
        key , value = list(condition.items())[0]
        content = self.load()
        for row in content :
            if(row.get(key) == value):
                row.update(obj)
        self.save(content)
    def get(self,condition):
        key , value = list(condition.items())[0]
        content = self.load()
        
        for row in content :
            
            if(row.get(key) == value):
                return row
        return None