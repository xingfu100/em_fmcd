# Synthetic geological-style comparison

The fictional 40 × 25 grid has 1,000 samples and 39 positive element variables. Grid indices are not geographic coordinates and no values or positions are extracted from the study data or geological map. Five hypothetical lithologies—carbonate, sandstone, shale, granite and mudstone—form interleaving background units and two irregular bodies. Some samples have mixed background signatures, and transitional mixtures occur at unit boundaries; an artificial Pb enrichment belt and local spots are added with different associated elements in each unit. One unit has a higher Pb background. The sample order is shuffled once using seed 42; model outcomes are not selected to satisfy any target performance metric.

## Run

```text
python tests/quick_test.py
python examples/generate_synthetic.py
python examples/synthetic_workflow.py
python examples/plot_results.py
```

The generator writes the fictional input CSV and a synthetic ground-truth CSV. The workflow writes `results_irregular/`: GMM trials, `model_summary.csv`, `rpca_loadings.csv`, `sample_comparison.csv` and `detection_comparison.csv`. The plotting script writes three manuscript-inspired PNG figures. It always reads `results_irregular/`.

## Processing

1. The synthetic data are finite and strictly positive; no nondetect replacement, unit conversion, Z-score or outlier deletion is applied. Coordinates and observations are only fictional. Calculate a single CLR across **all 39** concentration columns for every sample. No cluster-specific recentering or new CLR over selected subsets is performed for EM or FMCD.
2. Fit EM at K=5 with the manuscript's 14 indicators, seed 42 and the source script's diagonal-covariance settings. Labels are arbitrary and plots display label + 1.
3. Run RPCA independently for each EM cluster and once for all 1,000 observations. RPCA receives positive original values and internally calculates CLR, pivot ILR and MCD–PCA. For each model, use PC1–PC2 CLR loadings to select Pb plus 2–5 elements: rank positive-direction elements by cosine similarity with Pb multiplied by loading-vector length, preferring cosine ≥0.8; if necessary use the top two positive candidates. This reproducible numerical heuristic approximates the paper's qualitative same-direction and magnitude interpretation. It is not a correlation coefficient or a geological decision rule.
4. Use the previously computed 39-component CLR values for the selected variables. Run FMCD per cluster and once globally with support fraction 0.75, 1000 starts, initial C-steps 2, 20 retained candidates, up to 100 final C-steps, ridge 1e-12, reweight quantile 0.975 and seed 42. The anomaly index divides MD² by the 0.975 chi-square cutoff. Background ≤1; weak (1,1.5]; moderate (1.5,2]; strong >2. Within-cluster and regional element selections may differ, matching the paper's separate RPCA approach but confounding a comparison of EM alone.

## Limits of comparison

Synthetic concentrations are expressed on a common ppm-equivalent scale. The simulated oxide sum is capped at 950,000 ppm. Approximate marginal scales for Sn and six major oxides were informed by broad distribution summaries of a separate stream-sediment table; the other variables and all sample values and coordinates are simulated. The input table is not included. The model is illustrative and is not a fitted generative model for the full 39-element distribution.

The synthetic reference mask is the arbitrarily selected imposed-intensity threshold 0.55; it is not a measured mineral deposit or proven anomaly. Confusion-matrix metrics quantify this single constructed example only. Favorable recovery under these assumptions does not establish that EM is always needed or that it improves real-data performance. Boundaries and modeled signatures are synthetic; the results do not reproduce the manuscript's study-area sample outcomes. The tests call the numerical functions directly, not the desktop dialogs.
