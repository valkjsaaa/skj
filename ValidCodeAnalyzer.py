#-*- coding: utf-8 -*-
'''
Created on 2012-1-29

@author: shuxiong
@modified by: jackieyang9
'''
# from PIL import Image
from PIL import Image

class ValidCodeAnalyzer:
    '''
        this is a tool code with valid code in elective.pku.edu.cn
        takes in an image data, and return the valid code 
    '''
    
    # member goes here
    #     self.fileName
    #     self.dataFileName
    #     self.digitData
    
    def __init__(self, data):
        '''
        Constructor
        '''
        # save the picture
        self.fileName='/Users/Jackie/Downloads/src-1jackie/code.jpg'
        f=open(self.fileName,'wb')
        f.write(data)
        f.close()
        # read pre-save data
        self.dataFileName='/Users/Jackie/Downloads/src-1jackie/data'
        f=open(self.dataFileName,'r')
        self.digitData=[]
        for i in range(10):
            self.digitData.append([])
            f.readline()
            for j in range(13):
                self.digitData[i].append(f.readline())
                j=j # eliminate warning 
        f.close()
        
        
    def analyze(self):
        print self.fileName
        img=Image.open(self.fileName)
        (n,m)=img.size
        newImgPixel=[]
        for i in range(n):
            newImgPixel.append([0]*m)
        for i in range(n):
            for j in range(m):
                (r,g,b)=img.getpixel((i,j))
                if (r<=200 and g<=200 and b<=200):
                    newImgPixel[i][j]='0'
                else:
                    newImgPixel[i][j]='1'

        value=''
        for (p1,p2) in [(3,11),(14,22),(25,33),(36,44)]:
            tempMax=0
            tempAns=0
            for k in range(0,10):
                tempSum=0
                for j in range(2,15,1):
                    for i in range(p1,p2,1):
                        if self.digitData[k][j-2][i-p1]==newImgPixel[i][j]:
                            tempSum+=1
                if tempMax<tempSum:
                    tempMax=tempSum
                    tempAns=k
            value+=str(tempAns)
        return value
        