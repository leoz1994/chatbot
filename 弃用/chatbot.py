"""
    问答机器人

    --> 输入：问题语句 Q

    --> 输出：回答语句 A

"""
import time
from filter import LayerFilter


class ChatBot:
    """机器人类"""

    def __init__(self):
        self.layer_filter = LayerFilter()
        self.white_list = []

    @classmethod
    def to_log(cls, question, answer):
        with open('config/chat_log.txt', 'a', encoding='utf-8') as f:
            log_content = f'Q:{question}---A:{answer} \n'
            print(log_content)
            f.write(log_content)

    def local_start(self):
        """本地聊天模式"""
        time.sleep(0.2)
        print('我们开始聊天吧~')
        while True:
            question = input('>> ')
            if question == '关机':
                print('好的，下次再见~')
                break
            answer = self.layer_filter.get_answer(question)
            print(answer)