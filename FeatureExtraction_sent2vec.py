import networkx as nx
import numpy as np
import argparse
import os
import sent2vec
import pickle
import glob
from multiprocessing import Pool
from functools import partial

import pandas as pd
import csv


def parse_options():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-i', '--input', help='The path of a dir which consists of some dot_files', required=True)
    parser.add_argument('-o', '--out', help='The path of output.', required=True)
    # parser.add_argument('-t', '--type', help='The type of pairs(noclone,type_1-6.', required=True)
    # parser.add_argument('-m', '--model', help='The path of model.', required=True)
    args = parser.parse_args()
    return args


def graph_extraction(dot):
    graph = nx.drawing.nx_pydot.read_dot(dot)
    if '\\n' in graph.nodes():
        graph.remove_node('\\n')
    return graph


def sentence_embedding(sentence):
    emb = sent2vec_model.embed_sentence(sentence)
    return emb[0]


def sent_vec(G, emb_file):
    emb_file1 = emb_file + 'emb1.csv'
    emb_file2 = emb_file + 'emb2.csv'
    f1 = open(emb_file1, 'w', encoding='utf-8')
    csv_writer1 = csv.writer(f1)
    f2 = open(emb_file2, 'w', encoding='utf-8')
    csv_writer2 = csv.writer(f2)

    labels_code = nx.get_node_attributes(G, 'code')
    for label, code in labels_code.items():
        if not label.islower():
            vector = []
            code = eval(code)
            line_vec = sentence_embedding(code)
            vector.append(label)
            vector.extend(line_vec)
            if label[0] == 'G':
                csv_writer1.writerow(vector)
            elif label[0] == 'H':
                csv_writer2.writerow(vector)
            else:
                print(label)
    f1.close()
    f2.close()


def feature_extraction(dotfile, out):
    G = graph_extraction(dotfile)
    name = dotfile.split('/')[-1].split('.dot')[0]
    out_dir = out + name + '/'
    file1 = out_dir + 'emb1.csv'
    file2 = out_dir + 'emb2.csv'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        trained_model_path = '../sent2vec/model.bin'
        global sent2vec_model
        sent2vec_model = sent2vec.Sent2vecModel()
        sent2vec_model.load_model(trained_model_path)
        try:
            sent_vec(G,out_dir)
            print(name)
        except:
            print(name, 'error')
    else:
        print(name,'exist')
    # else:
    #     print(name,'exist')
        # sent2vec_model.release_shared_mem(trained_model_path)


def main():
    args = parse_options()
    dir_name = args.input
    out_path = args.out
    # type = args.type

    if dir_name[-1] == '/':
        dir_name = dir_name
    else:
        dir_name += "/"

    if out_path[-1] == '/':
        out_path = out_path
    else:
        out_path += '/'
    
    types = ['noclone','type_1','type_2','type_3','type_4','type_5','type_6']
    for type in types:
        dot_dir = dir_path + type + '/'
        dotfiles = glob.glob(dot_dir + '*.dot')
        out_dir = out_path + type + '/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        # print(type)
        # print(dot_dir,out_dir)

        pool = Pool(10)
        pool.map(partial(feature_extraction, out=out_dir), dotfiles)



if __name__ == '__main__':
    main()
    






