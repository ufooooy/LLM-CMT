import re

def detect_hardcoded_certs(file_path):
    cert_patterns = [
        r'-----BEGIN CERTIFICATE-----[\s\S]*?-----END CERTIFICATE-----',
        r'-----BEGIN RSA PRIVATE KEY-----[\s\S]*?-----END RSA PRIVATE KEY-----',
        r'-----BEGIN PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY-----',
        r'-----BEGIN ENCRYPTED PRIVATE KEY-----[\s\S]*?-----END ENCRYPTED PRIVATE KEY-----'
    ]

    with open(file_path, 'r') as file:
        content = file.read()

    found_certs = []
    for pattern in cert_patterns:
        matches = re.findall(pattern, content)
        found_certs.extend(matches)

    return found_certs

def main(file_path):
    # file_path = 'path/to/your/file.c'  # 替换为你的文件路径
    certs = detect_hardcoded_certs(file_path)

    if certs:
        print("Detected hardcoded certificates:")
        for cert in certs:
            print(cert)
            print('-' * 80)
    else:
        print("No hardcoded certificates found.")

if __name__ == "__main__":
    file = 'apply_test/707cacertinmem.c'
    main(file)