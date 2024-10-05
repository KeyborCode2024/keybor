import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import csv
import time
from itertools import islice
import os
import argparse

def parse_options():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-i', '--input', help='The path of input', required=True)
    parser.add_argument('-o', '--output', help='The path of output.', required=True)
    parser.add_argument('-m', '--model', help='The model of node embedding. (struct: Struc2vec, Role2vec, Graphwave, Attribute: MUSAE, AE)', required=True)
    # parser.add_argument('-t', '--type', help='The type of pairs(noclone,type_1-6.', required=True)
    args = parser.parse_args()
    return args


def func_vector(file):
    try:
        df = pd.read_csv(file, header=None, index_col=0)
        vector = list(df.sum())
        return np.array(vector)
    except:
        print(file)
        return np.array([0 for i in range(0,128)])
    # print(len(vector))
    # if len(vector) < 128:
    #     vector.extend(0 for i in range(128-len(vector)))

def sim(pair, path):
    dir = path + pair
    file1 = dir + '/emb1.csv'
    file2 = dir + '/emb2.csv'
    if os.path.exists(file1) and os.path.exists(file2):
        matrix1 = func_vector(file1).reshape(1, -1)
        matrix2 = func_vector(file2).reshape(1, -1)
        cos = float(cosine_similarity(matrix1, matrix2))
        return cos
    else:
        return None


def create_and_save_cos(dir_name, model, type, out_file):
    emb_sent2vec_path = dir_name + 'Sent2vec/' + type + '/'
    emb_node2vec_path = dir_name + model + '/' + type + '/'
    emb_node2vec_nokey_path = dir_name + model + '_nokey/' + type + '/'
    emb_node2vec_topic_path = dir_name + model + '_topic/' + type + '/'
    Pairs = os.listdir(emb_node2vec_path)

    Struct_models = ['Struc2vec', 'Role2vec']
    Attribute_models = ['MUSAE', 'AE']
    if model in Struct_models:
        models = ['sent2vec', 'node2vec', 'node2vec_topic', 'node2vec_nokey','avg_node2vec', 'avg_node2vec_topic', 'avg_node2vec_nokey']
        df = pd.DataFrame(index = models, columns=Pairs)
        for pair in Pairs:
            cos_sent2vec = sim(pair, emb_sent2vec_path)
            cos_node2vec = sim(pair, emb_node2vec_path)
            cos_node2vec_topic = sim(pair, emb_node2vec_topic_path)
            cos_node2vec_nokey = sim(pair, emb_node2vec_nokey_path)
            df.loc['sent2vec'][pair] = cos_sent2vec
            df.loc['node2vec'][pair] = cos_node2vec
            df.loc['node2vec_topic'][pair] = cos_node2vec_topic
            df.loc['node2vec_nokey'][pair] = cos_node2vec_nokey
            
            if cos_sent2vec and cos_node2vec and cos_node2vec_topic and cos_node2vec_nokey:
                df.loc['avg_node2vec'][pair] = (cos_sent2vec + cos_node2vec)/2
                df.loc['avg_node2vec_topic'][pair] = (cos_sent2vec + cos_node2vec_topic)/2
                df.loc['avg_node2vec_nokey'][pair] = (cos_sent2vec + cos_node2vec_nokey)/2
        df = df.dropna(axis=1)
        df.to_csv(out_file)
        # return df.mean(axis=1)
    elif model in Attribute_models:
        types = ['node2vec', 'node2vec_topic', 'node2vec_nokey']
        df = pd.DataFrame(index = types, columns=Pairs)
        for pair in Pairs:
            cos_node2vec = sim(pair, emb_node2vec_path)
            cos_node2vec_topic = sim(pair, emb_node2vec_topic_path)
            cos_node2vec_nokey = sim(pair, emb_node2vec_nokey_path)
            df.loc['node2vec'][pair] = cos_node2vec
            df.loc['node2vec_topic'][pair] = cos_node2vec_topic
            df.loc['node2vec_nokey'][pair] = cos_node2vec_nokey
        df = df.dropna(axis=1)
        # print(df.mean(axis=1))
        df.to_csv(out_file)
        # return df.mean(axis=1)
    else:
        print('Model Do Not Exist')


def main():
    args = parse_options()

    dir_name = args.input
    out_dir = args.output
    model = args.model

    if dir_name[-1] == '/':
        dir_name = dir_name
    else:
        dir_name += '/'
    

    if out_dir[-1] == '/':
        out_dir += model +'/'
    else:
        out_dir += '/' + model + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    types = ['type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'noclone']
    # mean_file = out_dir + 'mean.csv'
    # models = ['sent2vec', 'node2vec', 'node2vec_nokey','avg_node2vec', 'avg_node2vec_nokey']
    # df_mean = pd.DataFrame(index = models, columns=types)
    for type in types:
        out_file = out_dir + type + '.csv'
        create_and_save_cos(dir_name, model, type, out_file)
        # type_mean = create_and_save_cos(dir_name, model, type, out_file)
        # df_mean[type]=type_mean
    # df_mean.to_csv(mean_file)



if __name__ == '__main__':
    # python 5_sim.py -i ../emb -o ../cos -m Struc2vec
    main()


