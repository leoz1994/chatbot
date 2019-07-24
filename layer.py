import xml.etree.ElementTree as et
from urllib.parse import quote_plus
from urllib.request import Request
from urllib import request
from collections import Counter
from random import choice
import itertools
import logging
import json
import os
import re

import requests
from bs4 import BeautifulSoup
import numpy as np
import jieba

from config.path_config import *
from factory import WordWorker


class BaseLayer:
    """基础父类"""

    def __init__(self, log=True):
        self.logger = logging.getLogger()
        if not log:
            self.close_log()

    def close_log(self):
        self.logger.setLevel(logging.ERROR)

    def print_log(self, msg):
        self.logger.warning(msg)

    def search_answer(self, question):
        ...

class Template(BaseLayer):
    """
        针对机器人的人格信息，根据输入语句，利用正则表达式匹配问句，

        输出配置好的答案。

    """

    def __init__(self):
        super(Template, self).__init__()
        self.template = self.load_temp_file()
        self.robot_info = self.load_robot_info()
        self.temps = self.template.findall('temp')
        self.default_answer = self.get_default('default')
        self.exceed_answer = self.get_default('exceed')
        self.print_log('Template layer is ready.')

    def load_robot_info(self):
        """加载机器人的人格信息"""
        robot_info_dict = dict()
        robot_info = self.template.find('robot_info')
        for info in robot_info:
            robot_info_dict[info.tag] = info.text
        return robot_info_dict

    @staticmethod
    def load_temp_file():
        """加载模板的 xml 文件"""
        root = et.parse(SELF_TEMP_FILE)
        return root

    def get_default(self, item):
        """获取默认回复答案"""
        return self.template.find(item)

    def search_answer(self, question):
        """在模板中匹配答案"""
        global match_temp
        match_temp = None
        flag = False
        for temp in self.temps:

            # 搜索匹配的相关答案
            qs = temp.find('question').findall('q')
            for q in qs:
                result = re.search(q.text, question)
                if result:
                    match_temp = temp
                    # 匹配到后更改 标记
                    flag = True
                    break
            if flag:
                # 如果已经找打答案则跳出循环
                break

        if match_temp:
            a_s = match_temp.find('answer').findall('a')
            answer = choice(a_s).text
            return answer.format(**self.robot_info)
        else:
            return None

class CorpusSearch(BaseLayer):
    THRESHOLD = 0.7

    def __init__(self):
        super(CorpusSearch, self).__init__()
        ww = WordWorker()
        self.inverse = ww.inverse
        self.question_list = ww.question_list
        self.answer_list = ww.answer_list
        self.print_log('CorpusSearch layer is ready.')

    @staticmethod
    def cosine_sim(a, b):
        """计算两个句子的 余弦相似度"""
        a_words = Counter(a)
        b_words = Counter(b)

        # 建立两个句子的 字典 vocabulary
        all_words = b_words.copy()
        all_words.update(a_words - b_words)
        all_words = set(all_words)

        # 生成句子向量
        a_vec, b_vec = list(), list()
        for w in all_words:
            a_vec.append(a_words.get(w, 0))
            b_vec.append(b_words.get(w, 0))

        # 计算余弦相似度值
        a_vec = np.array(a_vec)
        b_vec = np.array(b_vec)
        a__ = np.sqrt(np.sum(np.square(a_vec)))
        b__ = np.sqrt(np.sum(np.square(b_vec)))
        cos_sim = np.dot(a_vec, b_vec) / (a__ * b__)

        return round(cos_sim, 4)

    def search_answer(self, question):
        # 分词后，各词都出现在了哪些文档中
        search_list = list()
        q_words = jieba.lcut(question)
        for q_word in q_words:
            index = self.inverse.get(q_word, list())
            search_list += index

        if not search_list:
            return None

        # 统计包含问句中词汇次数最多的 3 个文档
        count_list = Counter(search_list)
        count_list = count_list.most_common(3)
        result_sim = list()
        for i, _ in count_list:
            q = self.question_list[i]
            sim = self.cosine_sim(q_words, q)
            result_sim.append((i, sim))

        # 根据两两的余弦相似度选出最相似的问句
        result = max(result_sim, key=lambda x: x[1])

        # 如果相似度低于阈值，则返回 None
        if result[1] > self.THRESHOLD:
            answer = ''.join(self.answer_list[result[0]])
            return answer
        else:
            return None

