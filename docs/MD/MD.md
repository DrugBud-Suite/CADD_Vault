# Molecular Dynamics

## Free-Energy Perturbation

- **Planning**
  - [HiMap](https://github.com/MobleyLab/HiMap): High Information Mapper (HiMap), successor of the Lead Optimization Mapper (LOMAP), includes design generation based on statistical optimality for alchemical free energy calculations and optimization of free energy perturbation networks.
- **Classical**
  - [alchemlyb](https://github.com/alchemistry/alchemlyb) - Makes alchemical free energy calculations easier by leveraging the full power and flexibility of the PyData stack.
  - [OpenFE](https://github.com/OpenFreeEnergy/openfe): A Python package for executing alchemical free energy calculations
  - [gmx_MMPBSA](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA): gmx_MMPBSA is a new tool based on AMBER's MMPBSA.py aiming to perform end-state free energy calculations with GROMACS files
  - [Uni-GBSA](https://github.com/dptech-corp/Uni-GBSA): An Automatic Workflow to Perform MM/GB(PB)SA Calculations for Virtual Screening
  - [BAT](https://github.com/GHeinzelmann/BAT.py): Binding Affinity Tool (BAT.py) is a python tool for fully automated absolute binding free energy (ABFE) calculations using all-atom Molecular Dynamics (MD)
  - [FEgrow](https://github.com/cole-group/FEgrow): An interactive workflow for building user-defined congeneric series of ligands in protein binding pockets for input to free energy calculations.
  - [pAPRika](https://github.com/GilsonLabUCSD/pAPRika): pAPRika is a toolkit for setting up, running, and analyzing free energy molecular dynamics simulations.
  - [gufe](https://github.com/OpenFreeEnergy/gufe): GUFE is a toolkit for developers of software related to alchemical free energy calculations, containing data models and abstract base classes.
- **ML-enabled**
  - [ATM_with_NNPs](https://github.com/compsciencelab/ATM_benchmark/tree/main/ATM_With_NNPs): Enhancing Protein-Ligand Binding Affinity Predictions Using Neural Network Potentials
- **Tools**
  - [Kartograf](https://github.com/OpenFreeEnergy/kartograf): Kartograf is a package focusing on 3D geometry-based atom mappings, useful for generating hybrid topology systems in free energy calculations and other applications.
- **Benchmarks**
  - [Merck FEP Benchmark](https://github.com/MCompChem/fep-benchmark): Benchmark set for relative free energy calculations.
  - [OpenFF Benchmark](https://github.com/openforcefield/protein-ligand-benchmark): Protein-Ligand Benchmark Dataset for testing Parameters and Methods of Free Energy Calculations.
- **Guides**
  - [Best Practices for Alchemical Free Energy Simulations](https://github.com/alchemistry/alchemical-best-practices)

## Machine learning forcefields

- [Espaloma-0.3.0](https://github.com/choderalab/espaloma): Espaloma is an Extensible Surrogate Potential of Ab initio Learned and Optimized by Message-passing Algorithm, a framework for end-to-end differentiable construction of molecular mechanics force fields using graph neural networks.

## Molecular Dynamics Engines

- [Gromacs](http://www.gromacs.org/): GROMACS is a versatile package for performing molecular dynamics simulations, primarily designed for simulations of proteins, lipids, and nucleic acids.
- [OpenMM](http://openmm.org/): OpenMM is a high-performance toolkit for molecular simulation, offering extensive language bindings and a flexible platform for developing high-performance algorithms.
  - [openmmtools](https://github.com/choderalab/openmmtools) - A batteries-included toolkit for the GPU-accelerated OpenMM molecular simulation engine.
- [NAMD](https://www.ks.uiuc.edu/Research/namd/): NAMD is a parallel molecular dynamics code for high-performance simulation of large biomolecular systems, recognized for its scalability and efficiency.
- [SENPAI](https://github.com/SENPAI-Molecular-Dynamics/SENPAI): SENPAI is a molecular dynamics simulation software aimed at students and academia, designed to simulate molecular systems of educational and academic interest efficiently.
- [HTMD](https://github.com/Acellera/htmd) - High-Throughput Molecular Dynamics: Programming Environment for Molecular Discovery.
- [openff-toolkit](https://github.com/openforcefield/openff-toolkit) - The Open Forcefield Toolkit provides implementations of the SMIRNOFF format, parameterization engine, and other tools.
- [GaMD](https://github.com/MiaoLab20/gamd-openmm): Gaussian Accelerated Molecular Dynamics (GaMD) is a biomolecular enhanced sampling method that works by adding a harmonic boost potential to smoothen the system potential energy surface.

- **ML-enabled**
  - Reviews
    - [Medbi et al.](https://www.annualreviews.org/doi/pdf/10.1146/annurev-physchem-083122-125941)
  - [NeuralMD](https://www.semanticscholar.org/paper/A-Multi-Grained-Symmetric-Differential-Equation-for-Liu-Du/0215dd9f346534bf4c4247220501d7ab7d7715c6)
  - [torchmd](https://github.com/torchmd/torchmd) - End-To-End Molecular Dynamics (MD) Engine using PyTorch.
  - [MLCGMD](https://github.com/kyonofx/mlcgmd): Simulate Time-integrated Coarse-grained Molecular Dynamics with Multi-scale Graph Networks

## Libraries

- [MDTraj](https://github.com/simtk/mdtraj): MDTraj is a Python library for analyzing molecular dynamics trajectories, offering a wide range of functionalities for trajectory manipulation and analysis.
- [MDAnalysis](http://www.mdanalysis.org/) - Is an object-oriented library to analyze trajectories from molecular dynamics (MD) simulations in many popular formats.
- [MMTK](http://dirac.cnrs-orleans.fr/MMTK/) - The Molecular Modeling Toolkit is an Open Source program library for molecular simulation applications.
- [Packmol](http://m3g.iqm.unicamp.br/packmol/home.shtml): Packmol creates initial configurations for molecular dynamics simulations by packing molecules to meet specified conditions, aiding in the setup of simulation boxes.
- [ProDy](https://github.com/prody/ProDy): ProDy is a Python package for analyzing protein dynamics and sequence co-evolution, offering tools for comparative modeling and analysis of protein structural dynamics.
- [QUIP](http://libatoms.github.io/QUIP/) - A collection of software tools to carry out molecular dynamics simulations.

## Water

- [PyRod](https://github.com/wolberlab/pyrod): PyRod is a Python software for generating dynamic molecular interaction fields and pharmacophore features based on the protein environment of water molecules in molecular dynamics simulations.
