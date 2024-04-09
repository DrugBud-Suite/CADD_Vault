# Molecule Representations

## Fingerprints

- **Tools**
  - [SciKit-fingerprints](https://github.com/Arch4ngel21/scikit-fingerprints): A Python library for efficient computation of molecular fingerprints.
  - [RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity): Offers comprehensive tools for fingerprinting and molecular similarity, supporting various fingerprint types for chemical informatics.
  - [XenonPy](https://github.com/yoshida-lab/XenonPy/blob/master/xenonpy/descriptor/fingerprint.py): XenonPy provides a descriptor module for generating molecular fingerprints, part of a versatile Python library for materials informatics.
  - [QSAR_toolbox](https://github.com/iwatobipen/QSAR_TOOLBOX): scripts for QSAR model building and fingerprint generation
  - [MoleculaPy](https://github.com/kamilpytlak/MoleculaPy): A command-line application that utilizes the RDKit library to compute molecular descriptors and fingerprints, aiding in the analysis and characterization of chemical structures.
  - [E3FP](https://github.com/keiserlab/e3fp) - Converts molecules from conventional representations into a folded fingerprint for three-dimensional molecular shapes.
  - Graphlet fingerprint: [Minervachem](https://github.com/lanl/minervachem) - Provides a method for analyzing molecular graphlets, offering a unique approach to molecular characterization and comparison.

## Protein-ligand interaction

- [PLIP](https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index): An easy and fast web tool for identifying non-covalent interactions between biological macromolecules and their ligands.
- [SPLIF](https://doi.org/10.1021/ci500319f): The link leads to a DOI page which typically hosts scientific publications; SPLIF is a method for encoding protein-ligand interactions.
- [ProLIF](https://github.com/chemosim-lab/ProLIF): ProLIF (Protein-Ligand Interaction Fingerprints) generates interaction fingerprints for complexes made of ligands, protein, DNA, or RNA molecules extracted from molecular dynamics trajectories, docking simulations, and experimental structures.
- [2D-SIFt](https://bitbucket.org/zchl/sift2d/src/master/): 2D-SIFt provides a two-dimensional method for analyzing protein-ligand interactions.
- [BINANA](https://durrantlab.pitt.edu/binana-download/): BINANA is a tool for characterizing the binding interactions of ligands with proteins.

## Descriptors

- **Tools**
  - [GuideMol](https://github.com/jairesdesousa/guidemol): A tool for guiding molecular design through machine learning models.
  - [mordred](https://github.com/mordred-descriptor/mordred): A molecular descriptor calculator that is extendable and supports various chemical informatics tasks.
  - [DescriptaStorus](https://github.com/bp-kelley/descriptastorus): Provides a framework for computing chemistry descriptors and (optionally) storing them for machine learning applications.
  - [PaDEL](http://yapcwsoft.com/dd/padeldescriptor/): A software for calculating molecular descriptors and fingerprints.
  - [ChemoPy](https://github.com/ifyoungnet/Chemopy?tab=readme-ov-file): A Python library for calculating chemical descriptors for QSAR/SAR/QSPR studies.
  - [ChemDes](http://www.scbdd.com/chemdes/): An integrated web-based platform for molecular descriptor and fingerprint computation.
  - [SPOC](https://github.com/WhitestoneYang/spoc): A tool for calculating spatial and physicochemical descriptors from molecular dynamics simulations.
  - [Molecular3DLengthDescriptors](https://github.com/ThomasJewson/Molecular3DLengthDescriptors): Provides descriptors based on the three-dimensional lengths of molecules.
  - [PyL3dMD](https://github.com/panwarp/PyL3dMD): A Python library for 3D molecular descriptors calculation from molecular dynamics simulations.
  - [ChemDes](https://github.com/ifyoungnet/ChemDes): web-based platform for molecular descriptor and fingerprint computation
  - [DScribe](https://github.com/SINGROUP/dscribe) - Descriptor library containing a variety of fingerprinting techniques, including the Smooth Overlap of Atomic Positions (SOAP).
- **Descriptors**
  - [Spectrophores](https://github.com/silicos-it/spectrophore): Calculates spectrophoric descriptors that capture electronic and spatial properties of molecules.
  - [QED](https://github.com/silicos-it/qed): Offers the Quantitative Estimate of Drug-likeness for a given molecular structure.
  - [WHALES Descriptors](https://github.com/grisoniFr/whales_descriptors): compute Weighted Holistic Atom Localization and Entity Shape (WHALES) descriptors starting from an rdkit supplier file
  - [SPMS](https://github.com/licheng-xu-echo/SPMS): spherical projection descriptor of molecular stereostructure (SPMS), which allows precise representation of the molecular vdW surface.
  - [CATS-descriptor](https://github.com/alexarnimueller/cats-descriptor)
  - [DompeKeys](https://dompekeys.exscalate.eu/): a new substructure-based fingerprint descriptor, encoding patterns of functional groups and chemical features

## Other Representations

- **Strings**
  - [SMILESAugmentation](https://github.com/jcorreia11/SMILESAugmentation): A tool for augmenting SMILES strings to enhance the performance of machine learning models in cheminformatics.
  - [t-SMILES](https://github.com/juanniwu/t-smiles): Transforms SMILES strings for improved molecular representation and machine learning model performance.
  - [SMARTS](https://github.com/SqrtNegInf/SMARTS): A tool for generating and working with SMARTS, a language for specifying substructural patterns in molecules.
  - [EvoMPF](https://zivgitlab.uni-muenster.de/ag-glorius/published-paper/evompf): EvoMPF is a framework for evolutionary molecular pattern finding using SMARTS.
  - [selfies](https://github.com/aspuru-guzik-group/selfies) - Self-Referencing Embedded Strings (SELFIES): A 100% robust molecular string representation.
- [UniMAP](https://github.com/fengshikun/UniMAP): UniMAP offers a unified approach to molecular annotation and property prediction.
- [TUCAN](https://github.com/TUCAN-nest/TUCAN): TUCAN is a tool for transforming unstructured chemical annotations into normalized expressions.
- [mol2vec](https://github.com/samoturk/mol2vec): Generates vector representations of molecular substructures for machine learning applications.
- **Transformers**
  - [BERT](https://github.com/odb9402/MoleculeTransformer): A transformer model specifically designed for molecular property prediction tasks.
  - [molfeat](https://molfeat-docs.datamol.io/stable/)
- **Fragments**
  - [molZ](https://github.com/LiamWilbraham/molz): molZ offers a novel method for fragment-based molecular representation for machine learning models.
- **Compressed Representation**
  - [PaCh](https://pubs.acs.org/doi/10.1021/acs.jcim.3c01720)

## Graphs
- [graphium](https://graphium-docs.datamol.io/stable/)
- 