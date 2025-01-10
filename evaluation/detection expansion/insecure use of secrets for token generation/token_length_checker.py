import ast

class TokenLengthChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Call(self, node):
        # 检查是否是 secrets.token_urlsafe 的调用
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'token_urlsafe':
            if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, int):
                length = node.args[0].value
                if length < 256:
                    self.errors.append(f"Line {node.lineno}: 'secrets.token_urlsafe' length should be >= 256, found {length}.")
        self.generic_visit(node)

def check_token_length_in_file(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    checker = TokenLengthChecker()
    checker.visit(tree)
    
    return checker.errors

# 使用示例
if __name__ == "__main__":
    file_path = 'apply_test/1977websockets_server_client.py'  # 替换为你的文件路径
    errors = check_token_length_in_file(file_path)
    
    if errors:
        for error in errors:
            print(error)
    else:
        print("No issues found with token length.")