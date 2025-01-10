import ast

class NonceReuseChecker(ast.NodeVisitor):
    def __init__(self):
        self.nonces = set()
        self.reuse_detected = False

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and 'nonce' in target.id:
                if isinstance(node.value, ast.Constant):
                    nonce_value = node.value.value
                    if nonce_value in self.nonces:
                        self.reuse_detected = True
                        print(f"Nonce reuse detected: {nonce_value}")
                    else:
                        self.nonces.add(nonce_value)
                elif isinstance(node.value, ast.Name) and node.value.id in self.nonces:
                    self.reuse_detected = True
                    print(f"Nonce reuse detected: {node.value.id}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr in ['encrypt', 'decrypt']:
            if len(node.args) > 1:  # Check if there are at least two arguments
                nonce_arg = node.args[1]  # The second argument is the nonce
                if isinstance(nonce_arg, ast.Constant):
                    nonce_value = nonce_arg.value
                    if nonce_value in self.nonces:
                        self.reuse_detected = True
                        print(f"Nonce reuse detected in {node.func.attr} call: {nonce_value}")
                    else:
                        self.nonces.add(nonce_value)
                elif isinstance(nonce_arg, ast.Name) and nonce_arg.id in self.nonces:
                    self.reuse_detected = True
                    print(f"Nonce reuse detected in {node.func.attr} call: {nonce_arg.id}")
        self.generic_visit(node)

def check_nonce_reuse(code):
    tree = ast.parse(code)
    checker = NonceReuseChecker()
    checker.visit(tree)
    return checker.reuse_detected

# Example usage
code = """
from nacl.secret import SecretBox

g_nonce = b"123456781234567812345678"  # 24 byte
g_key = b"12345678123456781234567812345678"
nonce = b"123456781234567812345678"  # 24 byte
g_plaintext = b"abcdefghijklmnop"
g_key1 = b"12345678123456781234567812345678"
g_key2 = bytes("12345678123456781234567812345678", "utf8")

def p_example14_indirect_g_variable_access2(data):
    key = g_key2
    secret_box = SecretBox(key)
    cipher_text = secret_box.encrypt(data, nonce)
    return cipher_text

def decrypt(key, data):
    secret_box = SecretBox(key)
    cipher_text = secret_box.decrypt(data, g_nonce)
    return cipher_text

if __name__ == '__main__':
    # TestRule3 code
    print("PyNaCl -> Key -> p_example14_indirect_g_variable_access2:",
          decrypt(g_key, p_example14_indirect_g_variable_access2(g_plaintext)[24:]) == g_plaintext)
"""

if check_nonce_reuse(code):
    print("Nonce reuse detected in the code.")
else:
    print("No nonce reuse detected.")