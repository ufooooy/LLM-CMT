from collections import defaultdict
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

def write_file(file_path, content, mode='w'):
    path = Path(file_path)
    # Ensure the directory for the file exists and create file if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    
    if mode == 'w':
        path.write_text(content, encoding='utf-8')
    elif mode == 'a':
        with path.open(mode='a', encoding='utf-8') as f:
            f.write(content)

def read_json(json_path):
    path = Path(json_path)
    if path.exists():
        with path.open('r', encoding='utf-8') as file:
            try:
                json_list = json.load(file)
            except json.JSONDecodeError:
                json_list = []
            return json_list
        
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
def parse_taxonomy(input_text):
    lines = input_text.split('\n')

    taxonomy = defaultdict(lambda: defaultdict(lambda: {'title': '', 'items': []}))

    current_section = None
    current_subsection = None
    leaf_match_count = 0  # Initialize counter for number of leaf matches

    for line in lines:
        section_match = re.match(r'^### (\d+)\. (.+)$', line)
        subsection_match = re.match(r'^#### (\d+\.\d+) (.+)$', line)
        # leaf_match = re.match(r'^- \*\*(.+)\*\*:', line)
        # leaf_match = re.match(r'^- \*\*(.+?)\*\*$', line)
        leaf_match = re.match(r'^- \*\*(.+?)\*\*.*$', line)

        if section_match:
            current_section = section_match.group(1)
            section_title = section_match.group(2)
            taxonomy[current_section]['title'] = section_title
            current_subsection = None  # Reset current_subsection when a new section is encountered
        elif subsection_match:
            current_subsection = subsection_match.group(1)
            subsection_title = subsection_match.group(2)
            taxonomy[current_section][current_subsection]['title'] = subsection_title
        elif leaf_match:
            leaf_match_count += 1  # Increment leaf match counter
            leaf_title = leaf_match.group(1)
            # 如果存在当前子节，添加到子节
            if current_subsection:
                taxonomy[current_section][current_subsection]['items'].append(leaf_title)
            # 否则，直接添加到当前节
            else:
                # 确保当前节的'items'是一个列表
                if not isinstance(taxonomy[current_section]['items'], list):
                    taxonomy[current_section]['items'] = []
                taxonomy[current_section]['items'].append(leaf_title)

    return taxonomy, leaf_match_count

def trans_taxonomy(taxonomy):
    tax_str = ''
    leaf_num = 0
    for section, content in taxonomy.items():
        # print(f"{section} {content['title']}")
        tax_str += f"### {section}. {content['title']}\n"
        if content['items'] and isinstance(content['items'], list) and len(content['items']) > 0:
            for item in content['items']:
                # print(f"    - {item}")
                tax_str += f"- **{item}\n"
                leaf_num += 1
        for subsection, details in content.items():
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):
                # print(f"  {subsection} {details['title']} {type(details)}")
                tax_str += f"#### {subsection} {details['title']}\n"
                for item in details['items']:
                    # print(f"    - {item}")
                    tax_str += f"- **{item}**\n"
                    leaf_num += 1
    return tax_str, leaf_num