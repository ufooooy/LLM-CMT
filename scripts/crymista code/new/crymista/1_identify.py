
from pathlib import Path
import pandas as pd
from pipeline import Pipeline
from utility import extract_json_blocks, get_time, json_format_check, print_to, read_file, write_json


def identify(target_csv, error_times=3):
    run_time = get_time()
    log_file = 'log/identify-' + run_time.replace(':', '') + '.txt'
    result_file = 'result/identify-' + run_time.replace(':', '') + '.json'
    error_file = 'result/error-identify-' + run_time.replace(':', '') + '.json'

    model_file = 'model_parameters/deepseek.json'
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
        target_df[new_column2] = ''

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

if __name__ == "__main__":
    target_csv = 'deepseek.csv'
    identify(target_csv)