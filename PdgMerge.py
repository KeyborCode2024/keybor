import networkx as nx
import numpy as np
import argparse
import os
# import sent2vec
import pickle
import glob
from multiprocessing import Pool
from functools import partial
import matplotlib.pyplot as plt
import csv

def parse_options():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-p', '--pairs', help='The path of pairs', required=True)
    parser.add_argument('-i', '--input', help='The path of input', required=True)
    parser.add_argument('-o', '--out', help='The path of output.', required=True)
    # parser.add_argument('-t', '--type', help='The type of pairs(noclone,type_1-6.', required=True)
    args = parser.parse_args()
    return args

# keywords up to JAVA; immutable set
KeyWords = frozenset(['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
                      'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
                      'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
                      'import', 'instanceof', 'int', 'interface', 'long', 'native', 'nchronzed','new',
                      'package', 'private', 'protected', 'public', 'return', 'short', 'static','strictfp',
                      'super', 'switch', 'this', 'throw', 'throws', 'transient', 'try', 'void',
                      'volatile', 'while'])
#运算符
# operator = frozenset(['+','-','*','/','%','++','--','+=','-=','+=','/=',#算术运算符
# 			'==','!=','>','<','>=','<=',#关系运算符
# 			'&','|','^','~','<<','>>','>>>',#位运算符
# 			'&&','||','!',#逻辑运算符
# 			'=','+=','-=','*=','/=','%=','<<=','>>=','&=','^=','|=',#赋值运算符
# 			'?:'])#条件运算符
#
# #界符
# delimiters = frozenset(['{','}','[',']','(',')','.',',',':',';'])

def graph_extraction(dot):
    graph = nx.drawing.nx_pydot.read_dot(dot)
    if '\\n' in graph.nodes():
        graph.remove_node('\\n')
    return graph

def edge_addition_list(U):
    edge_list = []
    for node in U.nodes:
        tokens = eval(eval(U.nodes[node]['keywords']))
        if tokens:
            for token in tokens:
                tuple = (node,token)
                edge_list.append(tuple)
    # print(edge_list)
    return edge_list


def graph_merge(pair, in_path, out_path):
    pair1 = str(pair[0])
    pair2 = str(pair[1])
    dotfile1 = in_path + pair1 + '.dot'
    dotfile2 = in_path + pair2 + '.dot'
    if not os.path.exists(dotfile1):
        print(pair1, ' : file do not exist\n')
    elif not os.path.exists(dotfile2):
        print(pair2, ' : file do not exist\n')
    else:
        try:
            outfile = out_path + pair1 + '_' + pair2 + '.dot'
            G = graph_extraction(dotfile1)
            H = graph_extraction(dotfile2)
            U = nx.union(G, H, rename=('G', 'H'))

            # 连接keywords
            edges = edge_addition_list(U)
            U.add_nodes_from(KeyWords)
            U.add_edges_from(edges)

            nx.drawing.nx_pydot.write_dot(U, outfile)
        except:
            print(pair1 + '_' + pair2 + ' : dot file read error!\n')

def main():
    args = parse_options()
    if args.pairs[-1] == '/':
        pairs_path = args.pairs
    else:
        pairs_path = args.pairs + '/'

    if args.input[-1] == '/':
        in_path = args.input
    else:
        in_path = args.input + '/'

    out_path = args.out
    folder = os.path.exists(out_path)
    if not folder:
        os.makedirs(out_path)
    if out_path[-1] == '/':
        path_out = out_path
    else:
        out_path += '/'


    types = ['noclone','type_1','type_2','type_3','type_4','type_5','type_6']

    for type in types:
        pairs_file = pairs_path + type + '.csv'
        outdir = out_path + type + '/'
        folder = os.path.exists(outdir)
        if not folder:
            os.makedirs(outdir)

        # pairs_file = '../test/pair_csv/noclone.csv'
        # in_path = '../test/pdg/'
        # out_path = '../test/images/'
        Pairs = []
        pairs = csv.reader(open(pairs_file, 'r', encoding='gbk'))
        for line in pairs:
            f1 = line[0]
            f2 = line[1]
            pair = (f1, f2)
            Pairs.append(pair)

        pool_num = 8
        pool = Pool(pool_num)
        pool.map(partial(graph_merge, in_path=in_path, out_path=outdir), Pairs)


if __name__ == '__main__':
    main()








