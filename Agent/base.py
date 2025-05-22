from chat_model import DeepSeek

class BaseAgent:
    def __init__(self, **chat_config):
        if 'model_name' not in chat_config:
            chat_config['model_name'] = 'deepseek-v3'
        
        # 初始化语言模型.
        self.chat_tools = DeepSeek(**chat_config)

        # 初始化工具列表.
        self.tools = {
            'chat': {
                'tool': self.chat,
                'use_counts': 0,
            }
        }

    def chat(self, msg):
        return self.chat_tools.chat(msg)
    
    def count(self, tool_name, mode='+', times=1):
        if mode == '+':
            self.tools[tool_name]['use_counts'] += times
        elif mode == '-':
            self.tools[tool_name]['use_counts'] -= times