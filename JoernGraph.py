import os
import glob
import argparse
from multiprocessing import Pool
from functools import partial

def parse_options():
    parser = argparse.ArgumentParser(description='Extracting AST.')
    parser.add_argument('-i', '--input', help='The dir path of input', required=True, type=str)
    parser.add_argument('-o', '--output', help='The dir path of output', required=True, type=str)
    parser.add_argument('-t', '--type', help='The type of procedures: parse or export', required=True, type=str)
    args = parser.parse_args()
    return args

def joern_parse(file, outdir):
    name = file.split('/')[-1].split('.java')[0]
    out = outdir + name + '.bin'
    if not os.path.exists(out):
        os.environ['file'] = str(file)
        os.environ['out'] = str(out)
        os.system('/home/wym/joern/joern-cli/joern-parse $file --output $out')  # --language c

def joern_export(bin, outdir):
    name = bin.split('/')[-1].split('.bin')[0]
    out = outdir + name
    if not os.path.exists(out):
        os.environ['bin'] = str(bin)
        os.environ['out'] = str(out)
        os.system('/home/wym/joern/joern-cli/joern-export $bin --repr pdg --out $out')
    


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

    pool_num = 32
    pool = Pool(pool_num)
    type = args.type
    if type == 'parse':
        files = glob.glob(input_path + '*.java')
        pool.map(partial(joern_parse, outdir=output_path), files)
    elif type == 'export':
        bins = glob.glob(input_path + '*.bin')
        pool.map(partial(joern_export, outdir=output_path), bins)
    else:
        print('Type error!')

if __name__ == '__main__':
    main()
