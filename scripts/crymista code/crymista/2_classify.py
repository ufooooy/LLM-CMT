import json
from pathlib import Path
import pandas as pd
from pipeline import classify


def is_nomisuse(target_string):
    target = target_string.lower()
    nomisuse = 'No cryptographic API misuses'.lower()
    return target == nomisuse or nomisuse in target or target in nomisuse
    
def gather_nomis_instance(identify_csv, cam_json):
    # 读取CSV文件
    df = pd.read_csv(identify_csv)
    # 获取Identify Result文件路径，并过滤掉空值及-1
    filtered_df = df['Identify Result'].dropna()
    
    # 使用列表推导式优化循环处理
    cam_instances = []
    instance_id = 1  # 初始化instance_id计数器
    
    for file_path in filtered_df:
        try:
            with open(Path(file_path), 'r', encoding='utf-8') as f:
                json_data = json.load(f)  
            # 使用列表推导式优化过滤，同时添加instance_id
            temp_instance = [dict(item, instance_id=instance_id + i) 
                           for i, item in enumerate(json_data) 
                           if not is_nomisuse(item.get('abstract'))]
            cam_instances.extend(temp_instance)
            instance_id += len(temp_instance)  # 更新instance_id计数器
            # 去除重复项
            cam_instances = [dict(t) for t in {tuple(d.items()) for d in cam_instances}]
            # 去除location和code字段和值以节约token
            # for item in cam_instances:
            #     item.pop('location', None)
            #     item.pop('code', None)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue
    
    # 将结果写入JSON文件
    with open(cam_json, 'w', encoding='utf-8') as f:
        json.dump(cam_instances, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # 将识别过程得到的有误用instance集合到一起
    cams_instance_json = 'deepseek_cams.json'
    identify_count = 'dsub.csv'
    gather_nomis_instance(identify_count, cams_instance_json)

    # 运行分类过程
    model_parameter = 'model_parameters/deepseek.json'
    classify_count = 'classify_deepseek.csv'
    classify(model_parameter, cams_instance_json, classify_count)
    