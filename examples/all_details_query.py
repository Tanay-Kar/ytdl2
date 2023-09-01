import json
import yt_dlp
import ytlink
URL = ytlink.URL

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    f = open('examples/data.json','w')
    f.write(json.dumps(ydl.sanitize_info(info), indent=4))
    f.close()
    
