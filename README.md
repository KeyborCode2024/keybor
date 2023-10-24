# Keybor: Fine-grained Code Clone Detection by Keywords-based Connection of Program Dependency Graph

# Source Code  
## Step 1: File Preprocess
```
python FileAddClass.py -i ../dataset/id2sourcecode -o ../java
```

## Step 2: Generate pdgs with the help of joern
Prepare the environment refering to: [joern](https://github.com/joernio/joern) you can try the version between 1.1.995 to 1.1.1125
```
# generate .bin files
python JoernGraph.py -i ../java -o ../bin -t parse

# generate pdgs (.dot files)
python JoernGraph.py -i ../bin -o ../dot -t export

# change pdgs struct
python PdgGeneration.py -d ../dot -f ../java -o ../pdg
```

## Step3: PDG Mergence
Combining the two PDGs of a clone pair into a single graph PairPDG
```
 python 3_PdgMerge.py -p ../pair_csv/  -i ../pdg/ -o ../images
```

#### Step 4: Train a sent2vec model
Refer to [sent2vec](https://github.com/epfml/sent2vec#train-a-new-sent2vec-model)
```
# download sent2vec
git clone https://github.com/epfml/sent2vec.git
cd sent2vec
# compile
make
# build model
./fasttext sent2vec -input BCB.txt -output model -minCount 8 -dim 128 -epoch 9 -lr 0.2 -wordNgrams 2 -loss ns -neg 10 -thread 20 -t 0.000005 -dropoutK 4 -minCountLabel 20 -bucket 4000000
```

## Step5: Feature Extraction(Sent2vec)
Transform code information in PairPDG nodes into feature vectors
```
python FeatureExtraction_sent2vec.py -i ../images -o ../emb/Sent2vec
```

## Step6: Feature Extraction(Struc2vec)
Transform struct information in PairPDG nodes into feature vectors
```
cd Struc2vec
python FeatureExtraction_struc2vec.py -i ../../images -o ../../emb/Struc2vec
```

## Step7: Verifying
Calculate the similarity score of extracted feature vectors to determine if code pairs are semantically clones.
```
python cos.py -i ../emb -o ../cos -m Struc2vec
python Classification.py -i ../cos -o ../result -m Struc2vec
```


