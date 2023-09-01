# reads /example/data.json
import json
import pprint
'''import all_details_query
print('Details extracted from yt_dlp')'''

from typing import Literal

StreamTypes = Literal["audio", # Audio only
                      "progressive", # Video + Audio
                      "adaptive", # Video only
                    ]

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
    def __init__(self,data):
        self.data = data
        self.audio = []
        self.adaptive = []
        self.progressive = []
        self.adresolutions = []
        self.prresolutions = []
        self.segregate_streams()
        self.listprint("Audio",self.audio)
        self.listprint("Adaptive",self.adaptive)
        self.listprint("Progressive",self.progressive)
    
    def listprint(self,name,lst):
        print(name)
        for i in lst:
            print(i)
        print()    
    def segregate_streams(self,type_=0):
        # type_ 0 - No change ; 1 - Audio ; 2 - Adaptive ; 3 - Progressive
        for i in data.get('formats'):
            if i.get('format_note') == "storyboard":
                pass    
            else:
                if i.get('acodec') != "none" and i.get('vcodec') == "none" and (type_ == 0 or type_ == 1):
                    
                    # print('URL',i.get('url'))
                    st = Stream('audio',i.get('format_note'),i.get('format_id'),abr=i.get('abr'),url=i.get('url'),acodec=i.get('acodec'))
                    self.audio.append(st)
                    
                elif i.get('acodec') == "none" and i.get('vcodec') != "none" and (type_ == 0 or type_ == 2):
                    
                    # print('URL',i.get('url'))
                    if i.get('height') not in self.adresolutions:
                        self.adresolutions.append(i.get('height'))
                        st = Stream('adaptive',i.get('format_note'),i.get('format_id'),resolution=i.get('height'),url=i.get('url'),vcodec=i.get('vcodec'),)
                        self.adaptive.append(st)
                    
                
                elif i.get('acodec') != "none" and i.get('vcodec') != "none" and (type_ == 0 or type_ == 3):
                    
                    if i.get('height') not in self.prresolutions:
                        self.prresolutions.append(i.get('height'))
                        st = Stream('progressive',i.get('format_note'),i.get('format_id'),abr=i.get('abr'),resolution=i.get('height'),url=i.get('url'),vcodec=i.get('vcodec'),acodec=i.get('acodec'))
                        self.progressive.append(st)
                    # print('URL',i.get('url'))
                    
  
        


with open('examples/data.json','r') as f:
    data = json.load(f)
                        
sq = StreamQuery(data)
print(sq.adresolutions)
print(sq.prresolutions)