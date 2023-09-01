import time
import json
import re

t1 = round(time.time())
print(t1)

with open('examples/data.json','r') as f:
    data = json.loads(f.read())
    
url = data['formats'][3]['url']

t2 = int(re.findall(r'\?expire=(\d+)&',url)[0])
print(t2,' ',t1,' ',t2-t1)

days = t2 // 86400
hours = t2 // 3600 % 24
minutes = t2 // 60 % 60
seconds = t2 % 60

print(f'{hours} hrs ; {minutes} min ; {seconds} s')