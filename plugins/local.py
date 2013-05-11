import os

class Media:
    def __init__(self, title, path):
        self.title = title
        self.path = path
        
    def get_url(self):
        return self.path

class Directory:
    def __init__(self, title, path):
        self.title = title
        self.path = path
        
    def get_items(self):
        items = []
        
        for file in sorted(os.listdir(self.path)):
            filepath = self.path + '/' + file
            if os.path.isdir(filepath):
                items.append(Directory(file, filepath))
            else:
                items.append(Media(file, filepath))
                
        return items
        
class Plugin(Directory):
    def __init__(self, config):
        super(Plugin, self).__init__('Local files', config.get("local", "path", fallback="Videos"))