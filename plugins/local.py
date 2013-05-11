import os

class Media:
    def __init__(self, title, path):
        self.title = title
        self.path = path
        
    def get_url(self):
        return self.path
            
class Category:
    def __init__(self, title, path):
        self.title = title
        self.path = path
        
    def get_items(self):
        return [Media(file, self.path + '/' + file) for file in sorted(os.listdir(self.path), reverse=True) if not os.path.isdir(self.path + '/' + file)]
        
class Plugin:
    def __init__(self, config):
        self.name = 'Local files'
        self.path = config.get("local", "path", fallback="Videos")
        
    def get_items(self):
        return [Category(directory, self.path + '/' + directory) for directory in os.listdir(self.path) if os.path.isdir(self.path + '/' + directory)]