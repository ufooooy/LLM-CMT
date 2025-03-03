import json
from pathlib import Path
import re
import time


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当时年月日秒时间戳

def print_to(message, file, color='blue'):
    color_codes = {
        'red': "\033[91m",       # error 
        'green': "\033[92m",     # successfull
        'blue': "\033[94m",      # assistant information
        'gray': "\033[90m"       # insignificant information
    }
    color_code = color_codes.get(color, "\033[0m")  # Default to reset color if color is not found
    print(color_code + message + "\033[0m")
    
    if file:
        file_path = Path(file)
        if not file_path.exists():
            file_path.touch()  # Create the file if it doesn't exist
        with open(file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def write_json(file, content):
    path = Path(file)
    if not path.exists():
        path.touch()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def extract_json_blocks(text, pattern=r'```json(.*?)```'):
    '''
    提取一段话中所有以```json开头和```结尾的内容，并将其转化为字典列表
    args:
        text: 包含json块的文本
    returns:
        json_blocks: 包含所有json块的字典列表，如果json_blocks是空列表，或列表里的字典元素为空字典则返回None
    '''
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return None
    
    json_blocks = []
    for match in matches:
        try:
            json_block = json.loads(match.strip())
            if json_block: 
                json_blocks += json_block 
        except json.JSONDecodeError:
            continue  # Skip appending empty dict if decoding fails
    
    if not json_blocks or all(not block for block in json_blocks):
        return None  # Return None if json_blocks is an empty list or contains only empty dicts
    return json_blocks

def json_format_check(answer_text):
    json_result = extract_json_blocks(answer_text)
    if json_result:
        return 1
    return 0