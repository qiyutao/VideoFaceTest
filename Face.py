# coding=utf-8
from aip import AipFace
from PIL import Image,ImageDraw
import cv2

APP_ID = '10252037'
APP_KEY = 'k0Bh987vOSjVHHqh2sadh1kG'
SECRET_KEY = 'zc76jo7SbLxA4dFR5S0wn5GIIoclRtK0'

aipFace = AipFace(APP_ID,APP_KEY,SECRET_KEY)
frameNum = 1

def get_file_content(filePath) :
    with open(filePath,'rb') as fp:
        return fp.read()

def recogize(file) :
    img = Image.open(file)

    option = {
        'max_face_num':50,
        'face_fields': "age,beauty,expression,faceshape",
    }

    result = aipFace.detect(get_file_content(file),option)
    ls_loc =  result.get('result')

    for ls in ls_loc:
        loc = ls.get('location')

        x = loc.get('left')
        y = loc.get('top')
        width = loc.get('width')
        height = loc.get('height')

        print x,y,width,height


        draw = ImageDraw.Draw(img)

        draw.line([x,y,x+width,y,x+width,y+height,x,y+height,x,y],fill=(255,0,0),width=1)
        draw.text((x-5,y),str(round( ls.get('age'),1))+' '+str(round(ls.get('beauty'),1)))
    img.save(file)

def splitVideo(file) :
    global frameNum
    vc = cv2.VideoCapture(file)
    c = 1  
      
    if  vc.isOpened():
        rval ,  frame = vc.read()  
    else:  
        rval = False  
      
    timeF = 10
      
    while  rval:
        rval, frame = vc.read()  
        if (c % timeF  ==  0):
            cv2.imwrite('image/' + str(frameNum) + '.jpg', frame)
            frameNum = frameNum + 1
        c = c + 1  
        cv2.waitKey(1)  
    vc.release()

def mergerVideo() :
    img_root = 'image/'
    fps = 4

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter('saveVideo.avi',fourcc,fps,(1280,720))

    for i in range(1, frameNum):
        frame = cv2.imread(img_root + str(i) + '.jpg')
        videoWriter.write(frame)
    videoWriter.release()

splitVideo("1.mp4")

for i in range(1, frameNum) :
    recogize('image/'+str(i)+'.jpg')
    print '处理进度：'+str(round( i*1.0/frameNum,3)*100)+'%'

mergerVideo()