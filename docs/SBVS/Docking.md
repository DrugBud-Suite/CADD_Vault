# Molecular Docking

## Classical

- [**AutoDock Vina**](https://autodock-vina.readthedocs.io/en/latest/index.html)
  - [RDPSO_Vina](https://github.com/li-jin-xing/RDPSOVina): A fast docking tool utilizing random drift particle swarm optimization based on the AutoDock Vina and PSOVina framework.
  - [VinaXB (halogen-bonding)](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-016-0139-1): Introduces a halogen bonding scoring function (XBSF) in AutoDock Vina, termed AutoDock VinaXB, to improve docking accuracy with halogenated ligands.
  - [QVINA](https://github.com/QVina/qvina): QuickVina 2 aims to accurately speed up AutoDock Vina, providing up to 20.49-fold acceleration with high correlation in binding energy prediction.
  - [SMINA](https://sourceforge.net/projects/smina/): A fork of AutoDock Vina that supports scoring function development and high-performance energy minimization, maintained by the University of Pittsburgh.
  - [VinaCarb](https://pubs.acs.org/doi/10.1021/acs.jctc.5b00834): The content for VinaCarb was not available from the URL provided.
  - [FWAVina](https://www.sciencedirect.com/science/article/pii/S1476927120306381): The content for FWAVina was not accessible due to restrictions or an error from the URL provided.
  - [VinaGPU2.0](https://pubs.acs.org/doi/10.1021/acs.jcim.2c01504) and [AutoDockGPU](https://pubs.acs.org/doi/10.1021/acs.jctc.0c01006): The content for VinaGPU2.0 and AutoDockGPU was not available from the URLs provided.
  - [labodock](https://github.com/RyanZR/labodock): LABODOCK offers a collection of Jupyter Notebooks for molecular docking on Google Colab with minimal coding, streamlining pre- and post-docking processes.
  - [Uni-Dock](https://github.com/dptech-corp/Uni-Dock): Uni-Dock is a GPU-accelerated molecular docking program that supports various scoring functions and achieves significant speed-up compared with AutoDock Vina on a single CPU core.
- **PLANTS**
  - [parallel-PLANTS](https://github.com/discoverdata/parallel-PLANTS): Offers a method for parallel molecular docking using the PLANTS software, aimed at academic use.
- [PANTHER](https://www.medchem.fi/panther/): A tool designed for effective virtual screening, considering protein structure flexibility and physico-chemical properties, and available under a GPL license.
- [GeauxDock](https://www.brylinski.org/geauxdock): An ultra-fast automated docking program from LSU, predicting how small ligands bind to macromolecules using a novel hybrid force field and a Monte Carlo protocol.
- [GLOW-IVES](https://github.com/drorlab/GLOW_IVES): Provides Python implementation of GLOW (auGmented sampLing with softened vdW potential) and IVES (Iterative Ensemble Sampling) protocols for pose sampling, along with new cross-docking datasets.
- [HESS](<http://https>: //github.com/Entroforce/Hess)
- [JAMDA](https://doi.org/10.1021/acs.jcim.3c01573)
- 

## Flexible Docking

- **Residue conformation sampling**
  - [GNINA](https://github.com/gnina/gnina): GNINA is a molecular docking program that incorporates scoring and optimization of ligands using convolutional neural networks, aiming to combine the versatility of smina and AutoDock Vina with the predictive power of deep learning.
  - [Probis-Dock](http://insilab.org/probisdock/): ProBiS-Dock is a flexible docking algorithm treating both small molecules and proteins as fully flexible entities, complemented by a new scoring function, ProBiS-Score, for rapid docking and validated against standard benchmarks.
  - [tiny_IFD](https://github.com/darrenjhsu/tiny_IFD): Offers lightweight induced fit docking capabilities.
  - [ADFR](https://ccsb.scripps.edu/adfr/): AutoDockFR is a protein-ligand docking program supporting selective receptor flexibility and covalent docking, part of the ADFR suite for streamlined docking procedures.
  - [DSDPFlex](https://chemrxiv.org/engage/chemrxiv/article-details/6572d98429a13c4d47f6b4c6)
  - [PackDock](https://github.com/Zhang-Runze/PackDock): Describes PackDock as a diffusion-based side chain packing model for flexible protein-ligand docking, indicating code will be available following the publication of their paper.
  - [iDock](https://github.com/gloglita/idock): iDock is a multithreaded virtual screening tool for flexible ligand docking in computational drug discovery, inspired by AutoDock Vina and hosted on GitHub under Apache License 2.0.
- **Loop Conformation sampling**
  - [DynamicBind](https://github.com/luwei0917/DynamicBind): DynamicBind recovers ligand-specific conformations from unbound protein structures (e.g. AF2-predicted structures), promoting efficient transitions between different equilibrium states.

## Consensus

- [Exponential Consensus Ranking](https://www.nature.com/articles/s41598-019-41594-3#Sec8)
- [DockingPie](https://github.com/paiardin/DockingPie): DockingPie is a PyMOL plugin that facilitates consensus docking and scoring analyses, integrating four docking programs (Smina, Autodock Vina, RxDock, and ADFR) to offer a versatile platform for molecular and consensus docking.
- [dockECR](https://doi.org/10.1016/j.jmgm.2021.108023)
- [VoteDock](https://doi.org/10.1002/jcc.21642)

## ML-based

- [PointVS](https://github.com/jscant/PointVS): SE(3)-equivariant point cloud networks designed for virtual screening, enabling E(3)-invariant predictions of binding pose and affinity using networks based on the EGNN graph neural network layer.
- [EViS](https://github.com/JingHuangLab/EViS): EViS is an enhanced virtual screening method integrating ligand docking, protein pocket template searching, and ligand template shape similarity calculations, utilizing a novel PL-score for evaluation.
- [AQDNet](https://github.com/koji11235/AQDnet): Implements a Deep Neural Network for Protein-Ligand Docking Simulation, focusing on identifying correct binding poses through convolutional neural network approaches.
- [vScreenML](https://github.com/karanicolaslab/vScreenML): A machine learning classifier designed for virtual screening, allowing for the rescoring of hits to eliminate false positives, based on the Dataset of Congruent Inhibitors and Decoys (D-COID).
- [TopoFormer](https://github.com/WeilabMSU/TopoFormer): A topological transformer for protein-ligand complex interaction prediction, integrating multiscale topology techniques with a structure-to-sequence transformer model.
- [GNINA](https://github.com/gnina/gnina): GNINA is a molecular docking program that incorporates scoring and optimization of ligands using convolutional neural networks, aiming to combine the versatility of smina and AutoDock Vina with the predictive power of deep learning.
  - [gnina-torch](https://github.com/RMeli/gnina-torch/tree/0.0.2?tab=readme-ov-file): A PyTorch implementation of the GNINA molecular docking scoring function, designed for enhanced performance and adaptability.
- [DiffDock](https://github.com/gcorso/DiffDock): A state-of-the-art method for molecular docking, incorporating diffusion steps and a significant improvement in performance and generalization capacity.
  - [DiffDock-Pocket](https://anonymous.4open.science/r/DiffDock-Pocket-AQ32/README.md) is a binding-pocket specific molecular docking program that uses diffusion to sample ligand and sidechain poses.
- [ESF - scalar fields](https://github.com/bjing2016/scalar-fields): Implements Equivariant Scalar Fields for Molecular Docking with Fast Fourier Transforms, a machine learning-based ligand pose scoring function for rapid optimization.
- [SurfDock](https://github.com/CAODH/SurfDock): A Surface-Informed Diffusion Generative Model for reliable and accurate protein-ligand complex prediction, integrating generative model techniques for enhanced docking predictions.
- [GAABind](https://github.com/Mercuryhs/GAABind/blob/main/README.MD): GAABind is a Geometry-Aware Attention-Based Network for accurate protein-ligand binding pose and binding affinity prediction, featuring a comprehensive environment setup and dataset processing guide.
- [TankBind](https://github.com/luwei0917/TankBind): Trigonometry-Aware Neural NetworKs for Drug-Protein Binding Structure Prediction
- [Uni-Mol](https://github.com/dptech-corp/Uni-Mol): A Universal 3D Molecular Representation Learning Framework
- [PLANTAIN](https://github.com/molecularmodelinglab/plantain): Predicting LigANd pose wiTh an AI scoring functioN
- [KarmaDock](https://github.com/schrojunzhang/KarmaDock/blob/main/README.md) : a deep learning paradigm for ultra-large library docking with fast speed and high accuracy
- [SurfDock](https://github.com/CAODH/SurfDock): Surface-Informed Diffusion Generative Model for Reliable and Accurate Protein-ligand Complex Prediction
- [NeuralPlexer](https://github.com/zrqiao/NeuralPLexer): deep generative model to jointly predict protein-ligand complex 3D structures and beyond.

## Water

- [WatVina](https://github.com/biocheming/watvina): Watvina facilitates drug design with support for explicit or implicit waters, pharmacophore, or position-constrained docking, and external torsion parameters, enhancing the Autodock Vina engine.

## Pose Optimisation

- [DeepRMSD-Vina](https://github.com/zchwang/DeepRMSD-Vina_Optimization): DeepRMSD+Vina is a computational framework integrating ligand binding pose optimization and screening, utilizing deep learning alongside the classical Vina scoring function.

## Allosteric sites

- [FASTDock](https://github.com/BrooksResearchGroup-UM/FASTDock): FASTDock is a pipeline for allosteric drug discovery, offering scripts and a Jupyter notebook for efficiently generating and analyzing docking grids, clusters, and fingerprint screenings.

## Protein Docking

- [EquiDock](https://github.com/octavian-ganea/equidock_public): EquiDock employs geometric deep learning for fast and accurate rigid 3D protein-protein docking, focusing on efficiency and accessibility with comprehensive preprocessing and training guidelines.
- [LightDock](https://github.com/lightdock): The open-source macromolecular docking framework written in Python

## RNA docking

- Reviews
  - [Zhou et al.](https://wires.onlinelibrary.wiley.com/doi/pdf/10.1002/wcms.1571)

## Blind Docking

- [CBDock2](https://cadd.labshare.cn/cb-dock2/php/index.php): CBDock2 is an improved protein-ligand blind docking tool integrating cavity detection, docking, and homologous template fitting to suggest novel therapeutic targets for biological and pharmaceutical studies.
- [CoBDock](https://github.com/DavidMcDonald1993/cobdock): CoBDock is a reference implementation of the COBDock algorithm, detailing steps for setup and execution on Linux, with a focus on integrating various molecular docking and pocket identification algorithms.

## All-Atom-DL methods

- [RoseTTAFold-AllAtom](https://www.biorxiv.org/content/10.1101/2023.10.09.561603v1): RoseTTAFold All-Atom (RFAA) is a deep network capable of modeling full biological assemblies containing proteins, nucleic acids, small molecules, metals, and covalent modifications with high accuracy.
- [NeuralPlexer](https://github.com/zrqiao/NeuralPLexer): a deep generative model to jointly predict protein-ligand complex 3D structures and beyond.

## MD-based

- [ColDock](https://pubs.acs.org/doi/10.1021/acs.jpcb.8b02756)

## MetalloProteins

- [MetalDock](https://pubs.acs.org/doi/10.1021/acs.jcim.3c01582)

## Covalent Docking

- [Covalent Dock](https://onlinelibrary.wiley.com/doi/10.1002/jcc.23136)

## HPC enabled

- [VinaLC](https://onlinelibrary.wiley.com/doi/10.1002/jcc.23214)
- [VinaMPI](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.23367)
- [VinaSC](https://ieeexplore.ieee.org/abstract/document/7822624?casa_token=8WbdFXnx06cAAAAA:K-0Z1J07YAV_XKJU5-Ycj5LVAMoHoqheAiWABCAJ769TQnm22YsBczrFdWmJFNpFlrXPlNPlzfv3GA)
- [POAP](https://www.sciencedirect.com/science/article/pii/S1476927117305753)

## Multi-Ligand

- [HARMONICFlow](https://github.com/HannesStark/FlowSite)

## Quantum

- [Zhang et al.](https://doi.org/10.1021/acs.jctc.3c00943)

<https://github.com/AngelRuizMoreno/Jupyter_Dock>
