# Keybor: Fine-grained Code Clone Detection by Keywords-based Connection of Program Dependency Graph
Code clone detection is intended to identify functionally similar code fragments, which is of growing importance in the field of software engineering. There have been many proposed methods for detecting code clones, among which graph-based methods can handle semantic code clones. However, they all only consider the feature extraction of a single sample and ignore the semantic connection between different samples, resulting in the detection effect is still unsatisfactory. Meanwhile, most of the methods can only give whether they are clones or not, but cannot report which lines of code are more similar. 

In this paper, we propose a novel PDG-based semantic clone detection method namely Keybor which can give a fine-grained analysis of clone pairs to locate specific cloned lines of code. The highlight of the approach is to consider keywords as a bridge to connect PDG nodes of the target program to retain more semantic information about the functional code. To examine the effectiveness of Keybor, we assess it on a widely used BigCloneBench dataset. Experimental results indicate that Keybor is superior to 11 advanced code clone detection tools (i.e.,
CCAligner, SourcererCC, Siamese, NIL, NiCad, LVMapper, CCFinder, CloneWorks, Oreo, Deckard, and CCGraph).

# Design of Keybor
Keybor is divided into four phases: PDG Generation, PDG Mergence, Feature Extraction, and Verifying.
1. PDG Generation: 
  This phase aims to produce the corresponding PDG of the method.
  Therefore, the input of this phase is the methods and the output is the corresponding PDGs.

2. PDG Mergence: 
  This phase aims to merge two PDGs into one graph by adding keyword nodes.
  The input of this phase is two PDGs and the output is the merged PDG.
  
3. Feature Extraction:
  This phase aims to extract the feature of each node with code and structure information.
  The input of this phase is the merged PDG and the output is the vectors corresponding to each node in the merged PDG.

4. Verifying: 
  This phase aims to calculate the similarity score of extracted feature vectors to determine if code pairs are semantically clones. 
  The input of this phase is the vectors of the merged PDG and the output is the determination of clones or not.

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
 python 3_PdgMergel.py -p ../pair_csv/  -i ../pdg/ -o ../images

```

## Step4: Feature Extraction
Transforming PairPDG into feature vectors


