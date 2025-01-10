import code
import copy
import time

from docopt import docopt
from callgpt import generate_response
from lan import *
from prompt import *
from show import *
from utils import *

BATCH = 3

LAN = 'en'
ROUND = 1
RECORD_DIR = 'log'
RESULT_DIR = 'output'


def parse_identify_response(response, misuse_keyword, wrong_format_warns, rejudge_warns):
    result = extract_pattern_strings(response)
    if not result:
        # gpt没有按指定格式输出结果或整个batch的代码都被miss了，需记录prompt、代码
        print_warning(wrong_format_warns)
        print_warning(rejudge_warns)
        return None
    struc_list = string_list_to_json_list(result)

    # gpt可能回复多个list，需连接成一个列表
    # 另外gpt可能以每个代码来统计的，使得同类误用有多个字典，需按摘要合并文件和详细描述
    dict_list = None
    if type(struc_list[0]) == list:
        dict_list = merge_nested_lists(struc_list)
    else:
        print(type(dict_list), dict_list)
        return None
    merged_list = merge_dicts(dict_list, abstract=misuse_keyword[0], files=misuse_keyword[1], details=misuse_keyword[2])
    # gpt可能将未发现密码误用情况也统计成一个条目，文件列表为空，剔除这个类别
    merged_list = remove_empty_entries(merged_list, key=misuse_keyword[1])

    return merged_list


def process_identify_response(batch_files, response, dateset_dir, result_file, record_file, excepts, lan):
    # 处理识别响应的函数，解析响应并更新结果文件和记录文件
    try:
        result = parse_identify_response(response, misuse_key[lan], wrong_format_warning[lan], rejudge_warning[lan])
        if result is not None:
            # gpt漏报的情况
            miss = find_missing_file([i.name for i in batch_files], result, key=misuse_key[lan][1])
            # 摘要为空的文件列表
            miss += find_none_iterm(result, key1=misuse_key[lan][0], key2=misuse_key[lan][1])
            # 详细为空的文件列表
            miss += find_none_iterm(result, key1=misuse_key[lan][2], key2=misuse_key[lan][1])

            if miss:
                print_to_log(f'{missing_warning[lan]}{format_list(miss)}{stop[lan]}', record_file,
                             print_fun=print_warning)
                print_to_log(rejudge_warning2[lan], record_file, print_fun=print_warning)

                excepts += get_path_by_filename(miss, dateset_dir)
            history_result = read_json(result_file)
            merged_result = merge_dicts(result + history_result,
                                        abstract=misuse_key[lan][0], files=misuse_key[lan][1],
                                        details=misuse_key[lan][2])
            deduplicate_merged_result = deduplicate_dict_list(dict_list=merged_result, file_key=misuse_key[lan][1])
            write_file(result_file, json.dumps(deduplicate_merged_result, indent=4, ensure_ascii=False))
        else:
            excepts += batch_files
    except json.JSONDecodeError:
        print_to_log(json_error[LAN], record_file, print_fun=print_warning)
        excepts += batch_files


def cot_identify(model, max_tokens, files, sleep_time, dataset_dir, record_file, m_result, result_file,
                 cot_prompt_fun1, cot_prompt_fun2):
    for f in files:
        file = get_file(f)
        content = read_file(str(file.absolute()))
        prompt = cot_prompt_fun1(name=file.name, code=content, count=1)
        print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                     record_file)
        response = generate_response(prompt, model=model, max_tokens=max_tokens)
        print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, record_file)

        prompt2 = cot_prompt_fun1(name=file.name, code=code, count=2, response=response)
        print_to_log(f'Prompt({num_tokens_from_messages(prompt2, model=model)} tokens): ' + friendly_prompt(prompt2),
                     record_file)
        response2 = generate_response(prompt2, model=model, max_tokens=max_tokens)
        print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response2, record_file)
        write_file(m_result, json.dumps(response2, indent=4, ensure_ascii=False))

        prompt3 = cot_prompt_fun2(code, response2)
        print_to_log(f'Prompt({num_tokens_from_messages(prompt3, model=model)} tokens): ' + friendly_prompt(prompt3),
                     record_file)
        response3 = generate_response(prompt3, model=model, max_tokens=max_tokens)
        write_file(m_result, json.dumps(response3, indent=4, ensure_ascii=False))


