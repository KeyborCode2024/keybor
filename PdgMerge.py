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
    parser.add_argument('-t', '--type', help='The type of pairs(noclone,type_1-6.', required=True)
    args = parser.parse_args()
    return args

# keywords up to JAVA; immutable set
# KeyWords = frozenset(['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
#                       'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
#                       'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
#                       'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 
#                       'private', 'protected', 'public', 'return', 'short', 'static','strictfp', 'super',
#                       'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void',
#                       'volatile', 'while'])


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

Topic_dict = { #访问控制
            'private':'access', 'protected':'access', 'public':'access', 
            #类，方法，变量修饰符
            'enum':'enum', 'class':'class', 'interface':'interface', 'extends':'extends',
            'implements':'implements', 'final':'final', 'abstract':'abstract', 'native':'native',
            'new':'new', 'static':'static','strictfp':'strictfp',
            'synchronized':'synchronized', 'transient':'transient', 'volatile':'volatile',
            #程序控制
            'break':'jump', 'continue':'jump', #跳转语句
            'do':'loop', 'for':'loop', 'while':'loop', #循环控制
            'switch':'condition', 'case':'condition', 'default':'condition', 'if':'condition', 'else':'condition', #条件分支
            'return':'return', 'instanceof':'instanceof', 
            #错误处理
            'try':'exception', 'catch':'exception', 'finally':'exception',
            'throw':'throw', 'throws':'throw',
            'assert':'assert',
            #包相关
            'package':'package', 'import':'package',
            #基本数据类型
            'byte':'integer', 'short':'integer', 'int':'integer', 'long':'integer',
            'float':'float', 'double':'float',
            'boolean':'boolean',
            'char':'char',
            #变量引用
            'super':'super', 'this':'this', 'void':'void', 
            #保留字
            'const':'const', 'goto':'goto'}
Topics = frozenset(Topic_dict.values())

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
                topic = Topic_dict[token]
                tup = (node,topic)
                # print(node,token,topic)
                edge_list.append(tup)
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
            # U.add_nodes_from(KeyWords)
            U.add_nodes_from(Topics)
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
        in_path = args.input + "/"

    out_path = args.out
    folder = os.path.exists(out_path)
    if not folder:
        os.makedirs(out_path)
    if out_path[-1] == '/':
        path_out = out_path
    else:
        out_path += '/'

    type = args.type

    pairs_file = pairs_path + type + '.csv'
    out_path = out_path + type + '/'
    folder = os.path.exists(out_path)
    if not folder:
        os.makedirs(out_path)

    # pairs_file = '../test/pair_csv/noclone.csv'
    # in_path = '../test/pdg/'
    # out_path = '../test/images_topic/'
    Pairs = []
    pairs = csv.reader(open(pairs_file, 'r', encoding='gbk'))
    for line in pairs:
        f1 = line[0]
        f2 = line[1]
        pair = (f1, f2)
        Pairs.append(pair)

    pool_num = 32
    pool = Pool(pool_num)
    pool.map(partial(graph_merge, in_path=in_path, out_path=out_path), Pairs)


if __name__ == '__main__':
    main()
    # pair = (2401,911773)
    # in_path = '../../test/pdg/'
    # out_path = '../../test/images_topic/type_1/'
    # graph_merge(pair,in_path, out_path)

    









