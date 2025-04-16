
from pipeline import identify

if __name__ == "__main__":
    model = 'model_parameters/deepseek.json'
    identify_count = 'dsub.csv'
    identify(model, identify_count)