class Generate(BaseLayer):
    """
        生成模型

        利用 DL 模型对输入语句进行预测

            1. Seq2Seq
            2. Bin-Seq2Seq
            3. Seq2Seq + Attention
            4. （可以尝试机器学习方法）

    """

class Baike(BaseLayer):

    def __init__(self):
        super(Baike, self).__init__()
        self.print_log('Baike layer is ready.')

    def search_answer(self, query):
        import urllib.request
        import urllib.parse
        try:
            url = 'https://baike.baidu.com/item/' + urllib.parse.quote(query)
            html = urllib.request.urlopen(url)
            content = html.read().decode('utf-8')
            html.close()
            soup = BeautifulSoup(content, "lxml")
            text = soup.find('div', class_="lemma-summary").children
            y = []
            for x in text:
                word = re.sub(re.compile(r"<(.+?)>"), '', str(x))
                words = re.sub(re.compile(r"\[(.+?)\]"), '', word)
                y.append(words)
            return ''.join(y)
        except:
            return None

class InterNet(BaseLayer):
    """
    利用 Sogou 问问的接口获取问答语料库
    """
    DOMAIN = 'https://www.sogou.com/'


    # 搜索问题的链接
    QUERY_URL = 'https://www.sogou.com/sogou?query={0}&ie=utf8&insite=wenwen.sogou.com'


    # 获取相似问题的链接
    EXTEND_URL = 'https://wenwenfeedapi.sogou.com/sgapi/web/related_search_new?key={0}'

    HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
                             "AppleWebKit/600.5.17 (KHTML, like Gecko) "
                             "Version/8.0.5 Safari/600.5.17"}

    def __init__(self):
        super(InterNet, self).__init__()
        self.print_log('InterNet layer is ready.')

    def get_html(self, url):
        """
        不使用代理 ip
        """
        req = Request(url, headers=self.HEADERS)
        response = request.urlopen(req, timeout=3)
        html = response.read().decode('utf8')  # 读取后数据为 bytes，需用 utf-8 进行解码
        html = BeautifulSoup(html, 'html.parser')
        return html

    def collect_answers(self, query):
        """
        从搜索结果页面中收集答案
        """
        query = quote_plus(query)
        query_url = self.QUERY_URL.format(query)
        html = self.get_html(query_url)
        answer_list = html.select('.vrwrap')
        return answer_list

    def extract_skip_url(self, url):
        """
        从跳转页面中提取出目标 url
        """
        html = self.get_html(url)
        skip_url = html.select('meta')[1].attrs.get('content')
        skip_url = re.findall("URL=\\\'(.+)", skip_url)[0][:-1]
        return skip_url

    def extract_answer(self, answer_list):
        """
        提取问题的最佳答案
        将问题内容、标签、答案内容整合成一条数据
        """

        new_list = list()
        for answer in answer_list:

            a = answer.select_one('.vrTitle a')

            # 获取跳转链接
            link = self.DOMAIN + a.attrs.get('href')
            url = self.extract_skip_url(link)
            html = self.get_html(url)

            # 获取问题标题与标签
            section = html.select('.main .section')[0]
            title = re.sub(r'[\?？]+', '', section.select_one('#question_title span').text)
            tag = section.select_one('.tags a').text

            # 获取答案相关
            section = html.select('.main .section')[1]
            content = section.select_one('#bestAnswers .replay-info pre')
            if content is None:
                content = section.select_one('.replay-section.answer_item .replay-info pre')
            content = content.text
            content = re.sub(r'\s+', '', content)  # 去除空格字符，包括：\r \n \r\n \t 空格

            # 构建成一条答案，并添加至答案结果列表
            answer = {'title': title, 'tag': tag, 'content': content}
            new_list.append(answer)
        return choice(new_list[:2])

    def search_answer(self, query):
        """搜索答案"""
        try:
            answers = self.collect_answers(query)
            answer = self.extract_answer(answers).get('content')
            answer = answer.split('。')[0].split('！')[0]
            answer = re.sub(r'["“”]', '', answer) + '。'
            return answer

        except:
            return None






