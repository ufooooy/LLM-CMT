from abc import ABC, abstractmethod
from pathlib import Path
import re

import pandas as pd

from gpt import GPT
import time

from utility import extract_json_blocks, get_time, parse_taxonomy, print_to, read_file, trans_taxonomy, write_file, write_json, read_json


class Assembler(ABC):
    @abstractmethod
    def assemble(self, template_file, **kwargs):
        pass


class ConcreteAssembler(Assembler):
    def assemble(self, system_template, template_file, **kwargs):
        message = []
        # 如果存在系统设定
        if system_template:
            system_prompt = Path(system_template).read_text()
            message.append({"role": "system", "content": system_prompt})
        # 确保模板文件存在
        template = Path(template_file)
        if not template.exists():
            raise FileNotFoundError(f"Template file {template_file} not found")

        # 读取模板文件
        with open(template, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 替换模板中的占位符
        for key, value in kwargs.items():
            template_content = template_content.replace(f"{{{key}}}", str(value))

        message.append({"role": "user", "content": template_content})
        return message
    


class Pipeline:
    @staticmethod
    def task_one(model_file, system_promp_file, template_file, dynamic_data, check_fun, max_retries=3, sleep_time=2):
        '''
        model_file: 模型参数文件
        system_promp_file: 系统提示词文件
        template_file: 模板文件
        dynamic_data: 动态数据
        max_retries: 超时最大重试次数，默认为3次
        sleep_time: 每次重试的等待时间，默认为2秒
        return: 
            -1: 超时错误
            -2: 模型错误
            -3: 格式错误
            message: 提示词
            response_content: 回复内容
            prompt_tokens: 提示词token数
            completion_tokens: 回复token数
        '''
        # 装配提示词
        assembler = ConcreteAssembler()
        message = assembler.assemble(system_promp_file, template_file, **dynamic_data)
        # print(message)

        # 调用LLM
        llm = GPT(model_file)
        retries = 0

        while retries < max_retries:
            response = llm.query(message)
            if response == -1:
                retries += 1
                time.sleep(sleep_time) 
            elif response == -2:
                return -2
            else:
                break
        
        if response == -1:
            return -1
        
        # 处理回复
        assert isinstance(response, tuple)
        response_content, prompt_tokens, completion_tokens = response
        if check_fun:
            if 1 != check_fun(response_content):
                return -3

        return message, response_content, prompt_tokens, completion_tokens
    
def json_format_check(answer_text):
    json_result = extract_json_blocks(answer_text)
    if json_result:
        return 1
    return 0

def compare_check(answer_text):
    # 如果answer_text中有任意大小写的Yes，或任意大小写的No返回1
    if re.search(r'\b[Yy][Ee][Ss]\b|\b[Nn][Oo]\b', answer_text):
        return 1
    return 0

def get_append(answer_text):
    if re.search(r'\b[Yy][Ee][Ss]\b', answer_text):
        return 'Y'
    elif re.search(r'\b[Nn][Oo]\b', answer_text):
        return 'N'

def identify(model_file, target_csv, error_times=3):
    run_time = get_time()
    log_file = 'log/identify-' + run_time.replace(':', '') + '.txt'
    result_file = 'result/identify-' + run_time.replace(':', '') + '.json'
    error_file = 'result/error-identify-' + run_time.replace(':', '') + '.json'

    # model_file = 'model_parameters/deepseek.json'
    system_promp_file = 'prompts/system.txt'
    template_file = 'prompts/identify_one.txt'

    error_list = []
    result_list = []

    console_message = f'''
    #### identify a collection
    #### target: {target_csv}
    #### run time: {run_time}
    #### log file: {log_file}
    #### result file: {result_file}
    '''
    
    print_to(console_message, log_file)

    target_df = pd.read_csv(target_csv)
    # 增加新列并初始化
    new_column = 'Instance'
    new_column2 = 'Identify Result'
    if new_column not in target_df.columns:
        target_df[new_column] = -1
    if new_column2 not in target_df.columns:
        target_df[new_column2] = pd.Series(dtype='str')  # 明确指定为字符串类型

    files = target_df['path'].tolist()
    error_count = 0
    process_count = 0
    for file in files:
        assert Path(file).is_file()

        # 跳过处理Instance大于等于0的行
        if target_df.loc[target_df['path'] == file, new_column].values[0] >= 0:
            continue
        # 设置动态数据
        dynamic_data = {
            'file_name': Path(file).name,
            'file_content': read_file(file)
        }
        result = Pipeline.task_one(model_file, system_promp_file, template_file, dynamic_data, json_format_check)
        if result in [-1, -2, -3]:
            error_count += 1
            if error_count >= error_times:
                print_to("Three consecutive files have resulted in errors. Please check the error records.", log_file)
                break
        else:
            error_count = 0

            query, response, prompt_tokens, completion_tokens = result
            print_to(f'{prompt_tokens} query has been sent, {completion_tokens} tokens have been received', log_file)
            json_result = extract_json_blocks(response)

            
            # 将json_result写入result_file
            cam_num = 0
            for item in json_result:
                item['code'] = file
                if item not in result_list:
                    result_list.append(item)
            
            target_df.loc[target_df['path'] == file, new_column] = len(json_result)
            target_df.loc[target_df['path'] == file, new_column2] = result_file
        
        process_count += 1
        # 每次更新target_df就写入文件并写入result
        target_df.to_csv(target_csv, index=False)
        write_json(result_file, result_list)
    
    # 保存结果和错误记录
    write_json(error_file, error_list)
    print_to(f'#### {process_count} files processed, {len(result_list)} misuses found, {len(error_list)} errors',log_file)

def classify_one_batch(model, data):
    run_time = get_time()
    log_file = 'log/classify-' + run_time.replace(':', '') + '.txt'
    result_file = 'result/classify-' + run_time.replace(':', '') + '.json'
    error_file = 'result/error-classify-' + run_time.replace(':', '') + '.json'

    console_message = f'''
    #### classify a batch
    #### target number: {len(data)}
    #### run time: {run_time}
    #### log file: {log_file}
    #### result file: {result_file}
    '''
    print_to(message=console_message, file=log_file)

    # 合并+总结
    print_to(message='#### begin merge step', file=log_file)
    template_file = 'prompts/merge.txt'
    system_promp_file = 'prompts/system.txt'
    dynamic_data = {
        'file_content': data
    }
    result = Pipeline().task_one(model, system_promp_file, template_file, dynamic_data, json_format_check)

    # 记录错误
    error_record = []
    if result in [-1, -2, -3]:
        error_record.append({'target': data, 'error': result})
        print(error_record)
        write_json(error_file, error_record)
        return -1, str(result_file)
    # 保存正确结果
    else:
        query, response_text, prompt_tokens, answer_tokens = result
        print_to(message=f'Prompt({prompt_tokens}): {query}', file=log_file)
        print_to(message=f'Answer({answer_tokens}): {response_text}', file=log_file)
        json_result = extract_json_blocks(response_text)
        # save file
        write_json(result_file, json_result)
        print_to(message=f'#### classify {len(data)} instances into {len(json_result)} misuses', file=log_file)
        return len(json_result), str(result_file)

def classify(model_file, target_json, count_csv, batch_size=50):
    target = read_json(target_json)

    if len(target) > batch_size:
        batches = [target[i:i + batch_size] for i in range(0, len(target), batch_size)]
    else:
        batches = [target]
    
    # 建立统计分类结果csv
    existing_df = None
    if count_csv and Path(count_csv).exists():
        existing_df = pd.read_csv(count_csv)
    
    # 循环处理每个批次
    results_table = []
    for batch_data in batches:
        batch_order = batches.index(batch_data) + 1
        if existing_df is not None and not existing_df.empty: 
            existing_misuse_count = existing_df[existing_df['Batch Order'] == batch_order]['Misuse Count'].values[0] if not existing_df.empty else -1
            if existing_misuse_count > 0:
                continue
        mis_num, mis_file = classify_one_batch(model_file, batch_data)
        if existing_df is not None and not existing_df.empty and existing_misuse_count == -1:
            # 将 existing_df 对应数据更新，并且最后保存到count_file
            existing_df.loc[existing_df['Batch Order'] == batch_order, 'Misuse Count'] = mis_num
            existing_df.loc[existing_df['Batch Order'] == batch_order, 'Result File'] = mis_file
            existing_df.to_csv(count_csv, index=False)
        else:
            results_table.append({'Batch Order': batch_order, 'Instance Number': len(batch_data), 'Misuse Count': mis_num, 'Result File': mis_file})

    if results_table:
        results_df = pd.DataFrame(results_table)
        print(results_df)
        if count_csv:
            results_df.to_csv(count_csv, index=False)


def generalise(model, misuse_json, terms_txt, run_time):
    result_file = 'result/generalise-' + str(Path(misuse_json).stem) + '.txt'
    log_file = 'log/generalise-' + run_time.replace(':', '') + '.txt'
    console_message = f'#### generalise a taxonomy, misuse: {misuse_json}, terms: {terms_txt}'

    template_file = 'prompts/generalise.txt'
    system_promp_file = 'prompts/system.txt'
    terms = read_file(terms_txt)
    misuse = read_json(misuse_json)
    dynamic_data = {
        'json_content': misuse,
        'terms': terms
    }
    result = Pipeline.task_one(model, system_promp_file, template_file, dynamic_data, None)
    if result in [-1, -2, -3]:
        console_message += f', result: {result}'
        return -1
    else:
        query, response_text, prompt_tokens, answer_tokens = result
        taxonomy, leaf_num = parse_taxonomy(response_text)
        f_taxonomy, _= trans_taxonomy(taxonomy)
        
        # if leaf_num < len(misuse):
        #     return -1
        write_file(result_file, f_taxonomy)
        console_message += f'\nPrompt({prompt_tokens}): {query}\nAnswer({answer_tokens}): {response_text}'
        print(taxonomy)
        print_to(message=console_message, file=log_file)
        return result_file

def compare(model, input_data, log_file):
    '''input_data已经是list
    '''
    console_message = f'#### compare 2 misuses, first: {input_data[0]}, second: {input_data[1]}'

    template_file = 'prompts/compare.txt'
    system_promp_file = 'prompts/system.txt'
    dynamic_data = {
        'misuse1': input_data[0],
        'misuse2': input_data[1]
    }
    result = Pipeline.task_one(model, system_promp_file, template_file, dynamic_data, compare_check)
    if result in [-1,-2,-3]:
        console_message += f', result: {result}'
    else:
        query, response_text, prompt_tokens, answer_tokens = result
        console_message += f'\nPrompt({prompt_tokens}): {query}\nAnswer({answer_tokens}): {response_text}'
    print_to(message=console_message, file=log_file)
    return result

def merge_misuses(model, input_data, log_file):
    '''input_data已经是list'''

    console_message = f'#### merger 2 misuses, first: {input_data[0]}, second: {input_data[1]}'

    template_file = 'prompts/merge_misuse.txt'
    system_promp_file = 'prompts/system.txt'
    dynamic_data = {
        'misuse1': input_data[0],
        'misuse2': input_data[1]
    }
    result = Pipeline.task_one(model, system_promp_file, template_file, dynamic_data, json_format_check)
    if result in [-1,-2,-3]:
        console_message += f', result: {result}'
    else:
        query, response_text, prompt_tokens, answer_tokens = result
        console_message += f'\nPrompt({prompt_tokens}): {query}\nAnswer({answer_tokens}): {response_text}'
    print_to(message=console_message, file=log_file)
    return result
def set_append(model, target_csv):
    # target_csv为一个csv文件，补充代码将target赋值target_csv的Result File列的str列表
    target_df = pd.read_csv(target_csv)
    target = target_df['Result File'].tolist()
    
    # 如果target_df不存在Append Result列，则新建该列，并初始化为0
    if 'Append Result' not in target_df.columns:
        target_df['Append Result'] = 0
    
    # 如果target_df不存在Result Json列，则新建该列，并初始化为空
    if 'Result Json' not in target_df.columns:
        target_df['Result Json'] = ''

    # 确保target列表是json文件名列表，每个json文件存在
    for file_name in target:
        if not isinstance(file_name, str) or not file_name.endswith('.json'):
            raise ValueError("All elements in target must be JSON file names.")
        if not Path(file_name).exists():
            raise FileNotFoundError(f"File {file_name} does not exist.")
    
    base_data = read_json(target[0])
    target_df.at[0, 'Append Result'] = len(base_data)
    target_df.at[0, 'Result Json'] = target_df.at[0, 'Result File']

    for i in range(1, len(target)):
        if target_df.at[i, 'Append Result'] > 0 and target_df.at[i, 'Result Json']:
            base_data = read_json(target_df.at[i, 'Result Json'])
            continue
        run_time = get_time()
        log_file = 'log/append-' + run_time.replace(':', '') + '.txt'
        result_file = 'result/append-' + run_time.replace(':', '') + '.json'

        to_append = []
        next_data = read_json(target[i])
        for second in next_data:
            merged = False
            for first in base_data:
                temp_first = {'title': first['title'], 'explanation': first['explanation']}
                temp_second = {'title': second['title'], 'explanation': second['explanation']}
                result = compare(model, [temp_first, temp_second], log_file)
                if result in [-1, -2, -3]:
                    break
                _, response_text, _, _ = result
                flag = get_append(response_text)
                if flag == 'Y':
                    result2 = merge_misuses(model, [temp_first, temp_second], log_file)
                    if result2 in [-1, -2, -3]:
                        break
                    else:
                        _, response_text2, _, _ = result2
                        # 列表只装了一个字典元素
                        temp = extract_json_blocks(response_text2)[0]
                        temp['instances'] = list(set(first['instances'] + second['instances']))
                        first = temp
                        merged = True
                        break
            if not merged:
                to_append.append(second)
            if result in [-1, -2, -3]:
                break
        if result in [-1, -2, -3]:
            to_append = []
            break
        base_data.extend(to_append)
        # 保存每批append结果到result_file
        write_json(result_file, base_data)
        # 更新target_csv
        target_df.at[i, 'Append Result'] = len(base_data)
        target_df.at[i, 'Result Json'] = result_file
        # 每得到Append Result数据就写入到merge_count.csv中
        target_df.to_csv(target_csv, index=False)
def append_taxonomy(model, taxonomy_txt, misuse_json, terms_txt, run_time):
    result_file = 'result/append-' + str(Path(misuse_json).stem) + '.txt'
    log_file = 'log/append-' + run_time.replace(':', '') + '.txt'
    console_message = f'#### append a taxonomy, misuse: {misuse_json}, terms: {terms_txt}'

    template_file = 'prompts/append.txt'
    system_promp_file = 'prompts/system.txt'
    terms = read_file(terms_txt)
    base_taxonomy_content = read_file(taxonomy_txt)
    misuse = read_json(misuse_json)
    dynamic_data = {
        'terms': terms,
        'taxonomy': base_taxonomy_content,
        'json_content': misuse
    }
    result = Pipeline.task_one(model, system_promp_file, template_file, dynamic_data, None)

    if result in [-1, -2, -3]:
        console_message += f', result: {result}'
    else:
        query, response_text, prompt_tokens, answer_tokens = result
        # print(response_text)
        taxonomy, leaf_num = parse_taxonomy(response_text)
        # print(trans_taxonomy(taxonomy)[0])
        base_taxonomy, base_leaf_num = parse_taxonomy(base_taxonomy_content)
        # f_taxonomy, f_leaf_num = trans_taxonomy(merge_taxonomy(base_taxonomy, taxonomy))
        # print(f_taxonomy)
        write_file(result_file, trans_taxonomy(taxonomy)[0])  
        # if leaf_num < len(misuse) or (f_leaf_num - base_leaf_num) < len(misuse):
        #     return -1
        console_message += f'\nPrompt({prompt_tokens}): {query}\nAnswer({answer_tokens}): {response_text}'
        print_to(message=console_message, file=log_file)
        return result_file
def construct(model, target_csv, terms_txt='prompts/keywords1.txt'):
    run_time = get_time()
    target_df = pd.read_csv(target_csv)

    for index, row in target_df.iterrows():
        if not pd.isna(target_df.at[index, 'Result TXT']):
            continue
        
        # If Batch Order is 1, read the file and run generalise
        if row['Batch Order'] == 1:
            # 获取Result File列中的文件路径
            file_path = row['Result File']  # 修改这里，使用Result File列而不是Append Result
            result = generalise(model, file_path, terms_txt, run_time)
            target_df.at[index, 'Result TXT'] = str(result)
            target_df.to_csv(target_csv, index=False)
            if result == -1:
                break
        else:
            previous_result = target_df.at[index - 1, 'Result TXT'] if index > 0 else None
            if row['Batch Order'] > 1 and previous_result != '0':  # 修改为字符串比较
                # 获取Result File列中的文件路径
                append_json_path = row['Result File']  # 修改这里，使用Result File列而不是Append Result
                taxonomy_txt = target_df.at[index - 1, 'Result TXT']
                result = append_taxonomy(model, append_json_path, terms_txt, taxonomy_txt, run_time)
                target_df.at[index, 'Result TXT'] = str(result)
                if result == -1:
                    break
    target_df.to_csv(target_csv, index=False)