'''
Reference implementation of node2vec.

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec
Knowledge Discovery and Data Mining (KDD), 2016
'''

import argparse
import numpy as np
import networkx as nx
import os
import csv
import glob
from multiprocessing import Pool
from functools import partial
from struc2vec import Struc2Vec
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-i', '--input', help='The dir path of input', required=True, type=str)
    parser.add_argument('-o', '--output', help='The dir path of output', required=True, type=str)
    # parser.add_argument('-t', '--type', help='The type of pairs(noclone,type_1-6.', required=True, type=str)
    args = parser.parse_args()
    return args


def graph_extraction(dot):
    graph = nx.drawing.nx_pydot.read_dot(dot)
    if '\\n' in graph.nodes():
        graph.remove_node('\\n')
    return graph


def save_embedding(emb_file, nodes, features):
    # save node embedding into emb_file with word2vec format
    emb_file1 = emb_file + 'emb1.csv'
    emb_file2 = emb_file + 'emb2.csv'
    f1 = open(emb_file1, 'w', encoding='utf-8')
    csv_writer1 = csv.writer(f1)
    f2 = open(emb_file2, 'w', encoding='utf-8')
    csv_writer2 = csv.writer(f2)
    # f_emb.write(str(len(features)) + " " + str(features.shape[1]) + "\n")
    for node in nodes:
        vector = []
        if not node.islower():
            vector.append(node)
            vector.extend(features[node])
            if node[0] == 'G':
                csv_writer1.writerow(vector)
            elif node[0] == 'H':
                csv_writer2.writerow(vector)
    f1.close()
    f2.close()


def feature_extraction(dotfile, out):
    name = dotfile.split('/')[-1].split('.dot')[0]
    temp_path='./temp/' + name + '/'
    out_dir = out + name + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    G = graph_extraction(dotfile)
    model = Struc2Vec(G, 10, 80, workers=4, verbose=40, temp_path=temp_path,)
    model.train()
    X = model.get_embeddings()
    save_embedding(out_dir, G.nodes, X)


def main():
    '''
	Pipeline for representational learning for all nodes in a graph.
	'''
    args = parse_args()
    dir_name = args.input
    out_path = args.output
    if dir_name[-1] == '/':
        dir_name = dir_name
    else:
        dir_name += "/"

    if out_path[-1] == '/':
        out_path = out_path
    else:
        out_path += '/'

    # type = args.type
    types = ['type_1','type_2','type_3','type_4','type_5','type_6']
    for type in types:
        dot_dir = dir_name + type + '/'
        dotfiles = glob.glob(dot_dir + '*.dot')
        out_dir = out_path + type + '/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        # print(type)
        # print(dot_dir,out_dir)

        pool = Pool(10)
        pool.map(partial(feature_extraction, out=out_dir), dotfiles)


if __name__ == "__main__":
    main()


