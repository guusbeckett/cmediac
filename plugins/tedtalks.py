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
        feed = feedparser.parse('http://feeds.feedburner.com/TedtalksHD?format=xml')
        return [Media(talk["title"], talk["media_content"][0]["url"]) for talk in feed["items"]]
