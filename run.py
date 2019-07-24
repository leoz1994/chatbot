"""
    问答机器人

    --> 输入：问题语句 Q

    --> 输出：回答语句 A

"""
from filter import LayerFilter
from lzmodify import Muli_query_lz
from lzmodify import Project_query_lz
import GV

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

    def local_start(self,question):

        """本地聊天模式"""
        if question == '填单子':
            GV.FLAG = 1
            GV.SHOW = False
            return '转到多轮,请输入问题'
        elif question == '我要查项目':
            GV.FLAG = 2
            GV.SHOW = False
            return '转到项目,请输入问题'
        elif question == '88':
            GV.FLAG = 4
            GV.SHOW = False
            return '关机了,88'
        answer = self.layer_filter.get_answer(question)
        GV.SHOW = True
        return answer


#multi_query = Muli_query_lz()
#bot = ChatBot()
#project_query = Project_query_lz()
#listext,listtag,listcate,categylist,grouplist = multi_query.mulit_round_query_start_up()


def run(question):
    #flag: 1:多轮查询,2:项目查询
    if GV.FLAG == 1:
        answer = multi_query.mulit_round_query(listext,listtag,listcate,categylist,grouplist,question)
        #print('to model 1')
        if GV.SHOW == True:
            return answer
    if GV.FLAG == 2:
        answer = project_query.proj_query(question)
        #print('to model 2')
        if GV.SHOW == True:
            return answer
    if GV.FLAG == 3:
        answer = bot.local_start(question)
        #print('to model 3')
        return answer
          #  state = False
    #else:
    #    return '说出你想办的业务吧>>'

multi_query = Muli_query_lz()
bot = ChatBot()
project_query = Project_query_lz()
listext,listtag,listcate,categylist,grouplist = multi_query.mulit_round_query_start_up()

if __name__ == '__main__':
    #初始化

    print('办业务还是闲聊都可以哦>>')
    #nums = 1
    #GV.FLAG != 4:
    question = input('>>')
    answer = run(question)
    print(answer)
        #if GV.FLAG == 4
        #nums += 1


            
        
