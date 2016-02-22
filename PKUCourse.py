#-*- coding: utf-8 -*-
'''
Created on 2012-1-29

@author: shuxiong
@modified by: jackieyang9
'''

import re
import pkucaptcha

from HTTPConnection import HTTPConnection
from ValidCodeAnalyzer import ValidCodeAnalyzer
#from Logger import DebugLogger as Logger 
from Logger import BufferLogger as Logger
import requests
import random

class PKUCourse:
    
    # global member goes here
    MAX_FAIL_TIME=10
    
    # class member goes here
    #     self.mLogger
    #     self.mConnection    
    
    def __init__(self):
        self.mLogger=Logger()
        self.mConnection=HTTPConnection('elective.pku.edu.cn')

    def __getLoginPage(self):
        # get content
        headers = [self.mConnection.HEADER_ACCEPT_TEXT]
        params = []
        url = '/elective2008/edu/pku/stu/elective/controller/loginServlet/login.jsp'
        result = self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        # check result
        data=result.read()
        tempArr=re.findall(r'<title>(.*?)</title>',data)
        if len(tempArr)>0 and tempArr[0]=='学生选课用户登录':
            self.mLogger.log("__getLoginPage OK")
            return True
        else:
            self.mLogger.log("__getLoginPage Fail")
            return False
        
    
    def __getValidCode(self, Referer=None):
        # get content
        headers = [self.mConnection.HEADER_ACCEPT_PNG]
        if Referer!=None:
            headers.append(('Referer',Referer))
        params = [('Rand', 4583.84093823875)]
        url = '/elective2008/DrawServlet'
        result= self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        data = result.read()
        #validCode = ValidCodeAnalyzer(data).analyze()
        # save the picture
        fileName='./code.jpg'
        f=open(fileName,'wb')
        f.write(data)
        f.close()
        validCode = pkucaptcha.identify(fileName)
        print validCode
        # check result
        validCode=str(validCode)
        passed=len(validCode)==4
        if passed:
            self.mLogger.log("__getValidCode OK, vc="+validCode)
            return validCode
        else:
            self.mLogger.log("__getValidCode Fail, vc="+validCode)
            return None
    
    def __getVerifyPage(self, studentNo, password, validCode):
        # get content
        headers = [self.mConnection.HEADER_ACCEPT_TEXT]
        params = [('uid',studentNo),('psd',password),('validCode',validCode),('subBtn','\xE7\x99\xBB\xE5\xBD\x95')]
        url='/elective2008/edu/pku/stu/elective/controller/loginServlet/login_webservicehandle.jsp'
        result=self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_POST, url)
        # check result
        data=result.read()
		#print data
        tempArr=re.findall(r"<p class='pkuportal-remark'>网上选课 >> 帮助： 【(.*?)】</p>",data)
        if len(tempArr)>0:
            self.mLogger.log("__getVerifyPage OK, "+tempArr[0])
            return (True,tempArr[0])
        else:
            self.mLogger.log("__getVerifyPage Fail")
            return (False,None)
            
    def __getLoginPage2(self,url):
        # get content
        headers = [self.mConnection.HEADER_ACCEPT_TEXT]
        params = []
        result = self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        # check result
        data=result.read()
        tempArr=re.findall(r'<title>(.*?)</title>',data)
        print data
        if len(tempArr)>0 and tempArr[0]=='帮助-总体流程':
            self.mLogger.log("__getLoginPage2 OK")
            return True
        else:
            self.mLogger.log("__getLoginPage2 Fail")
            return False
    def __getVerifyPage2(self):
        headers=[self.mConnection.HEADER_ACCEPT_TEXT]
        params = []
        url = '/elective2008/edu/pku/stu/elective/controller/help/HelpController.jpf'
        result = self.mConnection.requestReliable(headers, params, self. mConnection.METHOD_GET,url)
        data=result.read()
        tempArr=re.findall(r'<title>(.*?)</title>',data)
        #print data
        if len(tempArr)>0 and tempArr[0]=='帮助-总体流程':
            self.mLogger.log("__getLoginPage2 OK")
            return True
        else:
            self.mLogger.log("__getLoginPage2 Fail")
            return False

    def login(self, studentNo, password):
    # try until login successfully, and return personal information
	print 'start login'
        while True:
            # get Login page
            #result=self.__getLoginPage()
            #if not result:
            #    continue
            # get Valid Code on Login Page
            #validCode=self.__getValidCode()
            #if validCode==None:
            #    continue
            # submit student ID & password, Login
            redirectURL= "http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do"
            payload = {
                'appid':'syllabus',
                'userName':'1200012727',
                'password': 'Oncall36',
                'randCode':'012345',
                'smsCode':'smsCode',
                'redirUrl': redirectURL
            }
            r = requests.post('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do', data=payload)
            token = r.json()['token']
            print "login token: %s"%token
            redirect = redirectURL + "?rand=" + str(random.randint(0, 10000)) + "&token=" + token
            print "redirectURL: %s"%redirect

            result = self.__getLoginPage2(redirect)
            if result:
                print 'login sucessfully!'
            
            result = self.__getVerifyPage2()
            if result:
                #print 'login sucessfully!'
                break
        self.__getVerifyPage2()
        info = ""
        self.mLogger.log("Login Successfully!")
        return info
    
    def getValidCode(self):
        while True:
            validCode=self.__getValidCode()
            if validCode!=None:
                break
        return validCode
    
    def __getClassInformation(self, data, g_courseInf):
        #print data
        start=data.index(r'<table class="datagrid" width="100%">')
        end=data.index(r'</table>',start)
        data=data[start:end]
        #print data
        allCourse=re.findall(r'<tr class="datagrid\-[eo].*?">.*?</tr>',data)
        #print allCourse
        #print '\n'
        #print '\n'
        #print '\n'
        for i in range(len(allCourse)):
            courseInf={}
            #print allCourse[i];
            #print '\n'
            tempArr=re.findall(r'<td.*?</td>',allCourse[i])
            #print tempArr

            courseInf['index']=len(g_courseInf)
            #print tempArr[0]
            start=tempArr[0].index('course_seq_no=')+len('course_seq_no=')
            end=tempArr[0].index('"',start)
            courseInf['seq']=tempArr[0][start:end]

            start=tempArr[0].index('<span>')+len('<span>')
            end=tempArr[0].index('</span>',start)
            courseInf['name']=tempArr[0][start:end]

            start=tempArr[5].index('<span style="width: 30">')+len('<span style="width: 30">')
            end=tempArr[5].index('</span>',start)
            courseInf['classid']=tempArr[5][start:end]
            #print tempArr[10]
            start=tempArr[10].index('<span>')+len('<span>')
            end=tempArr[10].index('</span>',start)
            courseInf['available']=tempArr[10][start:end]=='补选'
            #print courseInf['available']
            courseInf['addr']=re.findall(r'<span .*?>(.*?)</span>',tempArr[8])[0]

            g_courseInf.append(courseInf)
    
    def __getAllClassInformation(self):
        # get content
        headers = [self.mConnection.HEADER_ACCEPT_TEXT]
        params = []
        url='/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do'
        result=self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        # check result
        data=result.read()
        data=data.replace('\n','')
        data=data.replace('\r','')
        data=data.replace('\t','')
        dataBackup=data
        
        g_courseInf=[]
        self.__getClassInformation(data, g_courseInf)

        # 后面判断选课列表是否超过20门课
        while True:
            data=dataBackup
            data=data[data.index('Previous'):]
            tempArr=re.findall(r'<a href="/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp(.*?)">Next</a>',data)
            self.mLogger.log(str(tempArr))
            if len(tempArr)<=0:
                break
            tempArr[0]=tempArr[0].replace('&amp;','&')
            #注意复制dataBackup
            headers = [self.mConnection.HEADER_ACCEPT_TEXT]
            params = []
            url='/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp'+tempArr[0]
            result=self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
            data=result.read()
            data=data.replace('\n','')
            data=data.replace('\r','')
            data=data.replace('\t','')
            dataBackup=data
            self.__getClassInformation(data, g_courseInf)
            
            
        '''
        <a href="/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&amp;netui_row=electableListGrid%3B20">Next</a>
        '''
        # 这里输出全部课程信息            
        self.mLogger.log("全部课程信息")
        for courseInf in g_courseInf:
            self.mLogger.log("\tindex=%s,seq=%s,name=%s,addr=%s"%(courseInf['index'],courseInf['seq'],courseInf['name'],courseInf['addr']))
        return g_courseInf

    def getAllClassInformation(self):
        return self.__getAllClassInformation()
    
    def __valid(self, validCode):
        headers = [self.mConnection.HEADER_ACCEPT_TEXT,('Referer','http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do')]
        params = []
        #params = [('validCode',validCode)]
        #url='/elective2008/edu/pku/stu/elective/controller/supplement/validate.do'
        print 'the validCode now is'
        print validCode
        url='/elective2008/edu/pku/stu/elective/controller/supplement/validate.do?validCode='+str(validCode)
        result=self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        data=result.read()
        # print data
        if data.find('<valid>2</valid>')!=-1:
            self.mLogger.log("suc to validate!!")
            self.mLogger.log(data)                        
            return True
        else:
            self.mLogger.log("fail to validate!!")
            self.mLogger.log(data)
        return False
        
    def __supplyCourse(self, courseInf):
        index=courseInf['index']
        seq=courseInf['seq']
        name=courseInf['name']
        print '选课中\n'
        self.mLogger.log("正在选index=%s,seq=%s,name=%s"%(index,seq,name))

        while True:        
            validCode=self.__getValidCode("http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do")
            if self.__valid(validCode):
                break

        headers = [self.mConnection.HEADER_ACCEPT_TEXT,('Referer','http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do')]
        #params = [('index',index),('seq',seq)]
        params=[]
        url='/elective2008/edu/pku/stu/elective/controller/supplement/electSupplement.do?index=%s&seq=%s'%(index,seq)
        print url
        result=self.mConnection.requestReliable(headers, params, self.mConnection.METHOD_GET, url)
        return result
    
    def supplyCourse(self, courseInfArray):
        for courseInf in courseInfArray:
            if courseInf['available']:
                self.__supplyCourse(courseInf)

if __name__=='__main__':
    temp=PKUCourse()
    temp.login('','')
    courseInfArray=temp.getAllClassInformation()
    for cls in courseInfArray:
        print cls
    #temp.supplyCourse(courseInfArray)
    #courseInfArray=temp.getAllClassInformation()
