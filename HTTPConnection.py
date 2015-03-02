#-*- coding: utf-8 -*-
'''
Created on 2012-1-29

@author: shuxiong
@modified by: jackieyang9
'''

import copy
import urllib
import httplib
import platform

#from Logger import DebugLogger as Logger
from Logger import BufferLogger as Logger

class HTTPConnection:
    '''
        This is an HTTP connection. 
    '''
    
    # global value
    # const var
    HEADER_HOST = ('Host', 'elective.pku.edu.cn')
    HEADER_ACCEPT_TEXT = ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    HEADER_ACCEPT_PNG = ('Accept', 'image/png,image/*;q=0.8,*/*;q=0.5')
    HEADER_COOKIE = ('Cookie', '')
    DEFAULT_HEADER_WIN = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
        'Accept-Language':'en-us,en;q=0.5',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive':'115',
        'Connection':'keep-alive',
                    }
    DEFAULT_HEADER_LINUX = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
        'Accept-Language':'en-us,en;q=0.5',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive':'115',
        'Connection':'keep-alive',
    }

    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    
    IS_WINDOWS = platform.system().lower() == 'windows'
    
    # private value
    
    # connection cookie
    # self.mCookie
    # self.mHost 
    
    # logger
    logger = Logger()

    def __init__(self, host):
        '''
        Constructor
        '''
        self.mCookie = {}
        self.mHost = ('Host', copy.deepcopy(host))
        

    def setMHost(self, host):
        self.mHost = ('Host', copy.deepcopy(host))
        
    def addCookie(self, key, value):
        self.mCookie[key] = value

    def request(self, extraHeaders, extraParams, method, url):
        # configure params
        params = {}
        for (key, value) in extraParams:
            params[key] = value
        params = urllib.urlencode(params)

        # configure header
        if self.IS_WINDOWS:
            headers = copy.copy(self.DEFAULT_HEADER_WIN)
        else:
            headers = copy.copy(self.DEFAULT_HEADER_LINUX)
        # header cookie here
        if len(self.mCookie.keys()) > 0:
            tmp = ''
            for (key, value) in self.mCookie.items():
                tmp = tmp + ';' + key + '=' + value
            headers['Cookie'] = tmp[1:]
        # content type & length here
        if method==self.METHOD_POST and len(params)>0:
            headers['Content-type']='application/x-www-form-urlencoded'
            headers['Content-length']=str(len(params))
        # host
        headers[self.mHost[0]] = self.mHost[1]
        # other headers
        for (key, value) in extraHeaders:
            headers[key] = value
        
        self.logger.log("-----------------------begin-----------------------")
        self.logger.log("Requesting method=%s url=%s" % (method, url))
        self.logger.log("\theader=")
        for key in headers.items():
            self.logger.log("\t\t%s," % str(key))
        self.logger.log("\tparams=" + str(params))
        
        conn = httplib.HTTPConnection(headers['Host'])
        conn.request(method, url, params, headers)
        result = conn.getresponse()
        #conn.close()
        
        self.logger.log("\tresult=%d %s" % (result.status, result.reason))
        self.logger.log("------------------------end------------------------")
        
        # add cookie
        if result.status == 200: 
            tempCookie = result.getheader('Set-Cookie')
            if tempCookie:
                self.logger.log("tempCookie=%s"%tempCookie)
                tempArray = tempCookie.split('; ')
                for tempCookie in tempArray:
                    temp = tempCookie.split('=')
                    key = temp[0]
                    value = temp[1]
                    # 设置cookie
                    if key != 'path':
                        self.addCookie(key, value)
        #print result
                
        return result

    def requestReliable(self, extraHeaders, extraParams, method, url):
        while True:
            try:
                result=self.request(extraHeaders, extraParams, method, url)
                if result.status==200:
                    break
            except:
                self.logger.log("connection exception!")
        return result

if __name__ == '__main__':
    
    # login here
    con = HTTPConnection('elective.pku.edu.cn')
    
    headers = [con.HEADER_ACCEPT_TEXT]
    params = []
    url = '/elective2008/edu/pku/stu/elective/controller/loginServlet/login.jsp'
    result = con.request(headers, params, con.METHOD_GET, url)
