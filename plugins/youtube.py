import urllib.request
import re

def get_name():
    return 'YouTube'

def get_links():
    links = []
    
    with open("youtube-channels.txt") as f:
        for channel in f:
            feed = urllib.request.urlopen('http://gdata.youtube.com/feeds/api/users/' + channel + '/uploads') 
            data = feed.read()
            data = data.decode()
            titles = re.findall("<title type='text'>([^<>]+)</title><content type='text'>[^<>]+</content><link rel='alternate' type='text/html' href='([^']+)'/>", data)
            for title in titles:
                links.append((title[0], title[1]))
    
    return links 

def get_media(url):
    return url