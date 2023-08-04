import os
import glob
import argparse
from multiprocessing import Pool
from functools import partial

def parse_options():
    parser = argparse.ArgumentParser(description='Extracting AST.')
    parser.add_argument('-i', '--input', help='The dir path of input java file', required=True, type=str)
    parser.add_argument('-o', '--output', help='The dir path of output', required=True, type=str)
    args = parser.parse_args()
    return args

def main():
    args = parse_options()
    input_path = args.input
    if input_path[-1] == '/':
        input_path = input_path
    else:
        input_path += '/'

    output_path = args.output
    folder = os.path.exists(output_path)
    if not folder:
        os.makedirs(output_path)
    if output_path[-1] == '/':
        output_path = output_path
    else:
        output_path += '/'

    files = glob.glob(input_path + '*.java')
    for file in files:
        name = file.split('/')[-1]
        out_file = output_path + name
        with open(file, "r") as f:
            contents = f.readlines()
        fw = open(out_file, "w")
        str = 'public class pair{'
        fw.write(str + '\n')
        fw.writelines(contents)
        fw.write('}')
        fw.close()

if __name__ == '__main__':
    main()
