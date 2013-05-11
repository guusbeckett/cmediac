import re
import urllib.parse
import urllib.request

class Media:
    def __init__(self, title, page_url):
        self.title = title
        self.page_url = page_url
        
    def get_url(self):
        v = urllib.parse.parse_qs(urllib.parse.urlparse(self.page_url).query)['v'][0]
        
        video_info_file = urllib.request.urlopen('http://www.youtube.com/get_video_info?&video_id=' + v + '&ps=default&eurl=&gl=US&hl=en')
        video_info = urllib.parse.parse_qs(video_info_file.read().decode())
         
        url_data_strs = video_info['url_encoded_fmt_stream_map'][0].split(',')
        url_data = [urllib.parse.parse_qs(uds) for uds in url_data_strs]
        
        for video in url_data:
            if 'webm' not in video['type'][0]:
                return video['url'][0] + '&signature=' + video['sig'][0]   
            
class Plugin:
    def __init__(self):
        self.name = 'YouTube'
        
    def get_media(self):
        items = []
        
        with open("youtube-channels.txt") as f:
            for channel in f:
                feed = urllib.request.urlopen('http://gdata.youtube.com/feeds/api/users/' + channel.strip() + '/uploads') 
                data = feed.read().decode()
                items.extend(re.findall("<published>([^<>]+)</published>" +
                                        "<updated>[^<>]+</updated>" +
                                        "<category [^<>]+/>" +
                                        "<category [^<>]+/>" +
                                        "<title type='text'>([^<>]+)</title>" +
                                        "<content type='text'>[^<>]+</content>" +
                                        "<link rel='alternate' type='text/html' href='([^']+)'/>", data))
    
        items = sorted(items, reverse=True, key=lambda x : x[0])
        return [Media(item[1], item[2]) for item in items]
        

