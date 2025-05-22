from Agent import AgentManager, BaseAgent
from typing import List
from prompt import get_prompt
import threading
import json
import regex as re
from tools import *
import jsonlines
import time

def extract_question(res):
    question = re.findall(
        pattern=r'```json(.+?)```',
        string=res,
        flags=re.DOTALL,
    )[0]
    return json.loads(question)

def generate_question(question_prompt, agent_manager: AgentManager, questions_tools: List):
    for _ in range(3):
        try:
            questions = extract_question(
                agent_manager.execute('chat', msg=question_prompt)['content']
            )
            questions_tools.extend(questions)
            return questions
        except json.JSONDecodeError as e:
            print(e)
    return []

def generate_answer(answer_template, question: str, agent_manager: AgentManager, result_map: Dict):
    answer_prompt = answer_template.format(question=question)
    answer = agent_manager.execute('chat', msg=answer_prompt)['content']
    result_map[question] = answer
    return answer

def main():
    keys = read_text('key.txt')
    fields = read_text('field.txt')
    question_template = get_prompt('question')
    answer_template = get_prompt('answer')
    apis_pool = load_apis_pool()
    threadings_pool = []
    questions_pool = []
    result_map = {}

    agents = []
    for serve_name, serve in apis_pool.items():
        for api_name, api_config in serve.items():
            base_agent = BaseAgent(model_name='gpt-4o', **api_config)
            agents.append(base_agent)

    agent_manager = AgentManager(agents)

    for k in keys:
        for f in fields:
            question_prompt = question_template.format(key=k, field=f)
            
            # 创建问题的线程.
            qu_t = threading.Thread(target=generate_question, args=(question_prompt, agent_manager, questions_pool, ))
            qu_t.start()
            threadings_pool.append(qu_t)
        
        time.sleep(5)
        # 针对每个问题进行提问.
        while len(questions_pool) > 0:
            qu = questions_pool.pop(0)
            # print(qu)
            # 创建回答的线程.
            result_map[qu] = ''
            an_t = threading.Thread(target=generate_answer, args=(answer_template, qu, agent_manager, result_map, ))
            an_t.start()
            threadings_pool.append(an_t)
        
        rt = []
        with open('res.json', mode='w', encoding='utf-8') as writer:
            for qu, an in result_map.items():
                rt.append({'text': 'Question:\n{}\nAnswer:{}'.format(qu, an)})
            writer.write(json.dumps(rt, ensure_ascii=False, indent=4))
    
    
    # 回答全部的.
    while len(questions_pool) > 0:
        qu = questions_pool.pop(0)
        # print(qu)
        # 创建回答的线程.
        result_map[qu] = ''
        an_t = threading.Thread(target=generate_answer, args=(answer_template, qu, agent_manager, result_map, ))
        an_t.start()
        threadings_pool.append(an_t)

    for t in threadings_pool:
        t.join() # 等待所有线程结束.


if __name__ == '__main__':
    main()
