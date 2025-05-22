import importlib

def get_prompt(task, lang='en'):
    m = importlib.import_module('prompt.{}'.format(task))
    return getattr(m, lang)