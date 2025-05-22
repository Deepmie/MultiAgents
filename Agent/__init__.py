from .base import BaseAgent
from typing import List, Callable
import time

class AgentManager:
    def __init__(self, agents: List[BaseAgent], min_use_counts: int=0, min_search_time: int=0.5):
        self.agents = agents
        self.min_use_counts = min_use_counts
        self.min_search_time = min_search_time
    
    def execute(self, tool_name, **tool_kwargs):
        def sorted_agent(agent: BaseAgent):
            return agent.tools.get(tool_name)['use_counts']
        
        while True:
            agent_selected = min(self.agents, key=sorted_agent)

            # 满足条件才调用.
            if agent_selected.tools.get(tool_name)['use_counts'] <= self.min_use_counts:
                tool_func: Callable = agent_selected.tools[tool_name]['tool']
                agent_selected.count(tool_name, '+')
                tool_res = tool_func(**tool_kwargs)
                agent_selected.count(tool_name, '-')
                return tool_res
            
            time.sleep(self.min_search_time) # 检索频率.