import pathlib
import re
import json

class Node:
    def __init__(self, title, level):
        self.title = title
        self.level = level  # 0: root; 1-n: non-leaf; -1: leaf
        self.children = [] if self.level != -1 else None

    def add_child(self, node):
        if self.children is not None:
            self.children.append(node)
    
    def set_title(self, title):
        self.title = title

    def to_dict(self):
        if self.children is None:
            return {'title': self.title, 'level': self.level}
        else:
            return {'title': self.title, 'level': self.level, 'children': [child.to_dict() for child in self.children]}

def parse_taxonomy(taxonomy, num=3, generic_node_re=r'(#+)\s*(.*)', index_re=r'[\d\.]+', leaf_re=r'- \*\*(.*?)\*\*'):  # amended regular expression
    taxonomy_lines = [line for line in taxonomy.split('\n')]
    root = Node('root', 0)
    parent_stack = [root]
    for line in taxonomy_lines:
        generic_match = re.match(re.compile(generic_node_re), line)
        leaf_match = re.match(re.compile(leaf_re), line)

        if leaf_match:
            title = leaf_match.group(1).strip()
            parent_stack[-1].add_child(Node(title, -1))
        elif generic_match:
            # title = re.sub(index_re, '', generic_match.group(2)).strip()
            title = generic_match.group(2).strip()
            num_hashes = len(generic_match.group(1))
            level = (num_hashes - num) + 1

            if level == 0:
                root.set_title(title)
            else:
                new_node = Node(title, level)

                if parent_stack[-1].level < level:
                    parent_stack.append(new_node)
                else:
                    while parent_stack and parent_stack[-1].level >= level:
                        child = parent_stack.pop()
                        parent_stack[-1].add_child(child)
                    parent_stack.append(new_node)
        # else:
        #     return None
    while len(parent_stack) > 1:
        child = parent_stack.pop()
        parent_stack[-1].add_child(child)
    return parent_stack

def trans_taxonomy(file_path):
    # print(file_path)
    with open(pathlib.Path(file_path), 'r') as file:
        taxonomy = file.read()
    hierarchy = parse_taxonomy(taxonomy)
    
    # Change the file extension to .json
    trans_file_path = pathlib.Path(file_path).with_suffix('.json')
    print(trans_file_path)
    
    with open(pathlib.Path(trans_file_path), 'w') as file:
        json.dump(hierarchy[0].to_dict(), file, indent=4, ensure_ascii=False)
    return trans_file_path

upload_directory = pathlib.Path(__file__).parent / 'upload'
txt_files = list(upload_directory.glob('*.txt'))

if not txt_files:
    raise FileNotFoundError("No .txt files found in the upload directory.")

latest_txt = max(txt_files, key=lambda f: f.stat().st_mtime)
trans_taxonomy(latest_txt)