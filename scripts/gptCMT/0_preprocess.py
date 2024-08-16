import os
import shutil

from utils import num_tokens_from_string


def filter_files_by_token_count(source_dir, token_limit=4095, model='gpt-4-turbo-preview'):
    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Only process files (not directories)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Tokenize the file content and count the tokens
            tokens = num_tokens_from_string(content, model)
            if tokens > token_limit:
                # Ensure the target directory exists
                target_dir = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + '_filter')
                os.makedirs(target_dir, exist_ok=True)

                # Move the file to the target directory
                shutil.move(file_path, target_dir)


def batch(target_dir):
    files = os.listdir(target_dir)
    for i in range(0, len(files), 50):
        os.makedirs(os.path.join(target_dir, str(i // 50 + 1)), exist_ok=True)
        for file in files[i:i + 50]:
            shutil.move(os.path.join(target_dir, file), os.path.join(target_dir, str(i // 50 + 1), file))


if __name__ == '__main__':
    dataset_dir = 'java/data9_11'
    batch(dataset_dir)
    # Iterate over all subdirectories in the dataset directory
    for sub_dir in os.listdir(dataset_dir):
        sub_dir_path = os.path.join(dataset_dir, sub_dir)
        filter_files_by_token_count(sub_dir_path)
