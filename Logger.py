#-*- coding: utf-8 -*-
'''
Created on 2012-1-29

@author: shuxiong
@modified by: jackieyang9
'''
import sys

def changeToLocalEncoding(string, fromEncoding='utf-8', toEncoding='utf-8'):
    string=str(string)
    return string.decode(fromEncoding).encode(toEncoding)

class Logger:
    '''
        this is a Logger, which outputs comments to stdout. 
    '''

    def __init__(self):
        pass
    
    def log(self, comment):
        comment=changeToLocalEncoding(comment, toEncoding=sys.stdout.encoding)
        sys.stdout.write(comment+'\n')

class BufferLogger:
    '''
        this is a Logger, which saves the last MAX_LINE comment to a buffer, 
        and outputs:
            1. if FILE is set, output comments to a file,
            2. else output comments to stderr
    '''
    # global member goes here
    #     BUFFER
    #     MAX_LINE
    #     FILE
    BUFFER=[]
    MAX_LINE=500
    FILE=None
    def __init__(self):
        pass
    
    def setMaxLine(self, maxLine):
        self.MAX_LINE=maxLine
    
    def setFile(self, fileName):
        self.FILE=fileName
    
    def log(self, comment):
        self.BUFFER.append(comment)
        # delete extra previous comment
        if len(self.BUFFER)>=2*self.MAX_LINE:
            self.BUFFER=self.BUFFER[len(self.BUFFER)-self.MAX_LINE:]
    
    def output(self):
        # delete extra previous comment
        if len(self.BUFFER)>self.MAX_LINE:
            self.BUFFER=self.BUFFER[len(self.BUFFER)-self.MAX_LINE:]
        # choose output to a file or stderr
        if self.FILE==None:
            out=sys.stderr
            encoding=sys.stderr.encoding
        else:
            out=open(self.FILE,'w')
            encoding='utf-8'
        # output comment
        for comment in self.BUFFER:
            comment=changeToLocalEncoding(comment, toEncoding=encoding)
            out.write(comment)
            out.write("\n")
        # close file
        if out!=sys.stderr:
            out.close()
            

class DebugLogger:
    '''
        this is a Logger, which outputs comments to stderr. 
    '''

    def __init__(self):
        pass

    # logging comment        
    def log(self, comment):
        comment=changeToLocalEncoding(comment, toEncoding=sys.stderr.encoding)
        sys.stderr.write(comment)
        sys.stderr.write("\n")

class FileLogger:
    '''
        this is a Logger, which outputs comments to file. 
    '''

    def __init__(self, filename):
        self.fout = open(filename, 'w')
        pass

    # logging comment        
    def log(self, comment):
        self.fout.write(comment + "\n")

class NoneLogger:
    '''
        this is a Logger, which takes no actions with comments. 
    '''
    def __init__(self):
        pass
    
    def log(self, comment):
        pass

if __name__=="__main__":
    l=BufferLogger()
    l.setMaxLine(2)
    l.setFile("test")
    l.log(1)
    l.log(2)
    l.log(3)
    l.log(4)
    l.output()