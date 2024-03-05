### Homology Modelling
- [SWISS-MODEL](http://swissmodel.expasy.org/): an automated protein structure homology-modelling server, accessible via the ExPASy web server
- **[Phyre2](http://www.sbg.bio.ic.ac.uk/phyre2/html/page.cgi?id=index)**: Phyre2 is a tool for predicting and analyzing protein structure, function, and mutations. The server provides an expert mode for registered users and integrates models directly from the AlphaFold Protein Structure Database for one-to-one threading.
### Structure Prediction
- **[AlphaFold2](https://alphafold.com/)**: The specific details about AlphaFold2 could not be directly retrieved, but AlphaFold2 by DeepMind represents a significant advancement in protein structure prediction, using deep learning to accurately predict protein structures.
	- **[ColabFold](https://github.com/sokrypton/ColabFold)**: ColabFold makes protein folding accessible to all by leveraging AlphaFold2's capabilities in an accessible manner through Google Colab, providing an efficient and user-friendly way to perform protein folding predictions.
- **[RoseTTAFold](https://github.com/RosettaCommons/RoseTTAFold)**: This package contains deep learning models and scripts for RoseTTAFold, an accurate method for protein structure prediction that includes a 3-track network. It's capable of modeling multi-chain complexes and provides an option for large scale sampling.
- **[ESMFold](https://github.com/facebookresearch/esm)**: Evolutionary Scale Modeling (ESM) offers pretrained language models for proteins, including ESM-2 and ESMFold for structure prediction and variant effect prediction, supporting a wide range of protein research applications.
- **[McGuffin Group Web Servers](https://www.reading.ac.uk/bioinf/index.html)**: This link points to the home page of the McGuffin Group Web Servers at the University of Reading, which provides various bioinformatics tools, although specific details about the tools were not provided.
- **[Robetta](https://robetta.bakerlab.org/)**: Robetta offers structure prediction using deep learning methods like RoseTTAFold and TrRosetta. It allows for custom sequence alignments, constraints, local fragments for homology modeling, and can model multi-chain complexes.
- Trans-membrane
	- **[PredMP](http://www.predmp.com/)**: The website's specific content was not retrievable due to request issues, but PredMP is designed for predicting membrane protein types and orientations.
	- **[MemBrain](http://www.csbio.sjtu.edu.cn/bioinf/MemBrain/)**: The site provides resources related to membrane protein prediction but specific details about the MemBrain tool were not provided.
	- **[RosettaGPCR](https://github.com/benderb1/rosettagpcr)**: This repository contains methods for generating models of G protein-coupled receptors (GPCRs) using Rosetta, including a database of templates updated through June 2020.
	- **[membraneFold](https://ku.biolib.com/MembraneFold/)**: This resource is intended for predicting membrane protein structures, but specific details were not provided.
- Quaternary structure
	- **[AlphaFold-multimer](https://github.com/deepmind/alphafold)**: The specific details about AlphaFold-multimer could not be directly retrieved, but it extends AlphaFold2's capabilities to predict structures of protein complexes (multimers).
	- **[DeepComplex](http://tulip.rnet.missouri.edu/deepcomplex/web_index.html)**: This document has moved, and direct content was not provided in the data fetched, but DeepComplex is aimed at predicting quaternary protein structures.

### Structure Prediction with Ligand
- **[Umol](https://github.com/patrickbryant1/Umol)**: Umol is designed for protein-ligand structure prediction, representing the protein with a multiple sequence alignment and the ligand as a SMILES string, with versions utilizing protein pocket information recommended.
### Conformation Ensemble Generation
- **[AF2-Rave](https://github.com/tiwarylab/alphafold2rave)**: AF2-Rave combines AlphaFold2 with enhanced sampling to predict a range of conformations for a given protein sequence, aiming to generate Boltzmann-ranked conformations
- **[SubPEx](http://durrantlab.com/subpex/)**: This document has moved, and specific details were not directly provided in the fetched data.
- **[AlphaFlow](https://github.com/bjing2016/alphaflow)**: AlphaFlow is a modified version of AlphaFold, fine-tuned with a flow matching objective, capable of generating protein conformational ensembles.
- **[Str2Str](https://github.com/lujiarui/Str2Str)**: Str2Str is a score-based framework for zero-shot protein conformation sampling, drawing inspiration from traditional methods to sample conformations guided by a neural score network trained on the PDB database.
- **[AF-cluster](https://github.com/HWaymentSteele/AF_Cluster)**: This method predicts multiple protein conformations using sequence clustering and AlphaFold2, aiming to capture the diversity of protein structures.
- PepFlow
- CFold
### Binding Site Prediction
- - **[AF2BIND](https://colab.research.google.com/github/sokrypton/af2bind/blob/main/af2bind.ipynb)**: AF2BIND utilizes AlphaFold2 for predicting protein-ligand binding sites, though specific content was not directly retrievable.
- **[DogSiteScorer](https://proteins.plus/)**: This service provides tools for drug discovery, including the DogSiteScorer for predicting and scoring protein-ligand binding sites, though specific details were minimal.
- **[FPocketWeb](https://durrantlab.pitt.edu/fpocketweb-download/)**: FpocketWeb is a browser app for identifying pockets on protein surfaces where small-molecule ligands might bind, running calculations locally on the user's computer.
- **[P2rank](https://github.com/rdk/p2rank)**: P2Rank is a machine learning-based tool for predicting ligand-binding sites from protein structures, capable of handling various structure formats including AlphaFold models.
- **[PrankWeb](https://prankweb.cz/)**: Builds upon P2Rank for the prediction of ligand binding sites from protein structure, offered as a service by ELIXIR.
- **[GrASP](https://github.com/tiwarylab/GrASP/tree/main)**: GrASP (Graph Attention Site Prediction) identifies druggable binding sites using graph neural networks with attention.
- **[CavityPlus](https://github.com/PKUMDL2017/CavityPlus?tab=readme-ov-file)**: A web server for protein cavity detection with pharmacophore modeling, allosteric site identification, and covalent ligand binding ability prediction.
- Allosteric Site Prediction
	- **[PASSer](https://passer.smu.edu/)**: Designed for accurate allosteric site prediction, PASSer offers three machine learning models for quick and extensive allosteric analysis.
    - **[AlloReverse](http://www.allostery.net/AlloReverse/)**: AlloReverse predicts multi-scale allosteric regulation information based on reversed allosteric communication theory, aiding in drug design and biological mechanism understanding.
- Fragment Site Prediction
	- [**FTMap**](https://ftmap.bu.edu/show_example.php?example=ace): FTMap maps unbound protein surfaces to identify druggable hot spots where small molecules may bind.
- Metal-binding site
	- **[PinMyMetal](https://github.com/hhz-lab/PinMyMetal.git)**: Specific details about PinMyMetal, presumably a tool for predicting metal-binding sites in proteins, were not provided in the data fetched.
- MD
	- **[POVME2](https://durrantlab.pitt.edu/povme2/)**: POVME2 identifies druggable protein pockets and their unique conformations within molecular dynamics simulations, facilitating the discovery of novel pharmacologically active molecules.
### Partial Charge Calculation
- [alphaCharges](https://alphacharges.ncbr.muni.cz/)
### Datasets
- Data Mining
	- [PDBminer](https://github.com/ELELAB/PDBminer)
### Structure Refinement
- [DeepTracer-refine](https://www.semanticscholar.org/paper/Protein-Structure-Refinement-via-DeepTracer-and-Chen-Zia/8eb8e41af63e2b406a253347d1dfcd2185ffba16)
### Sequence Alignment
- Trans-membrane
	- **[tmAligner](http://skuastk.org/tmaligner/)**: tmAligner is an online alignment tool for transmembrane proteins, allowing users to paste or upload sequences in FASTA format for alignment.

### Protein Representation
- **[GraphSite](https://github.com/shiwentao00/Graphsite)**: GraphSite is a Python software that generates graph representations of protein binding sites, where each atom becomes a node, and edges represent close proximity, useful for applications based on graph neural networks.
### General
- **[pdb-tools](https://github.com/haddocking/pdb-tools)**: pdb-tools offer a collection of scripts that serve as a Swiss army knife for manipulating and editing PDB files without any external dependencies, designed to be simple to use by piping one script's output into another.
- PDBFixer
- 