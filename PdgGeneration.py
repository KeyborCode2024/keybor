import networkx as nx
import numpy as np
import argparse
import os
# import sent2vec
import pickle
import glob
from multiprocessing import Pool
from functools import partial
import javalang
import matplotlib.pyplot as plt

KeyWords = frozenset(['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
                      'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
                      'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
                      'import', 'instanceof', 'int', 'interface', 'long', 'native', 'nchronzed','new',
                      'package', 'private', 'protected', 'public', 'return', 'short', 'static','strictfp',
                      'super', 'switch', 'this', 'throw', 'throws', 'transient', 'try', 'void',
                      'volatile', 'while'])


def parse_options():
    parser = argparse.ArgumentParser(description='Image-based Vulnerability Detection.')
    parser.add_argument('-d', '--dot', help='The path of a dir which consists of some dot_files')
    parser.add_argument('-f', '--file', help='The path of a dir which consists of some java_files')
    parser.add_argument('-o', '--output', help='The path of output.', required=True)
    # parser.add_argument('-m', '--model', help='The path of model.', required=True)
    args = parser.parse_args()
    return args

def node_extraction(file, pdg):
    index = 0
    with open(file, 'r') as f:
        for line in f.readlines():
            index += 1
            code = line.expandtabs().strip('\n').strip(' ')
            # code = line.strip('{').strip('}').strip(';').strip(' ')
            if code and code != '{' and code != '}' and code != ';':
                if code != 'public class pair{':
                    keywords = []
                    tokens = list(javalang.tokenizer.tokenize(code))
                    for token in tokens:
                        if token.value in KeyWords:
                            keywords.append(token.value)
                    pdg.add_node(index, code=code, keywords=keywords)

def node_transform(line, dict):
    node_index = int(line.split(' ')[0].strip('\"'))
    if line.find('<SUB>')!=-1:
        line_index = int(line.split('<SUB>')[-1].split('</SUB>')[0])
        dict[node_index] = line_index

def edge_transform(line):
    # print(line)
    line = line.strip(' ')
    src_node = int(line.split(' ')[0].strip('\"'))
    dest_node = int(line.split(' ')[2].strip('\"'))
    # print(src_node, dest_node)
    return src_node, dest_node

def edge_extraction(dot):
    node_dict = {}
    edge_set= set()
    with open(dot,'r') as f:
        for line in f.readlines()[1:-1]:
            line = line.strip('\n')
            if line.find('->') == -1:
                node_transform(line, node_dict)
            else:
                src_node, dest_node = edge_transform(line)
                # print(src_node, dest_node)
                if src_node in node_dict and dest_node in node_dict:
                    edge_tup = (node_dict[src_node], node_dict[dest_node])
                    edge_set.add(edge_tup)
        # print(node_dict)
        # print(edge_set)
    return edge_set

def image_generation(file, path_dot, path_out):
    file_name = file.split('/')[-1].split('.java')[0]
    # print(file_name)
    dot = path_dot + file_name + '/0-pdg.dot'
    out_dot = path_out + file_name + '.dot'
    if os.path.exists(dot):
        try:
            pdg = nx.DiGraph()
            node_extraction(file, pdg)
            # print(pdg.nodes(data=True))
            edge_list = list(edge_extraction(dot))
            pdg.add_edges_from(edge_list)
            nx.drawing.nx_pydot.write_dot(pdg, out_dot)
        except:
            print('error')
    else:
        print('Dotfile do not exist :', file_name)

def main():
    args = parse_options()
    if args.dot[-1] == '/':
        path_dot = args.dot
    else:
        path_dot = args.dot + "/"

    if args.file[-1] == '/':
        path_file = args.file
    else:
        path_file = args.file + "/"

    path_out = args.output
    folder = os.path.exists(path_out)
    if not folder:
        os.makedirs(path_out)
    if path_out[-1] == '/':
        path_out = path_out
    else:
        path_out += '/'

    javafiles = glob.glob(path_file + '*.java')
    # print(javafiles)
    pool = Pool(10)
    pool.map(partial(image_generation, path_dot=path_dot, path_out=path_out), javafiles)




if __name__ == '__main__':
    main()