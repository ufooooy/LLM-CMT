import csv
from pathlib import Path


def record_files_to_csv(directory_path, output_csv_path):
    extensions = ['.c', '.cpp', '.go', '.java', '.py']
    extension_to_language = {
        '.c': 'c',
        '.cpp': 'cpp',
        '.go': 'go',
        '.java': 'java',
        '.py': 'python'
    }
            
    directory = Path(directory_path)
    output_csv = Path(output_csv_path)

    with output_csv.open('w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['path', 'source', 'language', 'If_CAM'])

        for extension in extensions:
            for file_path in directory.rglob('*' + extension):
                if 'crawl' in file_path.parts:
                    source = 'github'
                elif 'cryptogo' in file_path.parts:
                    source = 'CryptoGo'
                elif 'CryptoAPI-Bench' in file_path.parts:
                    source = 'CryptoAPI-Bench'
                elif 'licma' in file_path.parts:
                    source = 'licma'
                elif 'MASC' in file_path.parts:
                    source = 'MASC'
                else:
                    source = 'unknown'

                language = extension_to_language[file_path.suffix]
                if_cam = 0 if 'nomisuses' in file_path.parts else 1
                writer.writerow([str(file_path), source, language, if_cam])


if __name__ == "__main__":
    test_directory = "Dsub"
    output_csv = "dsub.csv"
    
    record_files_to_csv(test_directory, output_csv)

