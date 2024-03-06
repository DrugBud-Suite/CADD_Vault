### Docking
- [Lit-PCBA](https://drugdesign.unistra.fr/LIT-PCBA/index.html): A dataset for virtual screening and machine learning with 15 target sets, 7761 actives, and 382674 unique inactives selected from high-confidence PubChem Bioassay data.
- [MF-PCBA](https://github.com/davidbuterez/mf-pcba): A repository containing code for downloading, filtering, and assembling the MF-PCBA datasets for machine learning in drug discovery.
- [DEKOIS](http://www.pharmchem.uni-tuebingen.de/dekois/): Provides DEKOIS 2.0, a library of benchmark data sets for objective in silico screening.
- [Disco](http://disco.csb.pitt.edu/Targets_top1.php?ligands): A default benchmark containing 95 targets selected from the DUD-E Targets list for docking datasets generation.
- [TocoDecoy](https://github.com/5AGE-zhang/TocoDecoy): A new approach to design unbiased datasets for training and benchmarking machine-learning scoring functions.
	- [TocoDDB](http://cadd.zju.edu.cn/tocodecoy/)
- [MUDB-DecoyMaker](https://github.com/taoshen99/MUBDsyn): A tool for making synthetic Maximal Unbiased Benchmarking Datasets via Deep Reinforcement Learning.
	- [MUDB-DecoyMaker2.0](https://github.com/jwxia2014/MUBD-DecoyMaker2.0): A Python GUI application to generate maximal unbiased benchmarking sets data sets for virtual drug screening.
- [CASF](http://www.pdbbind.org.cn/casf.php): CASF offers benchmark packages for the assessment of scoring functions, with versions CASF-2016, CASF-2013, and CASF-2007 available for download upon registration.
### PL interaction
- [PDBscreen](https://zenodo.org/records/8049380): PDBscreen provides a dataset with multiple data augmentation strategies suitable for training protein-ligand interaction prediction methods.
- [PLAS-20K](https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/64cca66569bfb8925a5514c5/original/plas-20k-extended-dataset-of-protein-ligand-affinities-from-md-simulations-for-machine-learning-applications.pdf)
- [BindingNet](http://bindingnet.huanglab.org.cn/):  BindingNet is a dataset for analyzing protein-ligand interactions, containing modeled poses for compounds similar to the crystal ligands found in PDBbind, along with corresponding activities from ChEMBL.
- [MF-PCBA](https://github.com/davidbuterez/mf-pcba) : This repository includes the code for assembling multi-fidelity datasets from PubChem, aiming to enhance machine learning models for HTS data by integrating low and high-fidelity measurements.
- [BioLip2](https://zhanggroup.org/BioLiP/index.cgi): BioLiP is a semi-manually curated database for high-quality, biologically relevant ligand-protein binding interactions, aiming to serve the needs of ligand-protein docking, virtual ligand screening, and protein function annotation.
- [Leak Proof PDBBind](https://arxiv.org/abs/2308.09639): This work presents a cleaned PDBBind dataset of non-covalent binders, reorganized to avoid data leakage, allowing for more generalizable binding affinity prediction.
- [BindingDB](https://www.bindingdb.org/bind/index.jsp): BindingDB contains data for over 1.2 million compounds and 9.2k targets, supporting research, education, and practice in drug discovery, pharmacology, and related fields.
### Drugs
- [DrugCentral](https://drugcentral.org/): DrugCentral provides information on active ingredients in medicinal substances, offering access to drug labels, FDA and EMA datasets, pharmacological action, and more.
### Make on Demand Libraries
- [FreedomSpace](https://chem-space.com/compounds/freedom-space)
### Natural Products
- [LOTUS](https://lotus.naturalproducts.net/): LOTUS is a significant, well-annotated resource for natural products, offering a user-friendly experience including structural search, taxonomy-oriented queries, and exports.
- [COCONUT](https://coconut.naturalproducts.net/): COCONUT hosts one of the largest and best annotated natural product databases, freely available and undergoing continuous curation and improvement.
- [SymMap](http://www.symmap.org/): SymMap integrates traditional Chinese medicine with modern medicine through molecular mechanisms and symptom mapping, offering information on herbs, ingredients, targets, symptoms, and diseases.
### Chemical

- [ChemBL](https://www.ebi.ac.uk/chembl/): A manually curated database of bioactive molecules with drug-like properties, integrating chemical, bioactivity, and genomic data to aid drug discovery.
- [chembl_downloader](https://github.com/cthoyt/chembl-downloader): A Python package designed to automatically download and extract versions of the ChemBL database, simplifying data access for research purposes.
- [chembl_tools](https://github.com/mgalardini/chembl_tools): A collection of scripts to leverage the ChemBL API for retrieving information on compounds, including ChEMBL IDs and target information.
- [DrugBank](https://go.drugbank.com/): Offers structured drug information, including emerging research and novel connections, to support drug discovery, clinical software, and academic research.
- [ZINC](https://zinc.docking.org/): A free database for virtual screening containing over 230 million purchasable compounds in ready-to-dock, 3D formats.
- [DrugCentral](https://drugcentral.org/): Provides information on active ingredients in medicinal substances, offering access to drug labels, FDA and EMA datasets, pharmacological action, and more.
- [GDB-17](http://gdb.unibe.ch/): The GDB-17 database represents a comprehensive collection of hypothetical organic molecules for use in computational chemistry and drug discovery.
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/): The world's largest collection of freely accessible chemical information, offering chemical and physical properties, biological activities, safety and toxicity information, patents, literature citations, and more.
- [ChemSpider](http://chemspider.com/): A free chemical structure database providing fast access to over 100 million structures from hundreds of data sources, including physical properties, literature references, and supplier information.
- [ChemMine](http://chemminedb.ucr.edu/): A compound mining portal to facilitate drug and agrochemical discovery, offering chemical genomics screens and a toolbox for cheminformatics research.

### Protein Structures

- [PDB](https://www.rcsb.org/): The RCSB Protein Data Bank provides access to experimentally determined 3D structures from the PDB archive and computed structure models, offering tools for exploration, visualization, and analysis.
    - [Lemon](https://github.com/chopralab/lemon): A framework for rapidly mining structural information from the Protein Data Bank, designed to be fast and flexible for querying 3D features of structures.
- [PDB-redo](https://pdb-redo.eu/): Offers optimized versions of PDB entries through an automated procedure that refines, rebuilds, and validates structural models, combining popular crystallographic software with specially developed tools.

### Protein Sequences
- Alignments
	- [OpenProteinSet](https://arxiv.org/abs/2308.05326): OpenProteinSet is an open-source corpus of more than 16 million Multiple Sequence Alignments (MSAs), associated structural homologs from the Protein Data Bank, and AlphaFold2 protein structure predictions. It's designed to be broadly useful as training and validation data for tasks focused on protein structure, function, and design, as well as large-scale multimodal machine learning research.
### Molecular Dynamics
- **[ATLAS](https://www.dsimb.inserm.fr/ATLAS)**: Resource for exploring molecular dynamics simulations, offering insights into the dynamics of proteins and other biomolecules.

### Properties
- [Molecules Dataset Collection](https://github.com/GLambard/Molecules_Dataset_Collection?tab=readme-ov-file): - Selection of data sets of molecules (SMILES) and physicochemical properties