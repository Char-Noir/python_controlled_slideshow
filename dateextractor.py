from datetime import datetime
from PIL import Image
import os;
import json
#import time
 
def getTime(fn):
    return datetime.utcfromtimestamp(os.path.getmtime(fn)).strftime('%Y-%m-%d %H:%M:%S') 

def imgDate(fn):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    print(fn)        
    exif = Image.open(fn)._getexif()
 
    for t in tags:
        dat = exif.get(t[0])
 
        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat = dat[0] if type(dat) == tuple else dat
        if dat != None: break
 
    if dat == None: return None
    T = dat
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return T

folder_dir = "images"
files = []
for images in os.listdir(folder_dir):
 
    # check if the image ends with png
    if (images.endswith(".jpg") or images.endswith(".png")):
        files.append({
            "file":images,
            "date":getTime(folder_dir+'\\' + images),
            "type":"image"
        })
    if (images.endswith(".gif") or images.endswith(".GIF")):
        files.append({
            "file":images,
            "date":getTime(folder_dir+'\\' + images),
            "type":"gif"
        })
    if (images.endswith(".mp4") or images.endswith(".mov")):
        files.append({
            "file":images,
            "date":getTime(folder_dir+'\\' + images),
            "type":"video"
        })


newlist = sorted(files, key=lambda d: d['date'])    

file = open("image.json","w")

file.write(json.dumps(newlist));