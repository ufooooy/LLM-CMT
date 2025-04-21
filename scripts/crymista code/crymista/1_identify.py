
from pipeline import identify

if __name__ == "__main__":
    # 确保你指定的模型参数文件正确
    model = 'model_parameters/deepseek.json'
    identify_count = 'dsub.csv'
    identify(model, identify_count)
