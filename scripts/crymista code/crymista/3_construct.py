import pandas as pd
from pipeline import construct, set_append
  
def new_colnums(classify_csv, colnum_name):
    # 读取CSV文件
    df = pd.read_csv(classify_csv)
    # 新增一列
    df[colnum_name] = pd.Series(dtype='str')
    # 将修改后的DataFrame保存回CSV文件
    df.to_csv(classify_csv, index=False)

if __name__ == '__main__':
    model = 'model_parameters/deepseek.json'
    classify_csv = 'classify_deepseek.csv'
    # set_append(model, classify_csv)

    # 为classify_csv添加一列Result TXT记录taxonomy结果
    new_colnums(classify_csv, 'Result TXT')

    construct(model, classify_csv)