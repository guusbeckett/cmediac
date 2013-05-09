import urllib.request
import urllib.parse
import re

def get_name():
    return 'YouTube'

def get_links():
    links = []
    
    with open("youtube-channels.txt") as f:
        for channel in f:
            feed = urllib.request.urlopen('http://gdata.youtube.com/feeds/api/users/' + channel.strip() + '/uploads') 
            data = feed.read().decode()
            links.extend(re.findall("<published>([^<>]+)</published><updated>[^<>]+</updated><category [^<>]+/><category [^<>]+/><title type='text'>([^<>]+)</title><content type='text'>[^<>]+</content><link rel='alternate' type='text/html' href='([^']+)'/>", data))

    #links = sorted(links, reverse=True, key=lambda x : datetime.datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S.000Z"))
    links = sorted(links, reverse=True, key=lambda x : x[0])
    links = [(link[1], link[2]) for link in links]
    
    return links 

def get_media(url):
    tokens = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    
    file = urllib.request.urlopen('http://www.youtube.com/get_video_info?&video_id=' + tokens['v'][0] + '&ps=default&eurl=&gl=US&hl=en')
    video_info = urllib.parse.parse_qs(file.read().decode())
    
    url_data_strs = video_info['url_encoded_fmt_stream_map'][0].split(',')
    url_data = [urllib.parse.parse_qs(uds) for uds in url_data_strs]
    video = url_data[0] # always pick the first; this might need a little more research

    return video['url'][0] + '&signature=' + video['sig'][0]