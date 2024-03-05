import os

class FileCRUD:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def create(self, content, filepath=None):
        filepath = filepath or self.filepath
        if os.path.exists(filepath):
            return False
        with open(filepath, 'w') as file:
            file.write(content)
        return True
    
    def read(self, filepath=None):
        filepath = filepath or self.filepath
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r') as file:
            return file.read()
    
    def update(self, content, filepath=None):
        filepath = filepath or self.filepath
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'w') as file:
            file.write(content)
        return True
    
    def delete(self, filepath=None):
        filepath = filepath or self.filepath
        if not os.path.exists(filepath):
            return False
        os.remove(filepath)
        return True
    
    @staticmethod
    def list_files(directory):
        return os.listdir(directory)
