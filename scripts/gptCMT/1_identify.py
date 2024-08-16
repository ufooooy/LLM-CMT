from main import identify

if __name__ == "__main__":
    my_dataset_dir = 'FN analysis'
    my_types = ['.java', '.py']
    my_model = 'gpt-4-turbo-preview'    
    my_max_tokens = 4095   

    identify(random=False, dataset_dir=my_dataset_dir, types=my_types,
             model=my_model, max_tokens=my_max_tokens,
             record_dir=my_dataset_dir, result_dir=my_dataset_dir)
