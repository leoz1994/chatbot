"""
    层级过滤器，将输入语句先后通过模板、搜索、生成、互联网等模块，

    如果搜索到答案，则返回不再继续执行

    如果没有获得答案，则交给下一层处理

    如果最终没有获得相关答案则返回默认答案
"""

from layer import *

jieba.setLogLevel('INFO')


class LayerFilter:
    def __init__(self):
        self.make_word_worker()
        self.default_answers = self.get_default()
        self.pipeline = [Template(), CorpusSearch(), Baike(), InterNet()]

    @staticmethod
    def make_word_worker(build=True):
        """初始化语料库的倒排索引"""

        ww = WordWorker()
        if build:
            ww.build_vocab()
            ww.build_inverse()


    @staticmethod
    def get_default():
        """加载默认答案"""
        answers = list()
        root = et.parse(DEFAULT_PATH)
        a_s = root.find('default').findall('a')
        for a in a_s:
            answers.append(a.text)
        return answers

    def get_answer(self, question):
        """获取答案"""
        # 以此经过各模块处理，如果找到答案则直接返回
        for p in self.pipeline:
            try:
                answer = p.search_answer(question)
                if answer:
                    return answer
            except Exception as e:
                print(e)

        # 如果最终没有答案，则随机选择默认答案输出
        return choice(self.default_answers)
