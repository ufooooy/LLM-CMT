import json
import os

from main import append, merge2
from utils import write_file, read_json, ensure_file_exists, clear_file


def find_specific_files(folder_path, begin, end):
    """
    Finds all files in the given folder that start with 'identify' and end with '.json'.

    :param end:
    :param begin:
    :param folder_path: Path to the folder where files will be searched.
    :return: A list of matching file names.
    """
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(begin) and filename.endswith(end):
            matching_files.append(filename)
    return matching_files


if __name__ == "__main__":
    all_exams = ['base', 'dataset_new/1', 'dataset_new/11', 'dataset_new/11/add',
                 'c_22_2/1', 'go/data1/2',
                 'go/data3_5/1', 'go/data3_5/5', 'go/data3_5/10', 'python/data1_2/1',
                 'python/data1_6/2', 'python/data6/1', 'python/data6/1/add',
                 'python/data7_/2',
                 'python/data10/1', 'python/data10/1/add',
                 'java/data1_3/9', 'java/data1_3/9/add',
                 'java/data1_3/12',
                 'java/data7_8/1',
                 'java/data9_11/4', 'java/data9_11/4/add',
                 'MASC_minimal_flaws/SSL']
    count = 21
    base_dir = all_exams[count]
    dimension = 'append-0-op'
    base_taxonomies = [
        base_dir + '/' + find_specific_files(base_dir, dimension, '.txt')[0],
        ]

    target_dir = all_exams[count + 1]
    # target_misuses = target_dir + '/' + find_specific_files(target_dir, 'merge2', '.json')[0]
    # base = read_json(base_misuses)
    # target = read_json(target_misuses)
    # append_misuse = [i for i in target if i not in base]
    # print(append_misuse)
    append_file = target_dir + '/append2.json'

    # ensure_file_exists(append_file)
    # clear_file(append_file)
    # write_file(append_file, json.dumps(append_misuse, indent=4, ensure_ascii=False))
    to_append = read_json(append_file)
    # print(append_file)
    if to_append:
        append(model='gpt-4-turbo-preview', max_tokens=4095,
               previous_taxonomy=base_taxonomies, input_append=to_append,
               record_dir=target_dir, result_dir=target_dir,
               base_file=base_dir + '/' + find_specific_files(base_dir, dimension, '.txt')[0])

