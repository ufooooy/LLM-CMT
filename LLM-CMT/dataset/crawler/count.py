import os

def count_files_in_subfolders(directory):
    total_files = 0
    valid_extensions = ('.java', '.py', '.go', '.c', '.cpp')
    for root, dirs, files in os.walk(directory):
        if root != directory:  # Only count files in subdirectories
            filtered_files = [file for file in files if file.endswith(valid_extensions)]
            total_files += len(filtered_files)
    return total_files

def main():
    current_directory = os.getcwd()
    print(current_directory)
    file_count = count_files_in_subfolders(current_directory)
    print(f"Total files in subfolders: {file_count}")

if __name__ == "__main__":
    main()
