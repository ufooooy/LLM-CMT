import csv
import json
import pandas as pd

def calculate_accuracy(true_labels, predicted_labels):
    '''
    计算准确率
    args:
        true_labels: 真实的标签列表
        predicted_labels: 预测的标签列表
    return:
        accuracy: 准确率
    '''
    if len(true_labels) != len(predicted_labels):
        raise ValueError("The length of true_labels and predicted_labels must be the same.")
    
    correct_predictions = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == pred)
    total_predictions = len(true_labels)
    
    accuracy = correct_predictions / total_predictions
    print(f"Accuracy: {accuracy} = {correct_predictions} / {total_predictions}")

    return accuracy


def calculate_precision(true_labels, predicted_labels):
    '''
    计算精确率
    args:
        true_labels: 真实的标签列表
        predicted_labels: 预测的标签列表
    return:
        precision: 精确率
    '''
    if len(true_labels) != len(predicted_labels):
        raise ValueError("The length of true_labels and predicted_labels must be the same.")
    
    true_positives = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 1 and pred == 1)
    predicted_positives = sum(1 for pred in predicted_labels if pred == 1)
    
    if predicted_positives == 0:
        return 0.0  # Avoid division by zero
    
    precision = true_positives / predicted_positives
    print(f"Precision: {precision} = {true_positives} / {predicted_positives}")

    return precision


def calculate_recall(true_labels, predicted_labels):
    '''
    计算回召率
    args:
        true_labels: 真实的标签列表
        predicted_labels: 预测的标签列表
    return:
        recall: 回召率
    '''
    if len(true_labels) != len(predicted_labels):
        raise ValueError("The length of true_labels and predicted_labels must be the same.")
    
    true_positives = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 1 and pred == 1)
    actual_positives = sum(1 for true in true_labels if true == 1)
    
    if actual_positives == 0:
        return 0.0  # Avoid division by zero
    
    recall = true_positives / actual_positives
    print(f"Recall: {recall} = {true_positives} / {actual_positives}")

    return recall


# Calculate accuracy, precision, and recall
def acc1(csv_merge_file):
    # Load the CSV file
    df = pd.read_csv(csv_merge_file)

    # Extract the If_CAM and CAM_NUM columns
    t1 = df['If_CAM'].tolist()
    p1 = df['CAM_NUM'].tolist()

    # Filter out entries where CAM_NUM is -1
    filtered_t1 = [t for t, p in zip(t1, p1) if p != -1]
    # filtered_p1 = [p for p in p1 if p != -1]
    filtered_p1 = [1 if p > 0 else 0 for p in p1 if p != -1]


    # Count positive and negative samples in filtered_t1
    positive_samples = sum(1 for value in filtered_t1 if value == 1)
    negative_samples = sum(1 for value in filtered_t1 if value == 0)

    # Print the results
    print(f"Effective samples: {len(filtered_p1)}")
    print(f"Positive samples: {positive_samples}")
    print(f"Negative samples: {negative_samples}")
    
    # Calculate accuracy, precision, and recall
    accuracy = calculate_accuracy(filtered_t1, filtered_p1)
    precision = calculate_precision(filtered_t1, filtered_p1)
    recall = calculate_recall(filtered_t1, filtered_p1)


# Calculate FNR, FDR
def acc2(csv):
    df = pd.read_csv(csv)
    labels = 0
    predict = 0
    instances = 0
    err = 0
    for index, row in df.iterrows():
        if df.at[index, 'If_CAM'] == 1:
            labels += df.at[index, 'labels'].count(';') + 1
            predict += df.at[index, 'check']
            if df.at[index, 'CAM_NUM'] > 0:
                instances += df.at[index, 'CAM_NUM']
            if isinstance(df.at[index, 'err'], str):
                err += df.at[index, 'err'].count(';') + 1

    missing = (labels-predict)/labels
    err_ratio = err/instances
    print(f'{csv} label:{labels} predict:{predict} instances:{instances} missing:{missing}={labels-predict}/{labels} error:{err_ratio}={err}/{instances}')


acc2('identify_gpt4.csv')
acc2('identify_sonnet.csv')
acc2('identify_gemini.csv')
acc2('identify_llama.csv')


# print('gemini')
# acc1('identify_gemini.csv')
# print('\n')

# print('gpt3')
# acc1('identify_gpt3.csv')
# print('\n')

# print('gpt4')
# acc1('identify_gpt4.csv')
# print('\n')

# print('llama')
# acc1('identify_llama.csv')
# print('\n')

# print('sonnet')
# acc1('identify_sonnet.csv')