def identify_loop(model, max_tokens, files, batch, sleep_time, dataset_dir, record_file, result_file,
                  identify_prompt_fun, append_file_prompt_fun, process_response_fun):
    # 此函数用于识别循环处理文件，生成提示并处理响应。
    # 参数:
    # model: 使用的模型
    # max_tokens: 生成的最大token数
    # files: 待处理的文件列表
    # batch: 每次处理的文件数量
    # sleep_time: 每次处理之间的休眠时间
    # dataset_dir: 数据集目录
    # record_file: 记录文件
    # result_file: 结果文件
    # identify_prompt_fun: 生成识别提示的函数
    # append_file_prompt_fun: 追加文件提示的函数
    # process_response_fun: 处理响应的函数
    # 返回值:
    # excepts: 异常列表

    count = 0
    excepts = []
    while True:
        batch_files = []
        for i in range(count, count + batch):
            if i == len(files):
                break
            batch_files.append(files[i])
        prompt = identify_prompt_fun(len(batch_files), [i.name for i in batch_files])
        for i in batch_files:
            content = read_file(str(i.absolute()))
            prompt += append_file_prompt_fun(i.name, content)

        print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                     record_file)
        response = generate_response(prompt, model=model, max_tokens=max_tokens)
        print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, record_file)

        process_response_fun(batch_files, response, dataset_dir, result_file, record_file, excepts, lan=LAN)
        print_to_log(f'Debug Information, Now excepts: {excepts}', record_file, print_fun=print_debug)
        count += batch
        if count >= len(files):
            break

        time.sleep(sleep_time)

    return excepts


def merge2(model, max_tokens, input_result1, input_result2, record_dir=RECORD_DIR, result_dir=RESULT_DIR):
    """

    :param model:
    :param max_tokens:
    :param input_result1: append list
    :param input_result2:
    :param record_dir:
    :param result_dir:
    :return:
    """
    print('*****************************************************************')
    task_name = 'merge2'
    timestamp = get_formatted_datetime()
    record_file = record_dir + '/' + task_name + '-' + timestamp.replace(':', '_') + '.txt'
    result_file = result_dir + '/' + task_name + '-' + timestamp.replace(':', '_') + '.json'
    ensure_file_exists(record_file)
    ensure_file_exists(result_file)
    clear_file(record_file)
    clear_file(result_file)
    list1 = read_json(input_result1)
    list2 = read_json(input_result2)
    append = []
    for i in list1:
        flag = 0
        for j in list2:
            prompt = merge2_prompt(i, j)
            print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                         record_file)
            response = generate_response(prompt, model=model, max_tokens=max_tokens)
            print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, record_file)

            if response.find('YES') >= 0:
                flag = 1
                break
        if flag == 0:
            append.append(i)
    list2 += append
    write_file(result_file, json.dumps(list2, indent=4, ensure_ascii=False))
    return append


