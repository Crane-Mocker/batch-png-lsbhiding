#c0conut 2020.12.21
#Generate random bit stream to implement batch png lsbhiding
#Embedding rate 80%
#Coverimage : 512*512 png
import numpy as np 
import base64, json, random, os
from bitstring import BitArray
from cv2 import cv2 as cv

def genEmbedBinStream():
    #generate random bit stream
    s = random.randint(0, 2**20000 - 1)
    #print("这是s:"+str(s)+"\n")
    binStreamList = list(bin(s))
    binStreamList.pop(0)
    binStreamList.pop(0)
    #print("这是binStreamList:"+str(binStreamList))
    return binStreamList

def streamNormalize(binStream): 
    #Normalize bit stream
    #make 01 proportion of the embedding stream 1:1
    #The length of bitstream would better be even
    #zeroPos, onePos store the 0s' and 1s' positions in binStream
    zeroPos = [ pos for pos in range(len(binStream)) if binStream[pos] == 0]
    # zeeoPos = [pos for pos,value in enumerate(binStream) if value == 0]
    onePos = [ pos for pos in range(len(binStream)) if binStream[pos] == 1]
    zeroScale = len(zeroPos)
    oneScale = len(onePos)
    #which is more, 0 or 1
    flag = 1 if oneScale > zeroScale else 0
    appendScale = abs(oneScale - zeroScale)//2
    key = [flag,] # which is more before processing
    if flag: # more 1
        key+= [i for i in random.sample(onePos,appendScale)]
        for pos in key[1:]:
            binStream[pos]=0
    else: # more 0
        key+= [i for i in random.sample(zeroPos,appendScale)]
        for pos in key[1:]:
            binStream[pos]=1
    with open('keyPos.json','w') as fp:
        json.dump(key,fp)
    return binStream

def binReplace(x:int,b:str,pos:int)->int:
    #replace 0 or 1
    if b not in ['0','1']:
        print('b must be "0" or "1" !')
        return
    x = bin(x)[2:]
    if len(x) != 8: # must to be 8 bit
        x= '0'*(8 - len(x)) + x 
    # xbinList = [ x[i] for i in range(len(x))]
    xbinList = list(x)
    # print(xbinList)
    xbinList[len(x) - pos] = b
    # print(xbinList)
    return int(''.join(xbinList),2)

def embeding(imgCover,binStreamList,embedZone,bitPlane=1):
    for coordinate, embedBin in zip(embedZone,binStreamList):
        tmp = imgCover.item(coordinate[0],coordinate[1])
        replace = binReplace(tmp,str(embedBin),bitPlane) 
        # input should be str()
        # imgCover.itemset(coordinate,replace)
        # a = imgCover[coordinate[0]][coordinate[1]]
        imgCover[coordinate[0]][coordinate[1]]=replace
    return imgCover

# embedZone generator(random)
def genRandEmbedZone(imgCoverPath): 
    imgCover = cv.imread(imgCoverPath,cv.IMREAD_GRAYSCALE)
    binStreamScale = len(genEmbedBinStream())
    rowScale = imgCover.shape[0]
    columnScale = imgCover.shape[1]
    zone = []
    for i in range(rowScale):
        for j in range(columnScale):
            zone.append(tuple([i,j]))
    return random.sample(zone,binStreamScale)

# embedZone generator (random)
def genNormalZone(imgCoverPath):
    imgCover = cv.imread(imgCoverPath,cv.IMREAD_GRAYSCALE)
    binStreamScale = len(genEmbedBinStream())
    rowScale = imgCover.shape[0]
    columnScale = imgCover.shape[1]
    zone = [] # pix of imageCover
    for i in range(rowScale):
        for j in range(columnScale):
            zone.append(tuple([i,j]))
    return random.sample(zone[:binStreamScale],binStreamScale)
    # return zone[:binStreamScale] # 直接依次嵌入，不做随机处理

def LSBembedding(imgCoverPath:str,embedZone:list,bitPlane=1): 
    imgCover = cv.imread(imgCoverPath,cv.IMREAD_GRAYSCALE)
    binStreamList = streamNormalize(genEmbedBinStream()) 
    # binStreamList too large?
    if len(binStreamList) > imgCover.shape[0]*imgCover.shape[1]:
        print('binStream is too large')
        return
    imgStego = embeding(imgCover,binStreamList,embedZone,bitPlane)
    imgCoverName = imgCoverPath[9:].split('.')[0]
    cv.imwrite('res_bin/'+str(index)+'_lsb_1.png',imgStego)
    print('LSB Embeding done!')
    return imgStego

if __name__ == "__main__":

    target_dir = os.walk("ori")#dir of cover image
    index = 1
    for path, dir_list, file_list in target_dir:
        for file_name in file_list:
            cur_target = os.path.join(path, file_name)
            imgCoverPath = cur_target
            bitPlane = 1
            embedZone = genNormalZone(imgCoverPath)
            with open('zone.json','w') as fp:
                json.dump(embedZone,fp)
            LSBembedding(imgCoverPath,embedZone,bitPlane=bitPlane)
            index += 1
