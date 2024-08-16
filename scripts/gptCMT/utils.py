import codecs
import json
import os.path
import pathlib
import re

import chardet
import pandas as pd
import tiktoken

from datetime import datetime


def get_formatted_datetime():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 将日期和时间格式化为MySQL的DATETIME格式的字符串
    # MySQL的DATETIME格式为YYYY-MM-DD HH:MM:SS
    return current_datetime.strftime('%Y-%m-%d %H:%M:%S')


def remove_empty_entries(json_list, key):
    json_list = [entry for entry in json_list if entry.get(key) and entry[key]]
    return json_list


def merge_dicts(dicts, abstract, files, details, split=';'):
    """
    将字典根据共同的摘要键合并。
    :param dicts: 要合并的字典列表。
    :param abstract: 用于在每个字典中标识摘要的键。
    :param files: 用于在每个字典中标识文件的键。
    :param details: 用于在每个字典中标识细节的键。
    :param split: 用于连接细节的分隔符。默认为';'。
    :return: 合并后的字典列表。
    """
    merged_dict = {}
    for d in dicts:
        summary = d.get(abstract)
        if summary in merged_dict:
            if d.get(files) not in merged_dict[summary][files]:
                merged_dict[summary][files].extend(d.get(files))
                merged_dict[summary][details] += split + d.get(details)
        else:
            merged_dict[summary] = d
    return list(merged_dict.values())


def merge_nested_lists(nested_list):
    # 合并嵌套的列表并返回一个新的列表
    # 输入参数 nested_list: 包含子列表的嵌套列表
    # 返回值 merged_list: 所有子列表中元素合并的结果列表
    merged_list = []
    for sublist in nested_list:
        merged_list.extend(sublist)
    return merged_list


# 定义一个函数，将字符串列表转换为 JSON 对象列表
def string_list_to_json_list(string_list):
    # 创建一个空列表用于存储转换后的 JSON 对象
    dict_list = []
    # 遍历字符串列表
    for string in string_list:
        # 尝试解析字符串为 JSON 对象并将其添加到列表中
        try:
            dict_list.append(json.loads(string))
        # 捕获 JSON 解析错误并打印出错信息
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from string: {string}")

    # 返回转换后的 JSON 对象列表
    return dict_list


def extract_pattern_strings(text, pattern=r"```json(.*?)```"):
    # pattern = r"```json(.*?)```"
    json_strings = re.findall(pattern, text, re.DOTALL)
    return json_strings


def clear_file(file_path):
    if os.path.exists(file_path):
        open(file_path, 'w').close()


def add_file(file_path, content):
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write(content + '\n')


def write_file(file_path, content):
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(content)


def read_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            try:
                json_list = json.load(file)
            except json.JSONDecodeError:
                json_list = []
            return json_list


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(4096)  # 读取文件的前4096字节来猜测编码
    result = chardet.detect(raw_data)
    return result['encoding']


def read_file(file_path):
    file_content = None
    if os.path.exists(file_path):
        try:
            with codecs.open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
                file_content = file.read()
        except UnicodeDecodeError:
            print(f"Unicode decode error encountered while reading {file_path}")
            file_content = None
    return file_content


def print_warning(message):
    print("\033[1;31m" + message + "\033[0m")


def print_notice(message):
    print("\033[1;33m" + message + "\033[0m")


def print_debug(message):
    print("\033[1;33m" + message + "\033[0m")


def print_to_log(message, log, print_fun=print):
    print_fun(message)
    add_file(log, message)


def get_filename(path):
    file = pathlib.Path(path)
    if file.exists():
        return file.stem
    return None


def get_path_by_filename(filenames, dataset_dir):
    paths = []
    for filename in filenames:
        file_path = pathlib.Path(filename)
        dataset_file_path = pathlib.Path(dataset_dir) / filename
        if file_path.exists():
            paths.append(file_path)
        elif dataset_file_path.exists():
            paths.append(dataset_file_path)
    return paths


def get_file(filepath):
    return pathlib.Path(filepath)

def get_dataset(dataset_dir, suffixes, pattern='*'):
    """
    获取路径下文件和子文件夹下，限定后缀名的文件

    :param dataset_dir: 路径
    :param suffixes: 文件后缀列表
    :param pattern: 匹配模式
    :return: 符合条件的文件列表
    """
    all_files = []  # 存储符合条件的文件列表
    files = pathlib.Path(dataset_dir).rglob(pattern)  # 递归获取符合模式的所有文件
    for file in files:
        if pathlib.Path.is_file(file) and file.suffix in suffixes:  # 判断是否为文件且后缀名符合要求
            all_files.append(file)  # 将符合条件的文件添加到列表中
    return all_files  # 返回所有符合条件的文件列表


def format_list(alist, split='、'):
    return split.join(str(i) for i in alist)


def find_missing_file(all_files, now_files, key):
    missing_files = set(all_files) - set([file for entry in now_files for file in entry[key]])
    return list(missing_files)


def find_none_iterm(lst, key1, key2):
    """
    获取字典列表key1的值为空的key2值列表
    :param lst: 待处理字典列表
    :param key1: 用于检查空值的键
    :param key2: 返回值为空的键对应的值的列表
    :return: 返回 key1 的值为空的字典对应 key2 的值列表
    """
    none_lst = []
    for dic in lst:
        if dic[key1] == '':  # 检查 key1 的值是否为空
            none_lst += dic[key2]  # 将 key1 为空的字典对应 key2 的值加入列表
    return none_lst


def ensure_file_exists(file_path):
    """
    Checks if a file exists at the given path, and if not, creates it.
    :param file_path: The path to the file to check or create.
    """
    path = pathlib.Path(file_path)
    if not path.exists():
        path.touch()
        print(f"File created at {file_path}")
    else:
        print(f"File already exists at {file_path}")


def deduplicate_dict_list(dict_list, file_key):
    """
    对包含在字典列表中的文件列表进行去重，保持顺序不变。
    
    :param dict_list: 要处理的字典列表。
    :param file_key: 字典中包含需要去重的文件列表的键。
    :return: 一个新的字典列表，其中的文件列表已经去重。
    """
    for dic in dict_list:
        seen = set()
        dic[file_key] = [x for x in dic[file_key] if not (x in seen or seen.add(x))]
    return dict_list


# https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4-turbo-preview",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|im_start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    # elif "gpt-3.5-turbo" in model:
    #     print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
    #     return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    # elif "gpt-4" in model:
    #     print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
    #     return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai
            -python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|im_start|>assistant<|im_sep|>
    return num_tokens


def num_tokens_from_string(string, model):
    """
    从文本字符串中返回标记的数量
    :param string: 文本字符串
    :param model: 使用的模型
    :return: 文本字符串中的标记数量
    """
    # try:
    #     encoding = tiktoken.get_encoding(model)  # 获取指定模型的编码
    # except KeyError:
    #     print("Warning: model not found. Using cl100k_base encoding.")  # 打印警告消息，模型未找到，使用cl100k_base编码
    encoding = tiktoken.get_encoding("cl100k_base")  # 如果指定的模型未找到，则使用cl100k_base编码
    num_tokens = len(encoding.encode(string))  # 计算文本字符串中的标记数量
    return num_tokens


def export_json(json_file):
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Export the DataFrame to an Excel file
    excel_file = json_file.replace('.json', '.xlsx')
    df.to_excel(excel_file, index=False)


