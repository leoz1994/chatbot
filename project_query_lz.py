# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:42:09 2019

@author: Administrator
"""

from config.path_config import *
import GV
    
def ReadTxtName(rootdir):
    #读取文件中的每一行,转为list
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines

def project_query_lz_main(question):
    #找语句中是否匹配到了项目名称
    txt_line = ReadTxtName(PROJECT_NAMES) 
    for project_name in txt_line:
        if project_name in question:
            #print('我们觉得您是想查' + project_name + '项目的信息')
            GV.SHOW = True
            return ('我们觉得您是想查' + project_name + 
                  '项目的信息,但是我们还没有记录项目详细信息')
    GV.FLAG = 3
    GV.SHOW = False
            #state = False
            #print('与项目无关,此处跳出,接其他模块')
    return question

#project_query_lz_main('工银天梭项目进度怎么样了',2)