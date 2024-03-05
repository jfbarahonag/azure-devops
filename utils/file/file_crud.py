import os

class FileCRUD:
    @staticmethod
    def create(content, filepath, force=False, is_binary=False):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(filepath) and force == False:
            return False
        if os.path.isdir(filepath):
          return True

        with open(filepath, 'w' if is_binary is False else 'wb') as file:
            file.write(content)

        return True
    
    @staticmethod
    def read(filepath):
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r') as file:
            return file.read()
    
    @staticmethod
    def update(content, filepath):
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'w') as file:
            file.write(content)
        return True
    
    @staticmethod
    def delete(filepath):
        if not os.path.exists(filepath):
            return False
        os.remove(filepath)
        return True
    
    @staticmethod
    def list_files(directory):
        return os.listdir(directory)
