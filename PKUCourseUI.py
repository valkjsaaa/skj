#-*- coding: utf-8 -*-
'''
Created on 2012-1-29

@author: shuxiong
@modified by: jackieyang9
'''
from PKUCourse import PKUCourse
from Logger import BufferLogger
from Logger import Logger as stdout 
from multiprocessing import Pool

import traceback

class PKUCourseUI:
    '''
        This is PKUCourseUI.
    '''
    # global member goes here
    #     PKUCOURSE
    PKUCOURSE=None
    STDOUT=None
    STUDENT_NO=None
    PASSWORD=None

    
    # call init() first

    def __init__(self):

        pass
    
    def init(self):
        self.PKUCOURSE=PKUCourse()
        self.STDOUT=stdout()
        
    def welcome(self):
        while True:
            self.STDOUT.log("输入学号")
            studentNo=raw_input()
            self.STDOUT.log("输入密码")
            password=raw_input()
            self.STDOUT.log("确认信息，学号=%s，输入y确定，区分大小写，其他重新输入"%(studentNo))
            temp=raw_input()
            if temp=='y':
                break
        self.STUDENT_NO=studentNo
        self.PASSWORD=password
        pass
    
    def loginAndGetClassInf(self):
        self.PKUCOURSE.login(self.STUDENT_NO,self.PASSWORD)
        pass

    def displayClassInf(self, classInfArray=None):
        if classInfArray==None:
            classInfArray=self.PKUCOURSE.getAllClassInformation()
        for classInf in classInfArray:
            self.STDOUT.log("\tindex=%s,seq=%s,name=%s，classid=%s，addr=%s"%(classInf['index'],classInf['seq'],classInf['name'],classInf['classid'],classInf['addr']))
        return classInfArray 
        
        
    def chooseSupplyClass(self):
        while True:
            self.STDOUT.log("当前选课列表")
            fullClassArray=self.displayClassInf()
            self.STDOUT.log("选择刷的课，输入index，一行一个，空行结束")
            chooseArray=[]
            while True:
                temp=raw_input()
                if temp=='':
                    break
                chooseArray.append(temp)
            chooseClassArray=[]
            for temp in chooseArray:
                found=False
                fCls=None
                for cls in fullClassArray:
                    if str(cls['index'])==str(temp):
                        found=True
                        fCls=cls
                        break
                if found:
                    chooseClassArray.append(fCls)
            self.STDOUT.log("刷课列表")
            self.displayClassInf(chooseClassArray)
            self.STDOUT.log("确定输入y")
            temp=raw_input()
            if temp=='y':
                break
        return chooseClassArray
    
    def trySupplyClass(self,clsInfArray):
        times = 0
        while True:
            times = times + 1
            self.STDOUT.log(times)
            self.STDOUT.log(':')
            self.STDOUT.log("当前刷课列表")
            self.displayClassInf(clsInfArray)
            self.PKUCOURSE.supplyCourse(clsInfArray)
            #消除刷上得课
            tempInfArray=[]
            fullClassArray=self.PKUCOURSE.getAllClassInformation()
            for cls in clsInfArray:
                for cls2 in fullClassArray:
                    if cls['seq']==cls2['seq'] and cls['name']==cls2['name'] and cls['classid']==cls2['classid']:
                        tempInfArray.append(cls2)
                        break
            clsInfArray=tempInfArray
            if len(clsInfArray)==0:
                break

if __name__=='__main__':
    logger=BufferLogger()
    logger.setMaxLine(500)
    logger.setFile('errorInf')
    try:
        # pool = Pool()
        ui=PKUCourseUI()
        ui.init()
        ui.welcome()
        ui.loginAndGetClassInf()
        chooseClassInfArray=ui.chooseSupplyClass()
        for cls in chooseClassInfArray:
            cls['available']=False
        print chooseClassInfArray
        # pool.apply_async(ui.trySupplyClass,[ui,chooseClassInfArray])
        # pool.apply_async(ui.trySupplyClass,[ui,chooseClassInfArray])
        ui.trySupplyClass(chooseClassInfArray)
        while True:
            continue
    except Exception,e:
        logger.log(traceback.format_exc())
        logger.output()
        print traceback.format_exc()
        pass