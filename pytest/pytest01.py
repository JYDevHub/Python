import os
import sys
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import matplotlib.pylab as plt
from skimage.metrics import structural_similarity as ssim
import argparse
from PIL import Image
import imagehash


##시나리오: 이미지를 순서대로 교체하면서 본 이미지를 제외한 이미지들만을 비교

def filepath():
    path = "C:/Users/covin/Desktop/hdev/img"

    file_names = os.listdir(path)
    imgs = []
    for filename in file_names:
        
        if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".webp" or os.path.splitext(filename)[1] == ".gif":
            print(os.path.splitext(filename)[0])
            #이미지 흑백으로 변환
            fullpath = path+"/"+filename
            #한글경로 있을 시 변환
            img_array = np.fromfile(fullpath,np.uint8)
            #움짤인지 아닌지 판별
            # gif = cv2.VideoCapture(fullpath)
            # ret, frame = gif.read()
            
            # while gif.isOpened():
            #     if not ret:
            #         break
                
            #     cv2.imshow("root",frame)
                
            # gif.release()
            
            img = cv2.imdecode(img_array,cv2.IMREAD_UNCHANGED)
            
            imgs.append(img)            
        #     cv2.namedWindow("root",cv2.WINDOW_NORMAL)
        #     cv2.imshow("root",img)
        #     cv2.waitKey(5000)
        # cv2.destroyAllWindows()
        
    #히스토그램 예제
    # hists = []
    # for img in imgs:
    #     hsv = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #     hist = cv2.calcHist(hsv, [0, 1], None, [180, 256], [0, 180, 0, 256])
    #     cv2.normalize(hist,hist,0,1,cv2.NORM_MINMAX)
    #     hists.append(hist)
    
    # query = hists[0]
    
    # methods = ['CORREL', 'CHISQR', 'INTERSECT', 'BHATTACHARYYA', 'EMD']
    # np.seterr(divide='ignore',invalid='ignore')
    # for index, name in enumerate(methods):
    # # 비교 알고리즘 이름 출력(문자열 포맷팅 및 탭 적용)
    #     print('%-10s' % name, end = '\t')  
        
    #     # 2회 반복(2장의 이미지에 대해 비교 연산 적용)
    #     for i, histogram in enumerate(hists):
    #         ret = cv2.compareHist(query, histogram, index) 
    #         ## 교차 분석인 경우 
    #         ## 원본으로 나누어 1로 정규화
    #         if index == cv2.HISTCMP_INTERSECT:                   
    #             ret = ret/np.sum(query)                          
    #         print("img%d :%7.2f"% (i+1 , ret)+'\n', end='\t')
            
            
            
# filepath()

path = "C:/Users/covin/Desktop/hdev/img"

file_names = os.listdir(path)
imgs = []
imgdict = {}
hashes = []
for filename in file_names:
    
    if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".webp" or os.path.splitext(filename)[1] == ".gif":
        #print(os.path.splitext(filename)[0])
        #이미지 흑백으로 변환
        fullpath = path+"/"+filename
        #한글경로 있을 시 변환
        img_array = np.fromfile(fullpath,np.uint8)
        #움짤인지 아닌지 판별
        # gif = cv2.VideoCapture(fullpath)
        # ret, frame = gif.read()
        
        # while gif.isOpened():
        #     if not ret:
        #         break
            
        #     cv2.imshow("root",frame)
            
        # gif.release()        
        
        img = cv2.imdecode(img_array,cv2.IMREAD_UNCHANGED)
        
        #img = cv2.resize(img,dsize=(0,0),fx=0.5,fy=0.5,interpolation=cv2.INTER_LINEAR)
        
        #resizeimg = cv2.resize(img,dsize=(300,300),interpolation=cv2.INTER_AREA)
        
        #img = Image.open(fullpath)
        
        hash = imagehash.average_hash(Image.open(fullpath))
        print(str(hash),fullpath)
        hashes.append(hash)
        
        resizeimg = cv2.resize(img,dsize=(80,80),interpolation=cv2.INTER_LINEAR)
        
        #plt.imshow(img)
        #resizeimg = img.resize(img.size, Image.LANCZOS)
        
        height, width = resizeimg.shape[:2]
        
        imgs.append(resizeimg)
        imgdict[filename] = resizeimg
#print("해쉬: "+str(hashes[1]))
    
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
    # for fname in matched:
    #     del histdict[fname]

    
    
##원본코드

# hists = []
# for i, img in enumerate(imgs) :
#     plt.subplot(1,len(imgs),i+1)
#     plt.title('img%d'% (i+1))
#     plt.axis('off') 
#     plt.imshow(img[:,:,::-1])
#     #---① 각 이미지를 HSV로 변환
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     #---② H,S 채널에 대한 히스토그램 계산
#     hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0, 256])
#     #---③ 0~1로 정규화
#     cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
#     hists.append(hist)

#query = hists[0]
# methods = {'CORREL' :cv2.HISTCMP_CORREL, 'CHISQR':cv2.HISTCMP_CHISQR, 
#            'INTERSECT':cv2.HISTCMP_INTERSECT,
#            'BHATTACHARYYA':cv2.HISTCMP_BHATTACHARYYA}

# for j, (name, flag) in enumerate(methods.items()):
#     print('%-10s'%name, end='\t')
#     for i, (hist, img) in enumerate(zip(hists, imgs)):
        
#         #---④ 각 메서드에 따라 img1과 각 이미지의 히스토그램 비교
#         ret = cv2.compareHist(query, hist, flag)
#         if flag == cv2.HISTCMP_INTERSECT: #교차 분석인 경우 
#             ret = ret/np.sum(query)        #비교대상으로 나누어 1로 정규화
#         print("img%d:%7.2f"% (i+1 , ret), end='\t')
        
#         if(name == 'BHATTACHARYYA' and ret>0.1):
#             print('\n불일치')
#         elif(name == 'BHATTACHARYYA' and ret<0.1):
#             print('\n일치')
        
#     print()
#plt.show()