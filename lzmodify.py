#!/usr/bin/env python
# coding: utf-8

from multi_query_lz2 import Muli_query_methods_lz2
from config.path_config import *
import project_query_lz
'''
class Muli_query_lz:
    
    def __init__(self):
        pass
        #self.listext,self.listtag,self.listcate,self.categylist,self.grouplist = self.mulit_round_query_start_up()
        #self.mulit_round_query_start_up()
        
    def mulit_round_query_start_up(self):
        mqms = Muli_query_methods_lz()
        #listext:问题文本,listtag:问题一级分类,listcate:问题出口分类
        listext,listtag,listcate,categylist=mqms.coreword(COMPANY_HELP_PATH)
        grouplist=mqms.groupwordtfdif(listext)
        #ask = lzmethods.fake_main(listext,listtag,listcate,categylist,grouplist)
        #return ask
        return listext,listtag,listcate,categylist,grouplist
  
    def mulit_round_query(self,listext,listtag,listcate,categylist,grouplist,question,flag):
        #multy_query是多轮查询的主函数
        mqms = Muli_query_methods_lz()
        user_question,flag = mqms.multi_query_lz_main(listext,listtag,listcate,categylist,grouplist,question,flag)
        return user_question,flag
'''

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
        user_question = mqms.multi_query_lz_main(listext,listtag,listcate,categylist,grouplist,question)
 #                            multi_query_lz_main(self,listext,listtag,listcate,categylist,grouplist,ask)
        return user_question




class Project_query_lz:
    def __init__(self):
        pass
    
    def proj_query(self,question):
        question = project_query_lz.project_query_lz_main(question)
        return question
    
#project_query = Project_query_lz()
#question,flag = project_query.proj_query('我想查工银魔方',2)
