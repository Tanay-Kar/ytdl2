# ./modules/Query.py
#
# By: Tanay Kar
# Module for YTDL2
# 
# This file contains the StreamQuery class, which is used to list the 
# streams from the json file (./tmp/details.json). The Details class
# is used to list the details of the video.


import json
from typing import Literal

StreamTypes = Literal["audio", # Audio only
                      "progressive", # Video + Audio
                      "adaptive", # Video only
                      "none", # No streams : Only for stream selection
                    ]

class Data:
    def __init__(self,path='tmp/data.json') -> None:
        self.path = path
        with open(self.path,'r') as f:
            self.data = json.load(f)
        
    def get_data(self) -> dict:
        return self.data


class Stream:
    def __init__(self,
                 stream_type : StreamTypes,
                 format_note,
                 id,
                 abr=None,
                 resolution=None,
                 url=None,
                 acodec=None,
                 vcodec=None) -> None:
        self.stream_type = stream_type
        self.format_note = format_note
        self.id = id
        self.url = url
        if self.stream_type == "audio":
            self.abr = abr
            self.acodec = acodec
            
        elif self.stream_type == "adaptive":
            self.resolution = resolution
            self.vcodec = vcodec
        
        elif self.stream_type == "progressive":
            self.abr = abr
            self.resolution = resolution
            self.acodec = acodec
            self.vcodec = vcodec
        
    def __repr__(self):
        return f'<Stream type={self.stream_type} note={self.format_note} id={self.id}>'    


class StreamQuery:
    def __init__(self,data,type_:StreamTypes='none'):
        self.data = data
        self.audio = []
        self.adaptive = []
        self.progressive = []
        self.adaptive_resolutions = []
        self.progressive_resolutions = []
        self.segregate_streams(type_)
        # self.listprint("Audio",self.audio)
        # self.listprint("Adaptive",self.adaptive)
        # self.listprint("Progressive",self.progressive)
    
                
    def listprint(self,name,lst):
        print(name)
        for i in lst:
            print(i)
        print()
            
    def segregate_streams(self,type_=0):
        # type_ 0 - No change ; 1 - Audio ; 2 - Adaptive ; 3 - Progressive
        for i in self.data.get('formats'):
            if i.get('format_note') == "storyboard":
                pass    
            else:
                if i.get('acodec') != "none" and i.get('vcodec') == "none" and (type_ == 'none' or type_ == 'audio'): # Audio only
                    
                    # print('URL',i.get('url'))
                    st = Stream('audio',i.get('format_note'),i.get('format_id'),abr=i.get('abr'),url=i.get('url'),acodec=i.get('acodec'))
                    self.audio.append(st)
                    
                elif i.get('acodec') == "none" and i.get('vcodec') != "none" and (type_ == 'none' or type_ == 'adaptive'): # Adaptive
                    
                    if i.get('height') not in self.adaptive_resolutions:
                        self.adaptive_resolutions.append(i.get('height'))
                        st = Stream('adaptive',i.get('format_note'),i.get('format_id'),resolution=i.get('height'),url=i.get('url'),vcodec=i.get('vcodec'),)
                        self.adaptive.append(st)
                    
                
                elif i.get('acodec') != "none" and i.get('vcodec') != "none" and (type_ == 'none' or type_ == 'progressive'): # Progressive
                    
                    if i.get('height') not in self.progressive_resolutions:
                        self.progressive_resolutions.append(i.get('height'))
                        st = Stream('progressive',i.get('format_note'),i.get('format_id'),abr=i.get('abr'),resolution=i.get('height'),url=i.get('url'),vcodec=i.get('vcodec'),acodec=i.get('acodec'))
                        self.progressive.append(st)
  
        
class VideoDetails:
    def __init__(self,data) -> None:
        self.data = data
        self.title = None
    
    def get_title(self) -> str:
        self.title = self.data.get('title')
        return self.title
    
    def get_misc(self) -> tuple:
        # Returns a tuple of (url,title,thumbnail,duration,description,channel)
        self.url = self.data.get('webpage_url')
        self.title = self.title if self.title else self.get_title()
        self.thumbnail = self.data.get('thumbnail')
        self.duration = self.data.get('duration')
        self.description = self.data.get('description')
        self.channel = self.data.get('uploader')
        return (self.url,self.title,self.thumbnail,self.duration,self.description,self.channel)
    
    def get_detail(self,detail : str):
        if detail in self.data.keys():
            return self.data.get(detail)
        else:
            raise KeyError(f'Key {detail} not found in data')
        

if __name__ == '__main__':
    data = Data().get_data()
    q = StreamQuery(data)
    print(q.progressive)
    print(q.adaptive)
    p = VideoDetails(data)
    # print(p.get_misc())
