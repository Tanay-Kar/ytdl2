# ./modules/Query.py
#
# By: Tanay Kar
# Module for YTDL2
# 
# This file contains the Query class, which is used to query 
# the youtube link for details. This will be stored in a json
# file (./tmp/details.json) and will be used by the other modules.

import yt_dlp
import json


class LinkQuery:
    def __init__(self,link,verbose=False,yt_opts={}) -> None:
        self.link = link
        self.verbose = verbose
        self.yt_opts = yt_opts
        self.vprint = print if self.verbose else lambda *a, **k: None
        
    def query(self):
        with yt_dlp.YoutubeDL(self.yt_opts) as ydl:
            self.vprint(f"[QUERYING] : {self.link}")
            info = ydl.extract_info(self.link, download=False)
            self.vprint(f"[QUERYING] : {self.link} DONE")
            # ℹ️ ydl.sanitize_info makes the info json-serializable
            f = open('tmp/data.json','w')
            f.write(json.dumps(ydl.sanitize_info(info), indent=4))
            f.close()
            self.vprint(f"[WRITING QUERY] : {self.link} DONE")
            

if __name__ == '__main__':
    link = input("Enter link: ")
    q = LinkQuery(link,verbose=True)
    q.query()