def append(model, max_tokens, previous_taxonomy, input_append, record_dir=RECORD_DIR, result_dir=RESULT_DIR,
           base_file=None):
    print('*****************************************************************')
    task_name = 'append'
    timestamp = get_formatted_datetime()
    record_file = record_dir + '/' + task_name + '-' + timestamp.replace(':', '_') + '.txt'
    ensure_file_exists(record_file)
    clear_file(record_file)
    print_to_log(f'******************** Append Phase *****************************', record_file)
    to_append = input_append
    prompts = append_dimension_prompt(previous_taxonomy, to_append, None)
    layer = 0  # 0 # 1
    for prompt in prompts:
        response = generate_response(prompt, model=model, max_tokens=max_tokens)
        print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                     record_file)
        result_file = result_dir + '/' + task_name + f'-{str(layer)}-op' + '.txt'
        print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, record_file)

        ensure_file_exists(result_file)
        clear_file(result_file)

        if response[0:3] == '***' and response[-3:] == '***':
            write_file(result_file, response[3:-3].strip())
        a = parse_taxonomy(base_file)
        b = parse_taxonomy(result_file)
        c = merge_taxonomy(a, b)
        clear_file(result_file)
        write_file(result_file, trans_taxonomy(c))

        missing = []
        for i in to_append:
            if response.find(i['abstract']) < 0:
                missing.append(i)
        if len(missing) > 0:
            print(missing)

            taxonomy = read_file(result_file)
            prompt2 = append_dimension_prompt(previous_taxonomy, missing, taxonomy)[0]
            print_to_log(
                f'Prompt({num_tokens_from_messages(prompt2, model=model)} tokens): ' + friendly_prompt(prompt2),
                record_file)
            response2 = generate_response(prompt2, model=model, max_tokens=max_tokens)
            print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response2, record_file)
            if response2[0:3] == '***' and response2[-3:] == '***':
                clear_file(result_file)
                write_file(result_file, response2[3:-3].strip())
            d = parse_taxonomy(result_file)
            e = merge_taxonomy(c, d)
            clear_file(result_file)
            write_file(result_file, trans_taxonomy(e))
        layer += 1


# def generalise(model, max_tokens, input_terms, input_previous_result, record_dir=RECORD_DIR, result_dir=RESULT_DIR):
def generalise(model, max_tokens, input_previous_result, record_dir=RECORD_DIR, result_dir=RESULT_DIR):
    print('*****************************************************************')
    task_name = 'generalise'
    timestamp = get_formatted_datetime()
    # record_file = record_dir + task_name + str(get_filename(input_previous_result))[25:] + '.txt'
    record_file = record_dir + task_name + '-' + timestamp.replace(':', '_') + '.txt'
    # result_file = result_dir + task_name + str(get_filename(input_previous_result))[25:] + '.txt'
    ensure_file_exists(record_file)
    clear_file(record_file)
    print_to_log(f'******************** Generalise Phase *****************************', record_file)
    previous_result = read_json(input_previous_result)
    # terms = read_json(input_terms)
    # prompt = generalise_prompt(terms, previous_result)
    prompts = dimension_prompt(previous_result)
    layer = 0
    for prompt in prompts:
        print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                     record_file)
        response = generate_response(prompt, model=model, max_tokens=max_tokens)
        print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, record_file)

        result_file = result_dir + '/' + task_name + f'-{str(layer)}-' + timestamp.replace(':', '_') + '.txt'
        ensure_file_exists(result_file)
        clear_file(result_file)

        if response[0:3] == '***' and response[-3:] == '***':
            write_file(result_file, response[3:-3].strip())

        missing = []
        for i in previous_result:
            if response.find(i['abstract']) < 0:
                missing.append(i)
        if len(missing) > 0:
            taxonomy = read_file(result_file)
            dimension = 'generic causes'
            if layer == 0:
                dimension = 'generic causes'
            elif layer == 1:
                dimension = 'cryptosystem components'
            elif layer == 2:
                dimension = 'security properties'
            prompt2 = tune_prompt(dimension, taxonomy, missing)
            print_to_log(
                f'Prompt({num_tokens_from_messages(prompt2, model=model)} tokens): ' + friendly_prompt(prompt2),
                record_file)
            response2 = generate_response(prompt2, model=model, max_tokens=max_tokens)
            print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response2, record_file)
            if response2[0:3] == '***' and response2[-3:] == '***':
                clear_file(result_file)
                write_file(result_file, response2[3:-3].strip())
        layer += 1


