# Keybor: Fine-grained Code Clone Detection by Keywords-based Connection of Program Dependency Graph
Keybor is a PDG-based approach for complex semantic clone detection.
To preserve more semantic information about method codes, we treat keywords as bridges to connect PDG nodes of target programs to identify codes with similar semantics in different code blocks. 
Meanwhile, we are capable of performing line-level similarity matching to obtain fine-grained clone detection results.

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

The source code and dataset of Tritor will be published here after the paper is accepted.

