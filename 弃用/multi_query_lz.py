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


# ## 余弦距离
class Muli_query_methods_lz:

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
    
    
    
    #读取用户输入信息
    #输入可以调用两级索引
    def listcat(self,listtag,listnum):
        #调用model
        list = self.model_for_info(listtag,listnum)
        return list
       
    # #### 生成几个model,供输入信息使用
     
    def model_for_info(self,listtag,listnum):
        list = []
        requests = input("1确认输入信息,0退出>>")
        if requests == "0":
            return 0
        elif requests == "1":
            #通用信息
            #修改成正则
            list.append(input("您好,请输入您的姓名?"))
            
            list.append(input("请输入您的工号?"))
            list.append(input("请输入您的部门?"))
            #分类信息
            if listtag =="2":
                if listnum == 1 :
                    list.append(input("请输入您的身份证号码"))
                    list.append(input("请输入您的证明信息"))
                elif listnum== 0 :
                    list.append(input("请输入您的身份证号码"))
            elif listtag == '3':
                list.append(input("请问您想反馈的物业位于哪里呢?"))
                list.append(input("请问您想反馈的物业的问题是什么呢?"))
            elif listtag == "1" :
                list.append(input("请问您子女的身份证号码为?"))
            elif listtag == "4":
                list.append(input("请问您想慰问的对象是?"))
            elif listtag == "5":
                list.append(input("请问您想请假的时间是?"))
            elif listtag == "6":
                list.append(input("请问接待人员的姓名是?"))
                list.append(input("请问接待的时间是多久?"))
            elif listtag == "7" :
                if listnum == 0 :
                    list.append(input("请问您想收的东西的编号是多少?"))
                elif listnum == 1:
                    list.append(input("请问您想寄的东西的是什么?"))
                    list.append(input("请问您想寄往哪里?"))
            elif listtag == "8":
                list.append(input("请问您要报销的发票单号是多少?"))
                list.append(input("请问您要报销的发票金额是多少?"))
            else:
                return print('我们还没分好类!')
        return list
     
     # ## 主函数
    # #### 1.对于重复问题的回答
    # #### 2.quit退出程序
    
    
    def multi_query_lz_main(self,listext,listtag,listcate,categylist,grouplist,ask,flag):
        state = True
        while state:
            singletext=self.dealword(ask)
            newlist=self.singlewordtfdif(singletext,listext)
            resultlist=self.cosAB(newlist[0],grouplist)   
            maxindex=resultlist.index(max(resultlist))
            if max(resultlist)==0.0:
                #2:项目,3:闲聊
                flag = 2
                return ask,flag
            else:
                print("问题关联号码为:,",maxindex,
                      "您的问题关联方向为: ",listtag[maxindex],
                      "问题匹配为:",listext[maxindex])
                
                list = self.listcat(str(int(categylist[maxindex])),
                               listcate[maxindex])
                #print(type(str(categylist[maxindex])))
                print("您录入的信息为:",list)
                ask=input("您好,还想办理什么业务吗>>")
        #ask_history = ask