# Synthetic workflow tutorial

The repository contains `examples/synthetic_1200x39.csv`, a fully fictional dataset of 1,200 samples and 39 named variables. `X_coord` is a synthetic row index and `Y_coord` is zero: neither is a real geographic coordinate. Concentrations are simulated with NumPy seed 2024 and do not correspond to real observations or measured units. `examples/generate_synthetic.py` regenerates this file. Use it only for a computational demonstration, not geological interpretation.

Install the dependencies (README) and run from the repository root:

```text
python tests/quick_test.py
python examples/synthetic_workflow.py
```

The example applies the paper's main processing sequence:

1. Calculate CLR from all 39 strictly positive artificial variables.
2. Fit Gaussian mixtures with K=2–6 and seeds 7 and 42 using the 14 paper indicators: Be, Cr, F, La, Li, Nb, P, Ti, V, Y, Al2O3, Fe2O3, K2O and SiO2. As an example, choose K=5 as in the paper; the code does not claim AIC alone selects it.
3. For each of five fitted groups, calculate ILR–MCD robust PCA from all 39 positive concentrations, and save PC1–PC2 loadings mapped to CLR element space.
4. Calculate group-specific FMCD from selected CLR variables and compare squared distances with chi-square cutoffs at 0.975. The script uses five combinations appearing in the manuscript as *illustrative* input selections, assigned in arbitrary model-label order. GMM labels are arbitrary, and these combinations are not inferred from the synthetic PCA or evidence of mineralization.

On success a `PASS` message is printed and `example_output/` contains `synthetic_concentrations.xlsx`, `synthetic_clr.csv`, `gmm_trials.csv`, `rpca_pc1_pc2_loadings.csv`, `cluster_summary.csv` and `sample_results.csv`. Sample indices in the last file are zero-based. RPCA uses alpha 0.50 and seed 42; EM uses seeds 7 and 42; FMCD uses seed 42 and 30 starts, five retained candidates and other function defaults. These are demonstration parameters and do not establish the manuscript's exact settings. Numerical cluster labels can change between library versions. The reduced FMCD starts speed testing and differ from the GUI default of 1000.

The script invokes the original computational functions directly rather than the GUI or the complete Excel-export pipeline. It checks data shape, positivity, finite squared distances, CLR reconstruction and loading sums. It does not establish GUI operation, real-data equivalence, map generation, actual element-association selection or statistical validity for arbitrary datasets. For GUI operation and input/output details see [USER_GUIDE.md](USER_GUIDE.md).
