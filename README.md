# Code and data for: Engineered Nano-Biochar Hybrids for Soil Organic Carbon Stabilization: Synergies in Greenhouse Gas Mitigation and Heavy Metal Remediation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23098891.svg)](https://doi.org/10.5281/zenodo.23098891)

Author: Praveen Kumar, Department of Genetics and Plant Breeding, College of Agriculture, Agriculture University Jodhpur, Rajasthan, India (bkpraveenars@gmail.com)

## Zenodo

Concept DOI: [10.5281/zenodo.23098891](https://doi.org/10.5281/zenodo.23098891)  
Published version: [10.5281/zenodo.23098892](https://doi.org/10.5281/zenodo.23098892)

This archive is Supplementary Code S1 and Supplementary Data S1 of the review. It reproduces every model calculation and figure. The review generated no new experimental data; empirical values in Fig. 4 are taken from the cited primary studies. The multi-environment trial data are SIMULATED to illustrate the analytical pipeline and are not field evidence.

## Contents
- `code/style.py` - shared figure style (600 dpi PNG + LZW TIFF export to `figures/`)
- `code/fig1.py` - Fig. 1, conceptual framework
- `code/fig2.py` - Fig. 2, nano-trilemma: geometric surface area (Eq. 1), size-scaled two-pool decay (Eq. 2), colloid filtration travel distance (Eq. 3; Tufenkji-Elimelech correlation)
- `code/fig3.py` - Fig. 3, Nernst potentials at pH 7 (Eq. 6) and seasonal electron budget (Eq. 7)
- `code/fig4.py` - Fig. 4, verified sorption capacities on mass and molar bases; HSAB absolute hardness
- `code/fig5.py` - Fig. 5, evidence-graded synergy-antagonism matrix (scores and grades defined in the file)
- `code/fig5b.py` - Fig. 6, bipartite network view of Fig. 5
- `code/fig7pipe.py` - Fig. 7, biometrical translation pipeline
- `code/fig6.py` - Fig. 8 and Table 6: simulation of a 6 genotype x 3 amendment x 8 environment x 3 replicate trial; ANOVA partition, AMMI (IPCA, ASV, YSI, WAASB), Finlay-Wilkinson slopes (random seed 2026)
- `code/fig7.py` - Fig. 9, Monte Carlo power analysis (random seed 7; 4000 runs per point)
- `data/simulated_GxAxE_trial.csv` - plot-level simulated yields (columns: genotype, amendment, environment, water_index, rep, yield_t_ha)
- `data/met_results.json` - ANOVA, IPCA and per-entry stability statistics reported in Table 6 and Section 7.4
- `figures/` - all nine figures as 600 dpi TIFF

## Running
Python 3.10 or later. Install with `pip install -r requirements.txt`, then from the `code/` folder run, for example, `python fig2.py`. Figures are written to `figures/`. `fig5b.py` imports `fig5.py`, so keep both in the same folder. Fonts default to Liberation Sans; matplotlib falls back to DejaVu Sans if it is absent, which changes typography only.

## Licence
Code: MIT. Data and figures: CC BY 4.0.

## Citation
Please cite the article and this archive (DOI assigned by Zenodo).
