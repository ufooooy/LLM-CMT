import ast
import os

# 定义不安全或已弃用的库列表
UNSAFE_LIBRARIES = ['pyaes']

def check_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tree = ast.parse(content)
    
    unsafe_imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in UNSAFE_LIBRARIES:
                    unsafe_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module in UNSAFE_LIBRARIES:
                unsafe_imports.append(node.module)
    
    return unsafe_imports

def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                unsafe_imports = check_imports(file_path)
                if unsafe_imports:
                    print(f"File: {file_path}")
                    print(f"Unsafe imports: {', '.join(unsafe_imports)}")
                    print()

if __name__ == "__main__":
    directory_to_scan = "apply_test/"  # 替换为你的项目路径
    scan_directory(directory_to_scan)