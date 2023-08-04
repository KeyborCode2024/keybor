from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score
import csv
import pandas as pd
import numpy as np
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-i', '--input', help='The path of a dir which consists of some cos result', required=True)
    parser.add_argument('-o', '--output', help='The path of result.', required=True)
    parser.add_argument('-m', '--model', help='The type of model.', required=True)
    args = parser.parse_args()
    return args

def getmetrics_clone(clonecos, threshold):
    test_y = []
    pred_y = []
        
    l = len(clonecos)
    for data in clonecos:
        test_y.append(1)
        if data >= threshold:
            pred_y.append(1)
        else:
            pred_y.append(0)

    recall = recall_score(y_true=test_y, y_pred=pred_y)
    return [recall,None]

def getmetrics_noclone(noclonecos, threshold):
    test_y = []
    pred_y = []
    l = len(noclonecos)
    for data in noclonecos:
        test_y.append(1)
        if data >= threshold:
            pred_y.append(0)
        else:
            pred_y.append(1)

    recall = recall_score(y_true=test_y, y_pred=pred_y)
    return [recall, None, None, None]


def getmetrics(clonecos, noclonecos, threshold):
    test_y = []
    pred_y = []

    num_clone = len(clonecos)
    num_noclone = len(noclonecos)
        
    for data in clonecos:
        test_y.append(1)
        if data >= threshold:
            pred_y.append(1)
        else:
            pred_y.append(0)

    for data in noclonecos:
        test_y.append(0)
        if data >= threshold:
            pred_y.append(1)
        else:
            pred_y.append(0)

   
    precision = precision_score(y_true=test_y, y_pred=pred_y)
    recall = recall_score(y_true=test_y, y_pred=pred_y)
    f1 = f1_score(y_true=test_y, y_pred=pred_y)
    accuracy = accuracy_score(y_true=test_y, y_pred=pred_y)
    # TP = np.sum(np.multiply(test_y, pred_y))
    # FP = np.sum(np.logical_and(np.equal(test_y, 0), np.equal(pred_y, 1)))
    # FN = np.sum(np.logical_and(np.equal(test_y, 1), np.equal(pred_y, 0)))
    # TN = np.sum(np.logical_and(np.equal(test_y, 0), np.equal(pred_y, 0)))

    # TPR = TP / (TP + FN)
    # FPR = FP / (FP + TN)
    # TNR = TN / (TN + FP)
    # FNR = FN / (TP + FN)
    return [recall, precision, f1, accuracy]

def Classification(dir_path, out_path, threshold, model):
    
    key_index = 'node2vec'
    nokey_index = 'node2vec_nokey'

    csv_data = [[] for i in range(20)]
    csv_data[0] = ['Type', 'Recall', 'Precision', 'F-measure', 'Accuracy']
    noclonepath = dir_path + 'noclone.csv'
    df_noclone = pd.read_csv(noclonepath,index_col=0,header=0)
    noclone_key = np.array(df_noclone.loc[key_index,:])
    noclone_nokey = np.array(df_noclone.loc[nokey_index,:])
    csv_data[1].append('noclone_key')
    csv_data[1].extend(getmetrics_noclone(noclone_key, threshold))
    csv_data[2].append('noclone_nokey')
    csv_data[2].extend(getmetrics_noclone(noclone_nokey, threshold))

    types = ['type_1', 'type_2', 'type_3', 'type_4','type_5', 'type_6']
    all_key = np.array([])
    all_nokey = np.array([])
    i = 3
    for t in types:
        clonepath = dir_path + t + '.csv'
        df_clone = pd.read_csv(clonepath,index_col=0,header=0)
        clone_key = np.array(df_clone.loc[key_index,:])
        clone_nokey = np.array(df_clone.loc[nokey_index,:])

        csv_data[i].append(t + '_key')
        csv_data[i].extend(getmetrics_clone(clone_key, threshold))
        i += 1
        csv_data[i].append(t + '_nokey')
        csv_data[i].extend(getmetrics_clone(clone_nokey, threshold))
        i +=1

        all_key = np.hstack((all_key,clone_key))
        all_nokey = np.hstack((all_nokey,clone_nokey))
    csv_data[i].append('all_key')
    csv_data[i].extend(getmetrics(all_key, noclone_key, threshold))
    i += 1
    csv_data[i].append('all_nokey')
    csv_data[i].extend(getmetrics(all_nokey, noclone_nokey, threshold))
    with open(out_path, 'w', newline='') as f:
        csvfile = csv.writer(f)
        csvfile.writerows(csv_data)

def main():
    args = parse_args()
    dir_path = args.input
    out_path = args.output
    model = args.model

    if dir_path[-1] == '/':
        dir_path = dir_path
    else:
        dir_path += '/'
    dir_path = dir_path + model + '/'

    if out_path[-1] == '/':
        out_path = out_path
    else:
        out_path += '/'
    out_path = out_path + model + '/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    thresholds = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    for t in thresholds:
        out_csv = out_path + str(int(t*100)) + '.csv'
        Classification(dir_path, out_csv, t, model)


if __name__ == '__main__':
    main()
    # noclonepath = '../cos_result/noclone.csv'
    # df_noclone = pd.read_csv(noclonepath,index_col=0,header=0)
    # noclone_key = np.array(df_noclone.loc['avg_key',:])
    # print(noclone_key)