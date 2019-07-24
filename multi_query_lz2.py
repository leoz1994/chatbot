# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:02:21 2019

@author: Administrator
"""

import jieba
import re
import math
import xlrd
from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from random import sample
import GV

# ## 余弦距离
class Muli_query_methods_lz2:
    '''
    global MULTI_STATE
    global QUESTION_LIST
    global MAX_LEN
    global ANS_LIST
    global POSITION_LEN
    global FLAG
    global SHOW
    '''
    

    def __init__(self):
        pass
    
    
    def cosAB(self,listA,listB):
        
        resulttfdif=[]
        for i in range(len(listB)):
            #print(listA,'\n',listB[i])
            if len(listA)!=len(listB[i]) or len(listA)<1:
                return False
            Molecular,denominatorA,denominatorB,denominator=0,1,1,0
            for j in range(len(listA)):
                listA[j]=float(listA[j])
                listB[i][j]=float(listB[i][j])
                #print('A和B',listA[j],listB[i][j])
                Molecular=Molecular+(listA[j]*listB[i][j])
                #print(Molecular,'\n')
                denominatorA+=listA[j]*listA[j]
                denominatorB+=listB[i][j]*listB[i][j]
            denominator=Molecular/(math.sqrt(denominatorA)*math.sqrt(denominatorB))
            #print('分子分母',Molecular,denominatorA,denominatorB)
            #print(denominator,'\n')
            resulttfdif.append(denominator)
        #print('cos-result:',resulttfdif)
        return resulttfdif
    
    
    # ## 读取excel,分词
    
    
    
    def coreword(self,path):
        #wordlist:问题.labellist:问题分类.
        #numlist:二层分类.categylist:大类的数字(可优化)
        wordlist=[]
        labellist=[]
        numlist=[]
        categylist=[]
        ExcelFile=xlrd.open_workbook(path)
        sheet=ExcelFile.sheet_by_index(0)
        rownum=sheet.nrows
        #print('优化后',rownum)
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
        for i in range(0,rownum):
            row=sheet.row_values(i)
            wordstr= re.sub(r, '',row[0]) 
            seg_list = jieba.cut(wordstr, cut_all=False)
            wordlist.append(" ".join(seg_list))
            labellist.append(row[1])
            numlist.append(row[2])
            categylist.append(row[3])
        #print(wordlist,'\n',labellist,'\n')    
        return wordlist,labellist,numlist,categylist
    
    
    # ## TF-IDF
    
    
    
    def groupwordtfdif(self,wordlist):
        #count_list=CountVectorizer()
        #count_a1ist=count_list.fit_transform(wordlist)#计算各个词语出现的次数'
        #word=count_list.get_feature_names()#所有文档的关键词
        
        # tg_wordcountarray=count_a1ist.toarray().tolist()
        # print(tg_wordcountarray)#查看词频结果
        
        groupransformer=TfidfVectorizer()
        groupransformer.fit(wordlist)
        groupfidf=groupransformer.transform(wordlist)#将词频矩阵X统计成TF-IDF值
        group_wordtfdif=groupfidf.toarray().tolist()
        
        #print('多文档TFIDF矩阵:',group_wordtfdif)
        
        return group_wordtfdif
    
    
    
    
    def singlewordtfdif(self,newtext,wordlist):
        groupransformer=TfidfVectorizer()
        groupransformer.fit(wordlist)#用X_train数据来fit
        singlefidf=groupransformer.transform(newtext)#得到TF-IDF矩阵
        single_wordtfdif=singlefidf.toarray().tolist()
        #print('新文档TFIDF矩阵:',single_wordtfdif)
        return single_wordtfdif
    
    
    
    
    def dealword(self,str1):
        wordlist=[]
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
        str1=str1.strip()
        linestr = re.sub(r, '', str1)
        seg_list = jieba.cut(linestr, cut_all=False)
        wordlist.append(" ".join(seg_list))
        return wordlist
    
    
    # #### 分类别讨论

    def question_lists(self,listtag,listnum):
        list = []
        list.append("您好,请输入您的姓名?")
        list.append("请输入您的工号?")
        list.append("请输入您的部门?")
        #分类信息
        if listtag =="2":
            if listnum == 1 :
                list.append("请输入您的身份证号码")
                list.append("请输入您的证明信息")
            elif listnum== 0 :
                list.append("请输入您的身份证号码")
        elif listtag == '3':
            list.append("请问您想反馈的物业位于哪里呢?")
            list.append("请问您想反馈的物业的问题是什么呢?")
        elif listtag == "1" :
            list.append("请问您子女的身份证号码为?")
        elif listtag == "4":
            list.append("请问您想慰问的对象是?")
        elif listtag == "5":
            list.append("请问您想请假的时间是?")
        elif listtag == "6":
            list.append("请问接待人员的姓名是?")
            list.append("请问接待的时间是多久?")
        elif listtag == "7" :
            if listnum == 0 :
                list.append("请问您想收的东西的编号是多少?")
            elif listnum == 1:
                list.append("请问您想寄的东西的是什么?")
                list.append("请问您想寄往哪里?")
        elif listtag == "8":
            list.append("请问您要报销的发票单号是多少?")
            list.append("请问您要报销的发票金额是多少?")
        return list

     
     # ## 主函数
    # #### 1.对于重复问题的回答
    # #### 2.quit退出程序
    
    
    def multi_query_lz_main(self,listext,listtag,listcate,categylist,grouplist,ask):
        #如果已经在填表的状态里了
        '''
        global MULTI_STATE
        global QUESTION_LIST
        global MAX_LEN
        global ANS_LIST
        global POSITION_LEN
        global FLAG
        global SHOW
        '''
        
        
        if GV.MULTI_STATE == True:
            GV.POSITION_LEN = GV.POSITION_LEN + 1
            GV.ANS_LIST.append(ask)
            if GV.MAX_LEN == GV.POSITION_LEN:
                GV.MULTI_STATE = False
                GV.POSITION_LEN = 0
                return GV.ANS_LIST
            GV.SHOW = True
            return GV.QUESTION_LIST[GV.POSITION_LEN]
        #还没填表呢
        singletext=self.dealword(ask)
        newlist=self.singlewordtfdif(singletext,listext)
        resultlist=self.cosAB(newlist[0],grouplist)   
        maxindex=resultlist.index(max(resultlist))
        #没匹配到,带着问题走
        if max(resultlist)==0.0:
            #2:项目,3:闲聊
            GV.FLAG = 2
            GV.SHOW = False
            return ask

            #print("问题关联号码为:,",maxindex,"您的问题关联方向为: ",listtag[maxindex],"问题匹配为:",listext[maxindex])
        #else:
        #匹配到,更新各种参数,并返回第一个问题
        #QUESTION_LIST:问题列表,ANS_LIST:回答列表,MAX_LIST:问题长度,POSITION_LIST:当前长度
        GV.QUESTION_LIST = self.question_lists(str(int(categylist[maxindex])),
                       listcate[maxindex])
        GV.MAX_LEN = len(GV.QUESTION_LIST)
        GV.ANS_LIST = []
        GV.MULTI_STATE = True
        GV.SHOW = True
        return GV.QUESTION_LIST[GV.POSITION_LEN]

        
        
        
class Muli_query_lz:
    
    def __init__(self):
        pass
        #self.listext,self.listtag,self.listcate,self.categylist,self.grouplist = self.mulit_round_query_start_up()
        #self.mulit_round_query_start_up()
        
    def mulit_round_query_start_up(self):
        mqms = Muli_query_methods_lz2()
        #listext:问题文本,listtag:问题一级分类,listcate:问题出口分类
        listext,listtag,listcate,categylist=mqms.coreword(COMPANY_HELP_PATH)
        grouplist=mqms.groupwordtfdif(listext)
        #ask = lzmethods.fake_main(listext,listtag,listcate,categylist,grouplist)
        #return ask
        return listext,listtag,listcate,categylist,grouplist
  
    def mulit_round_query(self,listext,listtag,listcate,categylist,grouplist,question):
        #multy_query是多轮查询的主函数
        mqms = Muli_query_methods_lz2()
        user_question,flag = mqms.multi_query_lz_main(self,listext,listtag,listcate,categylist,grouplist,question)
        return user_question,flag