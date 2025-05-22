import os
import yaml
from dotenv import load_dotenv
from string import Template
from typing import List, Dict

def clean_text(text_content):
    def filter_spec(t):
        return len(t) > 0
    return list(filter(filter_spec, text_content.split('\n')))

def read_text(text_path: str) -> List[str]:
    with open(text_path, mode='r', encoding='utf-8') as f:
        return clean_text(f.read())

def load_apis_pool(apis_path='api.yaml') -> Dict:
    # 加载.env文件
    load_dotenv()

    # 读取.yaml文件
    with open(apis_path, mode='r') as f:
        apis = f.read()
        apis = yaml.safe_load(
            Template(apis).substitute(os.environ)
        )

    return apis