# User guide

The source files are desktop applications; they require a graphical display and Tkinter. Dialogs and workbook fields are in Chinese. These scripts do not comprise a single-command implementation of the manuscript. Prepare the stage-specific inputs externally and preserve row identities when joining cluster labels back to data. Choose one input worksheet or table at a time.

## 1. EM and AIC

Launch `python src/01_em_aic.py`. Select a UTF-8 CSV, `.xlsx` or `.xls` table and output directory. The first two columns are treated as coordinates; every column from the third onward is used in the model. Prepare a table containing only the intended clustering variables. This script does not calculate CLR or select elements. Missing, nonnumeric or infinite values in model columns cause the affected rows to be omitted and recorded in the output workbook.

Specify the range of cluster counts K and the seed list, inspect the AIC curve, and select final K values. The program fits diagonal-covariance Gaussian mixtures with `random_from_data` initialization, 1500 maximum iterations, tolerance 1e-6, covariance regularization 1e-6 and one initialization per seed. For each K it retains the lowest-AIC fitted model over the supplied seeds. Inspect convergence, cluster sizes and geology as well as AIC; numerical cluster labels are not geological names and can change across fits.

Outputs include an AIC PNG, an Excel workbook with AIC and all seed trials, and an analysis workbook for each selected K containing cluster assignments, model parameters, posterior probabilities and statistics. Output names include a timestamp. The program attempts to open the curve and output location where supported.

## 2. Robust PCA

Launch `python src/02_robust_pca.py`. Select an `.xlsx` or `.xlsm` file and worksheet, output directory and output name. The first two columns are coordinates, followed by at least two element columns. **Use unit-consistent, finite, strictly positive concentrations**, with missing and censored values handled beforehand; do not use CLR, ILR, Z-score or negative-valued data here. Prepare a separate file for each cluster if performing cluster-specific analysis.

The parameter dialog offers alpha in [0.50, 1.00] (default 0.50), an integer random seed (default `random`, a newly generated seed), and the candidate loading threshold (`auto` means 1/sqrt(D), where D is the number of input elements). At most PC1–PC20 are included; fewer are available when D-1 < 20. Record an explicit seed for repeatability. The threshold is a screening aid, not a geological decision rule.

The output includes a detailed workbook with ILR basis/data, MCD estimates, sample scores, explained variance, CLR element loadings and checks; a second core workbook contains a subset of key tables. Choose meaningful element associations from loadings and geological context; the software does not make the final geological selection.

## 3. FMCD

Launch `python src/03_fmcd.py`. Select a preprocessed CSV or Excel table and worksheet where applicable. The first two columns are coordinates; choose at least two remaining variables by name, or accept all. Input must be numeric and finite with nonzero variance, and n must exceed p+1. No missing-value replacement, CLR, ILR, standardization or outlier removal is performed. To follow the manuscript's stated workflow, construct a per-cluster table of the chosen CLR element columns outside this script.

Choose output directory, support fraction (default 0.75), number of random starts (GUI default 1000, minimum 100), initial C-steps (2), retained candidates (20), maximum final C-steps (100), reweight quantile (0.975), anomaly quantile (0.975), and seed (42). The program uses ridge 1e-12. The support-size lower bound depends on n and p; invalid choices raise an error. The synthetic API-level tutorial uses only 30 starts for speed and does not reproduce the GUI default or establish the paper's exact settings.

One Excel workbook contains sample distances and anomaly classes, parameters, anomaly counts, the robust center and covariance. The squared-distance cutoff uses a chi-square quantile with degrees of freedom equal to the selected variable count. Review covariance rank and other diagnostics; a singular or ill-conditioned covariance can make interpretation unreliable. An anomaly is a statistical departure from the fitted background, not proof of mineralization.

## Inputs and interpretation

Element units must be consistent and the treatment of censored values must be documented externally. A CLR transformation over D components has a zero-sum constraint; using all D CLR columns creates an exact linear dependency. The sample tutorial selects 14 of the 39 CLR columns for EM and a smaller association for each FMCD calculation. This is a demonstration choice, not a general geological selection rule. Depending on your selected data and model, assess rank and the scientific implications of the chosen representation.
