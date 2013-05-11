import feedparser
import urllib.parse
import urllib.request

class Media:
    def __init__(self, title, page_url):
        self.title = title
        self.page_url = page_url
        
    def get_url(self):
        v = urllib.parse.parse_qs(urllib.parse.urlparse(self.page_url).query)['v'][0]
        
        with urllib.request.urlopen('http://www.youtube.com/get_video_info?&video_id=' + v + '&ps=default&eurl=&gl=US&hl=en') as file:
            video_info = urllib.parse.parse_qs(file.read().decode())
            url_data_strs = video_info['url_encoded_fmt_stream_map'][0].split(',')
            url_data = [urllib.parse.parse_qs(uds) for uds in url_data_strs]
            for video in url_data:
                if 'webm' not in video['type'][0]:
                    return video['url'][0] + '&signature=' + video['sig'][0]   
            
class Category:
    def __init__(self, title):
        self.title = title
        
    def get_items(self):
        feed = feedparser.parse('http://gdata.youtube.com/feeds/api/users/' + self.title + '/uploads')
        return [Media(item["title"], item["link"]) for item in feed["items"]]
        
class Plugin:
    def __init__(self, config):
        self.title = 'YouTube'
        self.channels = config.get('youtube', 'channels', fallback='').split(',')
        
    def get_items(self):
        return [Category(channel) for channel in self.channels]
