import json
import os

from main import append, merge2
from utils import write_file, read_json, ensure_file_exists, clear_file


def find_specific_files(folder_path, begin, end):
    """
    Finds all files in the given folder that start with 'identify' and end with '.json'.

    :param folder_path: Path to the folder where files will be searched.
    :return: A list of matching file names.
    """
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(begin) and filename.endswith(end):
            matching_files.append(filename)
    return matching_files


if __name__ == "__main__":
    base_dir = 'MASC_minimal_flaws/RandomNumber'

    target_dir = 'MASC_minimal_flaws/SSL'
    # for i in range(1, 5):
    #     dataset_dir = target_dir + str(i)
    append_data = target_dir + '/paraphrase.json'
    base_misuses = base_dir + '/' + find_specific_files(base_dir, 'merge2', '.json')[0]
        # base_taxonomies = [base_dir + '/' + find_specific_files(base_dir, 'append-0', '.txt')[0],
        #                    base_dir + '/' + find_specific_files(base_dir, 'append-1', '.txt')[0],
        #                    base_dir + '/' + find_specific_files(base_dir, 'append-2', '.txt')[0], ]
    append_file = target_dir + '/append.json'

    append_misuse = merge2(model='gpt-4-turbo-preview', max_tokens=4095,
                        input_result1=append_data, input_result2=base_misuses,
                        record_dir=target_dir, result_dir=target_dir)
    ensure_file_exists(append_file)
    clear_file(append_file)
    write_file(append_file, json.dumps(append_misuse, indent=4, ensure_ascii=False))
        # base_dir = dataset_dir
        # to_append = read_json(append_file)
        # if to_append:
        #     append(model='gpt-4-turbo-preview', max_tokens=4095,
        #            previous_taxonomy=base_taxonomies, input_append=to_append,
        #            record_dir=dataset_dir, result_dir=dataset_dir)

        # print(append_misuse)
