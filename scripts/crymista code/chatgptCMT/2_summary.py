from main import base_task
from prompt import paraphrase_prompt, merge_prompt
import json
import os
import shutil

from utils import read_json, clear_file, write_file, ensure_file_exists


def find_identify_json_files(folder_path):
    """
    Finds all files in the given folder that start with 'identify' and end with '.json'.

    :param folder_path: Path to the folder where files will be searched.
    :return: A list of matching file names.
    """
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith('identify') and filename.endswith('.json'):
            matching_files.append(filename)
    return matching_files


def find_no_and_yes(totals):
    pur = []
    no = None
    yes = []
    for amis in totals:
        if amis['abstract'] == 'No cryptographic API misuse':
            no = amis
        else:
            pur.append(amis)
            yes += amis['files']
    return no, yes, pur


def write_json():
    pass


def separate(source_dir):
    identify_result = find_identify_json_files(source_dir)[0]
    identify_file = source_dir + '/' + identify_result
    total = read_json(identify_file)
    corrct, misuse, misuse_result_list = find_no_and_yes(total)
    clear_file(identify_file)
    write_file(identify_file, json.dumps(misuse_result_list, indent=4, ensure_ascii=False))
    correct_json = source_dir + '/correct.json'

    if corrct:
        final_correct = [{
            'abstract': corrct['abstract'],
            'files': [],
            'detail': corrct['detail']
        }]
        for f in corrct['files']:
            if f not in misuse:
                if f.find('.') >= 0:
                    final_correct[0]['files'].append(f)

        ensure_file_exists(correct_json)
        clear_file(correct_json)
        write_file(correct_json, json.dumps(final_correct, indent=4, ensure_ascii=False))

        correct = read_json(correct_json)
        # print(correct)
        if correct:
            correct_dir = source_dir + '_correct'
            os.makedirs(correct_dir, exist_ok=True)
            for i in correct[0]['files']:
                file_path = os.path.join(source_dir, i)
                shutil.move(file_path, correct_dir)
    return identify_file


if __name__ == "__main__":
    my_source_dir = 'MASC_minimal_flaws/RandomNumber'

    identify_results = separate(my_source_dir)
    # identify_result = '6/identify-2024-04-29 15_14_59.json'

    output_result = base_task(model='gpt-4-turbo-preview', max_tokens=4095,
                              task_name='merge', prompt_fun=merge_prompt,
                              input_json_file=identify_results,
                              result_dir=my_source_dir, record_dir=my_source_dir)
    base_task(model='gpt-4-turbo-preview', max_tokens=4095,
              task_name='paraphrase', prompt_fun=paraphrase_prompt,
              input_json_file=output_result,
              result_dir=my_source_dir, record_dir=my_source_dir)