def base_task(model, max_tokens, task_name, input_json_file, prompt_fun,
              record_dir=RECORD_DIR, result_dir=RESULT_DIR):
    print('*****************************************************************')
    integrate_result_list = []
    # task_log_filename = f'{task_name}-' + get_filename(input_json_file) + '.txt'
    task_log_filename = f'/{task_name}' + '.txt'
    # task_result_filename = f'{task_name}-' + get_filename(input_json_file) + '.json'
    task_result_filename = f'/{task_name}' + '.json'
    task_record = record_dir + task_log_filename
    task_result = result_dir + task_result_filename

    ensure_file_exists(task_record)
    ensure_file_exists(task_result)
    clear_file(task_record)
    clear_file(task_result)
    print_to_log(f'******************** {task_name.capitalize()} Task *****************************', task_record)
    previous_result = read_json(input_json_file)
    prompt = prompt_fun(previous_result)
    print_to_log(f'Prompt({num_tokens_from_messages(prompt, model=model)} tokens): ' + friendly_prompt(prompt),
                 task_record)
    response = generate_response(prompt, model=model, max_tokens=max_tokens)
    print_to_log(f'Answer({num_tokens_from_string(response, model=model)} tokens): ' + response, task_record)

    if response.find('```json') >= 0:
        integrate_result = extract_pattern_strings(response)
        integrate_result_list += merge_nested_lists(string_list_to_json_list(integrate_result))
    write_file(task_result, json.dumps(integrate_result_list, indent=4, ensure_ascii=False))

    return task_result


def identify(dataset_dir, types, model, max_tokens, random=False, record_dir=RECORD_DIR, result_dir=RESULT_DIR):
    """
    根据给定的参数执行密码误用识别任务，包括直接识别和CoT识别阶段。

    参数:
    random: bool, 是否对数据集文件进行随机排序
    dataset_dir: str, 数据集所在目录
    types: list, 允许的文件后缀类型列表
    model: str, 使用的大语言模型
    max_tokens: int, 模型能处理的最大token数
    record_dir: str, 记录文件的存储目录，默认值为RECORD_DIR
    result_dir: str, 结果文件的存储目录，默认值为RESULT_DIR
    """
    print('*****************************************************************')

    # 获取数据集文件列表
    files = get_dataset(dataset_dir=dataset_dir, suffixes=types)
    # 是否打乱顺序
    if random:
        random.shuffle(files)

    # 均转换为绝对路径列表
    if isinstance(type(files[0]), str):
        all_files = get_path_by_filename(files, dataset_dir)
    else:
        all_files = files

    # 获取当前时间作为批次时间，并构建记录文件和结果文件名
    batch_time = get_formatted_datetime()
    log_filename = '/identify-' + batch_time.replace(':', '_') + '.txt'
    result_filename = '/identify-' + batch_time.replace(':', '_') + '.json'
    result_filename1 = '/identify1-' + batch_time.replace(':', '_') + '.json'
    result_filename2 = '/identify2-' + batch_time.replace(':', '_') + '.json'
    identify_record = record_dir + log_filename
    identify_result = result_dir + result_filename
    identify_result1 = result_dir + result_filename
    identify_result2 = result_dir + result_filename

    ensure_file_exists(identify_record)
    clear_file(identify_record)
    ensure_file_exists(identify_result)
    clear_file(identify_result)

    # 记录识别阶段的开始信息
    print_to_log(f'******************** Identify Phase *****************************', identify_record)
    print_to_log(f'******************** Step 1. direct identification **************************', identify_record)

    begin_time = time.time()
    num = len(all_files)  # 数据集文件总数
    batch = BATCH  # 每批次处理的文件数
    excepts = []  # 异常文件列表
    for i in range(0, ROUND):
        if i > 0:
            # 重复提交，消除因输出格式错误导致的 missing
            print_to_log(resubmit_warning[LAN], identify_record, print_fun=print_notice)
            batch = BATCH - 1
        # 执行识别循环，处理异常情况
        excepts = identify_loop(model, max_tokens, all_files, batch, 5, dataset_dir, identify_record, identify_result,
                                identify_prompt, append_file_prompt, process_identify_response)
        if not excepts or len(excepts) == 0:
            print_to_log(success_hint[LAN], identify_record, print_fun=print_notice)
            break
        all_files = copy.deepcopy(excepts)

    if excepts or len(excepts) > 0:
        # 消除格式错误后仍有 missing，则需要 CoT 识别
        print_to_log(f'{fail_warning[LAN]}{format_list(all_files)}{stop[LAN]}', identify_record)
        print_to_log(f'******************** Step 2. CoT identification **************************', identify_record)
        # print(type(excepts), excepts)
        cot_identify(model, max_tokens, excepts, 5, dataset_dir, identify_record, identify_result1, identify_result2,
                     cot_prompt, knowledge_prompt)

    end_time = time.time()
    # 记录识别阶段的结束信息，包括总耗时、文件总数、异常文件、使用的模型和批次时间
    print_to_log(f'******************** Identify End ****************************', identify_record)
    print_to_log(f'total time(s): {end_time - begin_time}', identify_record)
    print_to_log(f'total codes: {num}', identify_record)
    print_to_log(f'excepted codes: ({len(excepts)}){excepts}', identify_record)
    print_to_log(f'model: {model}', identify_record)
    print_to_log(f'batch time: {batch_time}', identify_record)


