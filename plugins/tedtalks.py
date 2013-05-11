import feedparser

class Media:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        
    def get_url(self):
        return self.url

class Plugin:
    def __init__(self, config):
        self.title = 'TED Talks'
        
    def get_items(self):
        feed = feedparser.parse('http://feeds.feedburner.com/tedtalks_video')
        return [Media(talk["title"], talk["feedburner:origEnclosureLink"]) for talk in feed["items"]]
