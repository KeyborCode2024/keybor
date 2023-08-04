import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import csv
import time
from itertools import islice
import os
import argparse
import glob
from multiprocessing import Pool
from functools import partial

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

def cos(pair, path):
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

def create_and_save_cos(embs, emb_path, emb_nokey_path, out_path):
    models = ['node2vec', 'node2vec_nokey']
    df = pd.DataFrame(index = models, columns=embs)
    for pair in embs:
        cos_node2vec = cos(pair, emb_path)
        cos_node2vec_nokey = cos(pair, emb_nokey_path)
        df.loc['node2vec'][pair] = cos_node2vec
        df.loc['node2vec_nokey'][pair] = cos_node2vec_nokey
    df = df.dropna(axis=1)
    df.to_csv(out_path)

def main():
    # args = parse_options()

    # dir_name = args.input
    # out_dir = args.output
    # model = args.model

    # if dir_name[-1] == '/':
    #     dir_name = dir_name
    # else:
    #     dir_name += "/"
    # if out_dir[-1] == '/':
    #     out_dir += model +'/'
    # else:
    #     out_dir += '/' + model + '/'
    # if not os.path.exists(out_dir):
    #     os.makedirs(out_dir)
    # types = ['type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'noclone']
    # # models = ['node2vec', 'node2vec_nokey']
    # # df_mean = pd.DataFrame(index = models, columns=types)
    # for type in types:
    #     out_file = out_dir + type + '.csv'
    #     pairs_file = '../pair_csv/' + type + '.csv'
    #     # print(out_file,pairs_file)
    #     create_and_save_cos(out_file, pairs_file, dir_name, model, type)
    # #     type_mean = create_and_save_cos(out_file, pairs_file, dir_name, model, type)
    # #     df_mean[type]=type_mean
    # # df_mean.to_csv(mean_file)
    args = parse_options()
    emb_dir = args.input
    out_dir = args.output
    model = args.model

    if emb_dir[-1] == '/':
        emb_dir += model +'/'
        emb_nokey_dir = args.input + model + '_nokey/'
    else:
        emb_dir += '/' + model + '/'
        emb_nokey_dir = args.input + '/' + model + '_nokey/'

    if out_dir[-1] == '/':
        out_dir += model +'/'
    else:
        out_dir += '/' + model + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    types = ['type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'noclone']
    for type in types:
        emb_path = emb_dir + type + '/'
        emb_nokey_path = emb_nokey_dir + type + '/'
        embs = os.listdir(emb_path)
        out_csv = out_dir + type + '.csv'
        # print(emb_path, emb_nokey_path, out_csv)
        create_and_save_cos(embs, emb_path, emb_nokey_path, out_csv)
       



if __name__ == '__main__':
    # python 5_sim.py -i ../emb -o ../cos -m Struc2vec
    main()


