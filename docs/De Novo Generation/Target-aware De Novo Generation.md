# Target-Aware De Novo Generation

## Models

- **[Lingo3DMol](https://github.com/stonewiseAIDrugDesign/Lingo3DMol)**: A pocket-based 3D molecule generation method that combines language model capabilities with 3D coordinate generation and geometric deep learning.
- **[3D-Generative-SBDD](https://github.com/luost26/3D-Generative-SBDD)**: Focuses on structure-based drug design (SBDD) using a 3D generative model to sample molecules for specific protein pockets.
- **[GraphBP](https://github.com/divelab/GraphBP)**: Implements a method for generating 3D molecules targeting protein binding, presented at ICML 2022.
- **[FLAG](https://github.com/zaixizhang/FLAG)**: A Fragment-based Ligand Generation framework to generate 3D molecules with valid and realistic substructures fragment-by-fragment.
- **[DrugGPS](https://github.com/zaixizhang/DrugGPS_ICML23)**: Focuses on learning subpocket prototypes for generalizable structure-based drug design, introduced at ICML 2023.
- **[liGAN](https://github.com/mattragoza/liGAN)**: A project for structure-based drug discovery using deep generative models of atomic density grids.
- **[RELATION](https://github.com/micahwang/RELATION)**: A software for DL-based de novo drug design, focusing on generating molecules based on target protein interactions.
- **[DESERT](https://github.com/longlongman/DESERT)**: Zero-shot 3D drug design by sketching and generating, as presented at NeurIPS 2022.
- **[Pocket2Mol](https://github.com/pengxingang/Pocket2Mol)**: Uses equivariant graph neural networks for efficient molecular sampling based on 3D protein pockets.
- **[RGA](https://github.com/futianfan/reinforced-genetic-algorithm)**: A reinforcement learning-based genetic algorithm for structure-based drug design, introduced at NeurIPS 2022.
- **[PCMol](https://github.com/CDDLeiden/PCMol)**: A multi-target model for de novo molecule generation, using AlphaFold protein embeddings for thousands of protein targets.
- **[KGDiff](https://github.com/CMACH508/KGDiff)**: A model for explainable target-aware molecule generation with knowledge guidance.
- **[DiffDec](https://github.com/biomed-AI/DiffDec/blob/master/README.md)**: A model that uses an end-to-end equivariant diffusion process for optimizing molecular structures through scaffold decoration conditioned on 3D protein pockets.
- **[SINGA](https://github.com/Isomorpfishm/SINGA)**: SINGA is a Molecular Sampling model with Protein-Ligand Interactions aware Generative Adversarial Network, focusing on generating molecules considering their interactions with proteins.
- **[Ligand_Generation](https://github.com/HySonLab/Ligand_Generation)**: This project focuses on target-aware variational autoencoders for ligand generation, employing multimodal protein representation learning for structure-based drug design.
- **[LS-MolGen](https://github.com/songleee/LS-MolGen)**: A ligand-and-structure dual-driven deep reinforcement learning method for target-specific molecular generation, integrating docking scores and bioactivity data for molecule optimization.
- **[cMolGPT](https://github.com/VV123/cMolGPT)**: cMolGPT, a Conditional Generative Pre-trained Transformer, aims for de novo molecular design by enforcing target specificity during the generation process, emphasizing the incorporation of target embeddings.
- **[BindDM](https://github.com/YangLing0818/BindDM)**: Binding-Adaptive Diffusion Models for Structure-Based Drug Design
- **[DeepICL](https://github.com/ACE-KAIST/DeepICL)**
- **[DeepTarget](https://github.com/ehoogeboom/e3_diffusion_for_molecules)**
- **[TargetDiff](https://github.com/guanjq/targetdiff)**: 3D Equivariant Diffusion for Target-Aware Molecule Generation and Affinity Prediction (standalone, 2024).
- **[DrugGEN](https://github.com/asarigun/DrugGEN)**
- **[PETrans](https://github.com/Chinafor/PETrans)**
- **[BindDM](https://github.com/YangLing0818/BindDM)**: BindDM extracts subcomplex from protein-ligand complex, and utilizes it to enhance the binding-adaptive 3D molecule generation in complex
- **[PocketFlow](https://github.com/Saoge123/PocketFlow)**: data-and-knowledge driven structure-based molecular generative model
- **[SECSE](https://github.com/KeenThera/SECSE)**
- **[SBMolGen](https://github.com/clinfo/SBMolGen)**: integrates a recurrent neural network, a Monte Carlo tree search, and docking simulations
- **[PMDM](https://github.com/Layne-Huang/PMDM/tree/main)**: dual diffusion model enables 3D binding bioactive molecule generation and lead optimization given target pockets
- **[DeepICL](https://github.com/ACE-KAIST/DeepICL)**: 3D molecular generative framework for interaction-guided drug design
- **[DEVELOP](https://github.com/oxpig/DEVELOP/tree/main)**
  - **[SCRdkit](https://github.com/oxpig/DEVELOP/blob/main/analysis/calc_SC_RDKit.py)**: assesses the 3D similarity between generated molecules and a reference molecule
- **[MolSnapper](https://github.com/oxpig/MolSnapper)**
- **[FragGen](https://github.com/HaotianZhangAI4Science/FragGen)**: Fragment wise 3D Structure-based Molecular Generation
- **[DRAGONFLY](https://github.com/ETHmodlab/dragonfly_gen)**
- **[HySonLab](https://github.com/HySonLab/Ligand_Generation)**
- **[PocketOptimizer 2.0](https://github.com/Hoecker-Lab/pocketoptimizer)**: Design of small molecule‐binding pockets in proteins (standalone)
- **[DiffSBDD](https://github.com/arneschneuing/DiffSBDD)**: Structure-based Drug Design with Equivariant Diffusion Models (standalone, 2024).
- **[PocketGen](https://github.com/zaixizhang/PocketGen)**: Generating Full-Atom Ligand-Binding Protein Pockets (standalone).
- **[ResGen](https://github.com/HaotianZhangAI4Science/ResGen)**: pocket-aware 3D molecular generation model based on parallel multiscale modelling (standalone).
- **[ChemSpaceAL](https://github.com/gregory-kyro/ChemSpaceAL)**: an Efficient Active Learning Methodology Applied to Protein-Specific Molecular Generation (generative chemistry) (standalone, 2024).
- **[AlphaDrug](https://github.com/CMACH508/AlphaDrug)**: protein target specific de novo molecular generation (generative chemistry) (standalone).

## Dual-target

  - **[Alx-Fuse](https://github.com/biomed-AI/AIxFuse)**

## Interaction fingerprint constrained

  - **[IFP-RNN](https://github.com/jeah-z/IFP-RNN)**: A molecule generative model used interaction fingerprint (docking pose) as constraints.
## PROTACs

- **[PROTACable](https://github.com/giaguaro/PROTACable/)**: Integrative Computational Pipeline of 3-D Modeling and Deep Learning To Automate the De Novo Design of PROTACs (standalone, published 2024).