def main():
    """
    Usage:
        main.py identify --dataset=<dir> --types=<types> --model=<model> --tokens=<max_tokens> [--random]
        main.py paraphrase --input=<files> --model=<model> --tokens=<max_tokens>
        main.py generalise --misuses=<file1> --model=<model> --tokens=<max_tokens>
        main.py merge2 --misuse1=<m1> --misuse2=<m22> --model=<model> --tokens=<max_tokens>

    Options:
        --dataset=<dir>       Directory of the dataset to process.
        --types=<types>       Comma-separated list of file types to include.
        --model=<model>       The model to use for identification.
        --tokens=<max_tokens> Maximum number of tokens to use.
        --random              Use random selection of files [default: False].
        --input=<files>...    List of JSON files to merge.
        -h --help             Show this screen.
    """
    # main.py generalise - -misuses = < file1 > --terms = < file2 > --model = < model > --tokens = < max_tokens >

    arguments = docopt(main.__doc__)
    # print(arguments)

    if arguments['identify']:
        data_dir = arguments['--dataset']
        file_types = arguments['--types'].split(',')
        my_model = arguments['--model']
        my_tokens = int(arguments['--tokens'])
        random_selection = arguments['--random']
        identify(random=random_selection, dataset_dir=data_dir, types=file_types, model=my_model, max_tokens=my_tokens)
    elif arguments['paraphrase']:
        input_file = arguments['--input']
        my_model = arguments['--model']
        my_tokens = int(arguments['--tokens'])
        output_result = base_task(model=my_model, max_tokens=my_tokens, task_name='merge', prompt_fun=merge_prompt,
                                  input_json_file=input_file)

        base_task(model=my_model, max_tokens=my_tokens, task_name='paraphrase', prompt_fun=paraphrase_prompt,
                  input_json_file=output_result)
    elif arguments['generalise']:
        my_model = arguments['--model']
        my_tokens = int(arguments['--tokens'])
        my_previous_result = arguments['--misuses']
        generalise(model=my_model, max_tokens=my_tokens, input_previous_result=my_previous_result)
    elif arguments['merge2']:
        my_model = arguments['--model']
        my_tokens = int(arguments['--tokens'])
        misuse1 = arguments['--misuse1']
        misuse2 = arguments['--misuse2']
        merge2(model=my_model, max_tokens=my_tokens, input_result1=misuse1, input_result2=misuse2)


if __name__ == '__main__':
    main()
