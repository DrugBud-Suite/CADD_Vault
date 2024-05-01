# Molecule De Novo Generation

## Models

- [REINVENT 4](https://github.com/MolecularAI/REINVENT4): A molecular design tool for various design tasks like de novo design, scaffold hopping, and molecule optimization, using a reinforcement learning algorithm.
  - [REINVENT-HITL](https://github.com/MolecularAI/reinvent-hitl): Focuses on human-in-the-loop assisted de novo molecular design, leveraging reinforcement learning for optimizing molecules based on human feedback.
- [GRAPHINVENT](https://github.com/MolecularAI/GraphINVENT): A platform for graph-based molecular generation using graph neural networks, emphasizing probabilistic generation one bond at a time.
  - [RL-GraphInvent](https://github.com/olsson-group/RL-GraphINVENT): An extension using reinforcement learning for targeted molecular generation.
- [TransformerVAE](https://github.com/mizuno-group/TransformerVAE): A VAE model with Transformer backbone for molecule generation.
- [SiMGen](https://zndraw.icp.uni-stuttgart.de/): The provided link was unresponsive for extracting detailed information.
- [FREED](https://github.com/AITRICS/FREED): Utilizes explorative experience replay in a generative reinforcement learning setup for drug design.
- [GenUI](https://github.com/martin-sicho/genui): Offers API and GUI for molecular generators, QSAR modelling, and chemical space visualization.
- [mol-Zero-GAN](https://github.com/cucpbioinfo/Mol-Zero-GAN): Aims at optimizing pretrained generative models for drug candidate generation using Bayesian optimization.
- [LigDream](https://github.com/playmolecule/ligdream/tree/master): Generates novel molecules from a reference shape but is no longer actively supported.
- [COATI](https://github.com/terraytherapeutics/COATI/tree/main): A pre-trained, multi-modal encoder-decoder model designed for navigating and representing chemical space.
- [ReLeaSE](https://github.com/isayev/ReLeaSE): Utilizes deep reinforcement learning for de novo drug design.
- [LSTM_Chem](https://github.com/topazape/LSTM_Chem): Implements generative recurrent networks for drug design.
- [DrugEx](https://github.com/CDDLeiden/DrugEx): Library for de novo drug design using RNNs, Transformers within a multi-objective reinforcement learning framework
- [Pytorch_VAE](https://github.com/Ishan-Kumar2/Molecular_VAE_Pytorch): This repository provides a PyTorch implementation of the paper "Automatic Chemical Design Using a Data-Driven Continuous Representation of Molecules" by Gómez-Bombarelli, et al., focusing on a variational autoencoder for molecular design using the ChEMBL dataset.
- [DST](https://github.com/futianfan/DST): Differentiable Scaffolding Tree (DST) enables gradient-based optimization on a chemical graph for molecule optimization, providing a novel approach for de novo molecule design.
- [MolDrug](https://github.com/ale94mleon/MolDrug): MolDrug is a Python package for drug-oriented optimization in the chemical space, using a Genetic Algorithm as a search engine and CReM library as the chemical structure generator.
- [Molecule-RNN](https://github.com/shiwentao00/Molecule-RNN): Molecule-RNN is a recurrent neural network designed to generate drug-like molecules for drug discovery, learning the distribution of a training dataset to sample similar molecules.
- [MolGrad](https://github.com/pwolle/MolGrad): MolGrad is a Jugend forscht project that introduces score-based generative modeling for molecules, aiming to aid the drug development process by generating and optimizing new, high-quality molecules.
- [moleculegen-ml](https://github.com/sanjaradylov/moleculegen-ml): Moleculegen-ML is a Python package for de novo drug design based on generative language modeling, featuring tools for molecular data processing and SMILES-based language modeling.
- [MDM](https://github.com/tencent-ailab/MDM): MDM is a model designed for molecular dynamics simulations, with a focus on generating data and training conditioned on various molecular properties.
- [MoFlowGAN](https://github.com/thisisntnathan/MoFlowGAN): MoFlowGAN is a normalizing flow for molecular graphs that is heuristically biased towards easily synthesized, drug-like molecules, aiming to generate high-quality molecular graphs through a process similar to GANs.
- [JODO](https://github.com/graph-0/jodo): JODO focuses on learning joint 2D and 3D diffusion models for complete molecule generation, representing molecules as both 3D point clouds and 2D bonding graphs to enhance molecular design.
- [ScaffoldGVAE](https://github.com/ecust-hc/ScaffoldGVAE): ScaffoldGVAE is a variational autoencoder based on multi-view graph neural networks for scaffold generation and scaffold hopping of drug molecules, aiming to enhance molecular design by focusing on the scaffold components.
- [MolFilterGAN](https://github.com/MolFilterGAN/MolFilterGAN): MolFilterGAN is a progressively augmented generative adversarial network for triaging AI-designed molecules, focusing on improving the quality of generated molecules by filtering out undesired candidates early in the generation process.
- [HierDiff](https://github.com/qiangbo1222/HierDiff): HierDiff is a hierarchical diffusion model for 3D molecule generation, presenting a coarse-to-fine approach that aims to efficiently and effectively generate drug-like molecules in 3D space.
- [SpotGAN](https://github.com/naruto7283/SpotGAN): SpotGAN, a PyTorch implementation of a reverse-transformer GAN, generates scaffold-constrained molecules with property optimization, demonstrating advanced capabilities in generating molecules that adhere to specific structural constraints while optimizing for desired properties.
- [QADD](https://github.com/yifang000/QADD): QADD is a novel de novo multi-objective quality assessment-based drug design approach that integrates an iterative refinement framework with a graph-based molecular quality assessment model to generate molecules with multiple desired properties.
- [MolCode](https://github.com/zaixizhang/MolCode): MolCode introduces a roto-translation equivariant generative framework for co-designing molecular 2D graph structures and 3D geometries, aiming to efficiently learn the structure-property relationship for molecule generation.
- [RRCGAN](https://github.com/linresearchgroup/RRCGAN_Molecules): RRCGAN combines a generative adversarial network with a regressor to generate small molecules with targeted properties, emphasizing the use of deep learning models to design molecules with specific desired attributes.
- [E3_diffusion](https://github.com/ehoogeboom/e3_diffusion_for_molecules): This project develops equivariant diffusion models for molecule generation in 3D, providing a novel approach to generating molecular structures by leveraging the properties of diffusion models within a 3D space.
- [NYAN (NotYetAnotherNightshade)](https://github.com/Chokyotager/NotYetAnotherNightshade): A graph variational encoder designed for embedding molecules into a continuous latent space for molecular property prediction and high-throughput virtual screening in drug discovery.
- [ChemTSv2](https://github.com/molecule-generator-collection/ChemTSv2): An extended version of ChemTS, focusing on functional molecular design using de novo molecule generators, incorporating improvements for LogP maximization tasks and other molecular design objectives.
- [MiCaM (De Novo Molecular Generation via Connection-aware Motif Mining)](https://github.com/miralab-ustc/ai4sci-micam): Introduces a novel approach for de novo molecular generation by mining connection-aware motifs from molecular structures, aiming to enhance molecule generation processes.
- [GENTRL (Generative Tensorial Reinforcement Learning)](https://github.com/insilicomedicine/GENTRL): A variational autoencoder with a rich prior distribution of the latent space, trained to find molecules with high reward, emphasizing the relations between molecular structures and their properties.
- [Sc2Mol](https://github.com/zhiruiliao/Sc2Mol): A scaffold-based two-step molecule generator that combines variational autoencoders with transformers to generate molecules, supporting batch random generation for efficiency.
- [SQUID (Equivariant Shape-Conditioned Generation of 3D Molecules for Ligand-Based Drug Design)](https://github.com/keiradams/squid): Demonstrates the generation of chemically diverse molecules for arbitrary molecular shapes, aiming at ligand-based drug design through shape-conditioned molecular generation.
- [HyFactor (Hydrogen-count Labelled Graph-based Defactorization Autoencoder)](https://github.com/Laboratoire-de-Chemoinformatique/HyFactor): An open-source architecture for structure generation using graph-based approaches, focusing on a new molecular graph type that considers hydrogen counts for enhanced molecular representation and generation.
- [GAN-Drug-Generator](https://github.com/larngroup/GAN-Drug-Generator): Proposes a framework based on Feedback Generative Adversarial Network (GAN) for the generation and optimization of drug-like molecules, including a multiobjective optimization selection technique.
- [FASMIFRA](https://github.com/UnixJunkie/FASMIFRA): Generate molecules fast from a molecular training set while also doing training-set distribution matching
- [hgraph2graph](https://github.com/wengong-jin/hgraph2graph): Hierarchical Generation of Molecular Graphs using Structural Motifs
- [MolDQN](https://github.com/google-research/google-research/tree/master/mol_dqn): Optimization of Molecules via Deep Reinforcement Learning
- [ChemTSv2](https://github.com/molecule-generator-collection/ChemTSv2): Functional molecular design using de novo molecule generator
- [Mothra](https://github.com/sekijima-lab/Mothra)
- [FlowMol](https://github.com/dunni3/FlowMol)
- [DRAGONFLY](https://github.com/ETHmodlab/dragonfly_gen)
- [FraHMT](https://github.com/llldddmmm/Code-FraHMT)

- **Fragment-based**
  - [CRem](https://github.com/DrrDom/crem): open-source Python framework to generate chemical structures using a fragment-based approach

- **Pharmacophore**
  - [PGMG](https://github.com/CSUBioGroup/PGMG): A Pharmacophore-Guided Deep Learning Approach for Bioactive Molecule Generation, offering a strategy to generate molecules with structural diversity based on a pharmacophore hypothesis.
    - [Webserver](https://www.csuligroup.com/PGMG/)
  - [DEVELOP](https://github.com/oxpig/DEVELOP): Implements Deep Generative Design with 3D Pharmacophoric Constraints for molecular design, focusing on linker design and scaffold elaboration using a combination of variational autoencoders and 3D pharmacophore modeling.
  - [TransPharmer](https://www.semanticscholar.org/reader/fac3d72a3e73f65e1c950104e010edd136cb4201): The provided link was unresponsive for extracting detailed information; typically, it would describe a tool or model for pharmacophore-based molecular design or analysis.

- **Linker generation**
  - [DiffLinker](https://github.com/igashov/DiffLinker): An Equivariant 3D-conditional Diffusion Model for Molecular Linker Design that places missing atoms between disconnected fragments in 3D, designing molecules that incorporate all initial fragments with potential applications in linker generation for drug discovery.
  - [DeLinker](https://github.com/oxpig/DeLinker): Deep Generative Models for 3D Linker Design
  - [DRLinker](https://github.com/biomed-AI/DRlinker): Deep Reinforcement Learning for optimization in fragment linking Design
  - [GRELinker](https://github.com/howzh728/GRELinker): A Graph-based Generative Model for Molecular Linker Design with Reinforcement and Curriculum Learning

- **Using Large Chemical Spaces**
  - [SyntheMol](https://github.com/swansonk14/SyntheMol): SyntheMol is a generative AI method for designing structurally novel and diverse drug candidates with predicted bioactivity that are easy to synthesize.