# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:57:39 2019

@author: Administrator
"""

from config.path_config import *
from multi_query_lz2 import Muli_query_methods_lz2

lz = Muli_query_methods_lz2()
#lists = lz.question_lists('2',1)
#print(lists)
#position = len(lists)
listext,listtag,listcate,categylist=lz.coreword(COMPANY_HELP_PATH2)
grouplist=lz.groupwordtfdif(listext)
while True:
    question = input('>>')
    print(lz.multi_query_lz_main(listext,listtag,listcate,categylist,grouplist,question))