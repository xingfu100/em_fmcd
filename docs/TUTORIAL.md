# Synthetic 40 × 40 geochemical workflow

The dataset `examples/synthetic_1600x39.csv` contains 1,600 fictional samples on a 40 × 40 integer grid and 39 artificial element variables. Coordinates are grid indices, not real geographic locations. A generator using seed 42 assigns five contiguous spatial background blocks with distinct indicator signatures and embeds an oblique Pb enrichment trend with block-specific associated elements. These characteristics are deliberately designed, not observed geology. Rows are deliberately permuted to give seed 42 a favorable initialization for the present scikit-learn `random_from_data` implementation; the clean blocks therefore are not evidence of robust classification on real datasets.

Install the dependencies in the README and run:

```text
python tests/quick_test.py
python examples/synthetic_workflow.py
```

The workflow calculates CLR across all 39 variables and fits EM with K=5 using 14 lithological indicators and seed 42. It computes cluster-specific ILR–MCD RPCA on the 39 original positive values with alpha 0.50 and seed 42. For each cluster, it represents Pb and each element as their two CLR loading coordinates (PC1, PC2). It ranks elements with positive cosine similarity to Pb by cosine multiplied by their loading-vector length; it selects up to five with cosine at least 0.8, and fills a minimum of two positive-direction partners when needed. Thus each combination contains Pb plus 2–5 elements. This explicit heuristic operationalizes the paper's directional and relative-loading criteria for the demonstration; it is not a Pearson correlation and does not replace geological interpretation. If Pb has negligible PC1–PC2 loading or fewer than two candidates, the workflow fails rather than inventing an association.

FMCD operates on each cluster's chosen CLR variables using seed 42 and the original function defaults: support fraction 0.75, 1000 starts, two initial C-steps, 20 candidates, maximum 100 C-steps, ridge 1e-12 and reweight quantile 0.975. The anomaly cutoff is the 0.975 chi-square quantile with degrees of freedom equal to the number of selected variables. Output includes sample-level cluster, distance, threshold and anomaly index; selected associations and PC1/PC2 loadings; and GMM trials. The recorded results in `results_1600/` were generated with the tested Windows environment. Cluster numbers are arbitrary.

The example calls computational functions directly; it does not automate the GUIs, maps in the paper, or all geological decisions. It validates numerical execution on designed synthetic data, not reproducibility of paper results. `generate_synthetic.py` can regenerate the fictional dataset. Real study data and geographic locations are not included.
