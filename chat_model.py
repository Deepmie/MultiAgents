import requests


class DeepSeek:
    def __init__(self, model_name, api_key, base_url): # "deepseek-reasoner", "deepseek-chat", 
        self.url = "{}/chat/completions".format(base_url)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_key)
        }
        self.data = {
            "model": model_name,
            "max_tokens": 4096,
            "stream": False
        }
    
    def chat(self, msg):
        msg = self._package(msg)
        self.data['messages'] = msg
        response = requests.post(self.url, headers=self.headers, json=self.data)

        if response.status_code == 200:
            res = response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return 
        
        res = res['choices'][0]['message'] # chat: 'content', reasponer: 'reasoning_content', 'content'
        return res

    
    def _package(self, msg):
        if isinstance(msg, str):
            return [{'role': 'user', 'content': msg}]
        else:
            return msg


if __name__ == '__main__':
    chat_model = DeepSeek(
        model_name='deepseek-v3',
        api_key='sk-andwtpakahbrmipd',
        base_url='https://cloud.infini-ai.com/maas/v1',
    )

    msg = chat_model.chat('Hello!')
    print(msg)