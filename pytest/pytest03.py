from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import numpy as np
import argparse
from PIL import Image
import os
import sys
import imagehash

path = "C:/Users/covin/Desktop/hdev/img"


def files():
    file_names = os.listdir(path)
    
    global imgs
    imgs = []
    global imgdict
    imgdict = {}
    global hashes
    hashes = {}
    
    for filename in file_names:
        
        if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".webp": #or os.path.splitext(filename)[1] == ".gif":

            fullpath = path+"/"+filename

            img_array = np.fromfile(fullpath,np.uint8)    
            
            img = cv2.imdecode(img_array,cv2.IMREAD_UNCHANGED)
            
            hash = imagehash.average_hash(Image.open(fullpath))
            
            hashes[filename] = hash
            
            print(filename,hashes[filename])
            
            if(len(imgdict)>0):
                dimg = list(imgdict.values())[-1]
                dheight, dwidth = dimg.shape[:2]
                height, width = img.shape[:2]
                if(height*width<dheight*dwidth):
                    for i,(dfname,dimage) in enumerate(imgdict.items()):
                        resizeimg = cv2.resize(dimage,dsize=(height,width),interpolation=cv2.INTER_LINEAR)
                        imgdict[dfname] = resizeimg
                elif(height*width>dheight*dwidth):
                    resizeimg = cv2.resize(img,dsize=(dheight,dwidth),interpolation=cv2.INTER_LINEAR)
                    imgdict[filename] = resizeimg
                else:
                    imgs.append(img)
                    imgdict[filename] = img
            else:
                imgs.append(img)
                imgdict[filename] = img
            
##히스토그램    

def hist():
    histdict = {}
    for i,(filename,img) in enumerate(imgdict.items()):
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        hist = cv2.calcHist([hsv], [0,1], None, [180 ,256], [0,180,0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        histdict[filename] = hist
    ##Dict 사용하여 file이름까지 추가
    histdictcount = len(histdict)
    for x in range(histdictcount):
        firstkey = list(histdict.keys())[0]
        standardimg = histdict.get(firstkey)
        
        print("기준 이미지: "+firstkey)
        
        del histdict[firstkey]

        methods = {'INTERSECT':cv2.HISTCMP_INTERSECT,
            'BHATTACHARYYA':cv2.HISTCMP_BHATTACHARYYA}
        matched = set()

        
        
        for j, (name, flag) in enumerate(methods.items()):
            print('%-10s'%name, end='\t')
            for i, (filename,hist) in enumerate(histdict.items()):
                #---④ 각 메서드에 따라 img1과 각 이미지의 히스토그램 비교
                ret = cv2.compareHist(standardimg, hist, flag)
                if flag == cv2.HISTCMP_INTERSECT: #교차 분석인 경우 
                    ret = ret/np.sum(standardimg)        #비교대상으로 나누어 1로 정규화
                print(filename+":%7.2f"% (ret), end='\t')
                

                
                if(name == 'INTERSECT' and ret<0.9):
                    print('불일치\n')
                elif(name == 'INTERSECT' and ret>0.9):
                    print('일치\n')
                    matched.add(filename)
                
                if(name == 'BHATTACHARYYA' and ret>0.1):
                    print('불일치\n')
                elif(name == 'BHATTACHARYYA' and ret<0.1):
                    print('일치\n')
                    matched.add(filename)
        print(matched)
    
    
    
##compare_ssim
def compare_ssims():
    for j in range(len(imgdict)):
        firstkey = list(imgdict.keys())[0]
        standardimg = imgdict.get(firstkey)
        del imgdict[firstkey]
        for i,(filename,img) in enumerate(imgdict.items()):
            grayA = cv2.cvtColor(standardimg, cv2.COLOR_BGR2GRAY)
            grayB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            (score, diff) = compare_ssim(grayA, grayB, full=True)
            print(firstkey+"&"+filename + f" SSIM: {score}")

def dhash():
    for j in range(len(imgdict)):
        firstkey = list(imgdict.keys())[0]
        standardimg = imgdict.get(firstkey)
        del imgdict[firstkey]
        for i,(filename,hash) in enumerate(hashes.items()):
            if(hashes[firstkey] == hashes[filename]):
                print(firstkey+"&"+filename+" 일치")
            else:
                print(firstkey+"&"+filename+" 불일치")
                
files()
hist()
compare_ssims()
dhash()