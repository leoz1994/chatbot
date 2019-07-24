import jieba
import re
import math
import xlrd
import time
from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

def cosAB(listA,listB):
    
    
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
'''
def coreword(path):
    wordlist=[]
    taglist=[]
    i=0
    fo = open(path, 'r',encoding="utf-8")
    taglist=[]
    for line in fo.readlines():
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
        i+=1
        line=line.strip()
        line=line.split('    ')
        listline=line[0].split('\t')
        taglist.append(listline[0])
        linestr = re.sub(r, '', listline[1])
        seg_list = jieba.cut(linestr, cut_all=False)
        wordlist.append(" ".join(seg_list))
        #seg_str=" ".join(seg_list)
        #print("读取的数据为：%s"%(line))
        #print("文档",i,seg_str,'\n')
    fo.close()
    #for t in wordlist:
        #print(t,'\n')
    return wordlist,taglist
'''

def coreword(path):
    wordlist=[]
    labellist=[]
    answer=[]
    ExcelFile=xlrd.open_workbook(path)
    sheet=ExcelFile.sheet_by_index(0)
    rownum=sheet.nrows
    print('优化后',rownum)
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
    for i in range(0,rownum):
        row=sheet.row_values(i)
        wordstr= re.sub(r, '',row[0]) 
        seg_list = jieba.cut(wordstr, cut_all=False)
        wordlist.append(" ".join(seg_list))
        labellist.append(row[1])
        answer.append(row[2])
    #print(wordlist,'\n',labellist,'\n',answer,'\n')    
    return wordlist,labellist,answer

def groupwordtfdif(wordlist):
    count_list=CountVectorizer()
    count_a1ist=count_list.fit_transform(wordlist)#计算各个词语出现的次数'
    word=count_list.get_feature_names()#所有文档的关键词
    #tg_wordcountarray=count_a1ist.toarray().tolist()
    #print(tg_wordcountarray)#查看词频结果
    groupransformer=TfidfVectorizer()
    groupransformer.fit(wordlist)
    groupfidf=groupransformer.transform(wordlist)#将词频矩阵X统计成TF-IDF值
    group_wordtfdif=groupfidf.toarray().tolist()
    #print('多文档TFIDF矩阵:',group_wordtfdif)
    return group_wordtfdif

def singlewordtfdif(newtext,wordlist):
    groupransformer=TfidfVectorizer()
    groupransformer.fit(wordlist)#用X_train数据来fit
    singlefidf=groupransformer.transform(newtext)#得到TF-IDF矩阵
    single_wordtfdif=singlefidf.toarray().tolist()
    #print('新文档TFIDF矩阵:',single_wordtfdif)
    return single_wordtfdif
    
def dealword(str1):
    wordlist=[]
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
    str1=str1.strip()
    linestr = re.sub(r, '', str1)
    seg_list = jieba.cut(linestr, cut_all=False)
    wordlist.append(" ".join(seg_list))
    return wordlist

def main():
    listext,listtag,answer=coreword("语料-第六版B.xlsx")
    grouplist=groupwordtfdif(listext)
    while True:
        something=input("请提问：")
        start=time.time()
        singletext=dealword(something)
        newlist=singlewordtfdif(singletext,listext)
        resultlist=cosAB(newlist[0],grouplist)   
        maxindex=resultlist.index(max(resultlist))
        #print("最大值位置",maxindex)
        print("回答",answer[maxindex])
        end=time.time()
        #print('用时:',end-start,'s')
    
    
if __name__=='__main__':
    main()
