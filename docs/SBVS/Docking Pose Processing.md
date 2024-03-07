# Post-processing of docking poses

- **Interaction Filtering**
 	- **[LigGrep](https://durrantlab.pitt.edu/liggrep/)**: LigGrep is a program for identifying docked poses that participate in specified receptor/ligand interactions, accepting a protein receptor file, docked-compound files, and user-specified filters as input.
 	- **[BINANA](https://durrantlab.pitt.edu/binana-download/)**: BINANA analyzes the geometries of predicted ligand poses to identify molecular interactions that contribute to binding, also featuring a web-browser application for visualizing these interactions.

- **Clustering**
 	- **[ClusterX](https://github.com/ChenSikang/ClusterX)**: ClusterX is a deep clustering framework for learning molecular representations of protein-ligand complexes and accurately clustering ligands, designed to assist computational medicinal chemists in making visual decisions.
- **RMSD calculation**
 	- [spyRMSD](https://github.com/RMeli/spyrmsd): Python tool for symmetry-corrected RMSD calculations.
 	- [rmsd](https://github.com/charnley/rmsd): Calculate Root-mean-square deviation (RMSD) of Two Molecules Using Rotation
 	- **[pyDockRMSD](https://github.com/neudinger/pyDockRMSD)**: DockRMSD is an open-source program that identifies the minimum symmetry-corrected RMSD for docked poses without losing computational efficiency, useful for ligand molecules with complex structural symmetry.
- **Quality Assessment***
 	- [PoseBusters](https://github.com/maabuu/posebusters): Plausibility checks for generated molecule poses.
- **Minimization**
 	- [Vina_pose_Optimization](https://github.com/rongfengzou/vina_pose_optimization): optimize positions of ligand polar hydrogens in docking pose
 	- [DeepRMSD-Vina_Optimisation](<https://github.com/zchwang/DeepRMSD-Vina_Optimization>: This algorithm is based on deep learning and a classical scoring function (Vina score) and is designed to optimize ligand conformations.
- **Other**
 	- [SiteInterlock](https://github.com/rasbt/siteinterlock): based upon the hypothesis that interfacial rigidification of the protein-ligand interface is an important characteristic that can detect the native ligand binding mode
