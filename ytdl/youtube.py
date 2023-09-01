# ./modules/Downloader.py
#
# By: Tanay Kar
# Module for YTDL2
#
# This file contains the Youtube class , which combines 
# the Query and Details modules to provide a single interface
# for the user to interact with. It also contains the Downloader
# class, which is used to download the video.

from .Query import LinkQuery
from .Details import StreamQuery,Data,VideoDetails,Stream
from typing import Literal

StreamType = Literal["audio","video"]

class Youtube():
    def __init__(self,link) -> None:
        self.link = link
        self.data = None
        self.details = None
        self.streams = None
        self.adaptive = None
        self.progressive = None
        self.audio = None
        self._get_data()
        self._get_details()
        self._get_streams()
    
    def _get_data(self):
        LinkQuery(self.link).query()
        self.data = Data().get_data()
    
    def _get_details(self):
        self.details = VideoDetails(self.data).get_misc()
    
    def _get_streams(self):
        self.streams = StreamQuery(self.data)
        self.adaptive_streams = self.streams.adaptive
        self.progressive_streams = self.streams.progressive
        self.adaptive_resolutions = self.streams.adaptive_resolutions
        self.progressive_resolutions = self.streams.progressive_resolutions
        self.audio = self.streams.audio
    
    def _search_stream(self,resolution):
        if resolution in self.progressive_resolutions:
            for i in self.progressive_streams:
                if i.resolution == resolution:
                    return i
        elif resolution in self.adaptive_resolutions:
            for i in self.adaptive_streams:
                if i.resolution == resolution:
                    return i
        else:
            raise Exception(f"Resolution {resolution} not found")
                
    def download(self,resolution=None,type_:StreamType="video"):
        if type_ == "video":
            if resolution:
                dl = Downloader(self,self._search_stream(resolution),type_)
                    
            else:
                print('Downloading best video')
    
    def __repr__(self):
        return f'<Youtube link={self.link}>'

class Downloader():
    def __init__(self,yt:Youtube,stream:Stream,type_:StreamType="video") -> None:
        self.yt = yt
        self.stream = stream
        self.type_ = type_
        self.stream_type = stream.stream_type
        self._download(self.stream)
    
    def _get_audio(self):
        best_audio = self.yt.audio[-1]
        print(best_audio)
            
    def _download(self,stream):
        print(self.stream.url)

if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=Slq4aeE8FoE"
    yt = Youtube(link)
    '''print(yt.adaptive)
    print(yt.progressive)
    print(yt.audio)
    # print(yt.details)
    print(yt.streams)'''
    print(yt.audio)
