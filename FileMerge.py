import os
import glob
file_txt = '../sent2vec/BCB.txt'
dir_path = '../dataset/id2sourcecode/*.java'
files = glob.glob(dir_path)
fw = open(file_txt, "w+", encoding='utf-8')
for file in files:
    # fw.write(file.split('/')[-1])
    with open(file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            fw.write(line)
    fw.write('\n')
fw.close()



