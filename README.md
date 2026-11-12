# EM–FMCD geochemical anomaly analysis

This repository contains three interactive Python programs used in a geochemical workflow: EM/Gaussian-mixture clustering with AIC, robust PCA after ILR transformation, and FAST-MCD robust Mahalanobis distance estimation. The program code comments and docstrings are in English; the graphical dialogs, console messages, and output worksheet names are in Chinese.

## Repository contents

- [01_em_aic.py](src/01_em_aic.py): EM clustering and multi-seed AIC comparisons.
- [02_robust_pca.py](src/02_robust_pca.py): ILR–MCD robust PCA and CLR loadings.
- [03_fmcd.py](src/03_fmcd.py): robust distances, thresholds, and anomaly classes.
- [Synthetic data](examples/synthetic_1600x39.csv): 1,600 artificial samples and 39 variables, with no real coordinates.
- [Synthetic workflow](examples/synthetic_workflow.py): manuscript-style demonstration of the three computational cores.
- [Data generator](examples/generate_synthetic.py): regenerate the artificial dataset with a fixed seed.
- [User guide](docs/USER_GUIDE.md): input formats, options, and outputs.
- [Synthetic tutorial](docs/TUTORIAL.md): commands, data generation and output interpretation.
- [Data and reproducibility](docs/DATA_AND_REPRODUCIBILITY.md): scope and limitations for reproducing the manuscript.
- [LICENSE](LICENSE): MIT license.

## Installation

Clone the repository and enter its directory:

```text
git clone https://github.com/xingfu100/em_fmcd.git
cd em_fmcd
```

A desktop environment with Python and Tkinter is needed for the interactive programs. The synthetic example uses no GUI. Windows with Python 3.14.5 was used for the checks below; other platforms and versions have not been verified. A Chinese-capable font is recommended for GUI plots and Excel output.

```text
python -m venv .venv
```

Activate with `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux), then install dependencies:

```text
python -m pip install -r requirements.txt
```

The tested Windows environment, including transitive dependencies, is recorded in `requirements-tested-windows.txt`. This is a record of one tested environment, not a promise that those exact versions support other operating systems. Excel `.xls` input requires `xlrd`; `.xlsx` input/output requires `openpyxl`.

## Run

Start each application from the repository root and follow the dialogs:

```text
python src/01_em_aic.py
python src/02_robust_pca.py
python src/03_fmcd.py
```

These programs are separate interactive steps, not a fully automatic pipeline. EM consumes selected preprocessed variables; RPCA requires strictly positive raw concentration data for each cluster, while FMCD requires already preprocessed variables for the selected association. Data preparation, cluster-wise table construction and geological interpretation are manual. See the [user guide](docs/USER_GUIDE.md).

## Quick test and synthetic example

```text
python tests/quick_test.py
python examples/synthetic_workflow.py
```

The first command checks parsing and Chinese characters in source comments and docstrings. The second reads the included synthetic 1,600-sample, 39-element dataset and exercises all three computational cores without launching GUIs; on success it prints `PASS` and writes files under `results_irregular/`. To choose a different destination, append its path, for example `python examples/synthetic_workflow.py my_output`. See the [tutorial](docs/TUTORIAL.md) for expected outputs and limitations.

## Synthetic clustered and regional comparison

The example generates a fictional 40 × 40 grid with 39 synthetic elements, interleaved background units, two distinct bodies, and an imposed Pb-enrichment pattern. It is inspired by the layout of geological units, not extracted or digitized from the study-area map. Coordinates are artificial indices. The synthetic generator intentionally separates backgrounds and selects a row permutation that gives K=5 seed 42 one initialization point per designed unit. This makes the demonstration favorable to EM; it is not independent evidence of superior performance on real geological data.

The pipeline applies CLR to all 39 variables, fits EM with K=5, then performs ILR–RPCA and FMCD within each cluster and independently for the entire region. The simulated imposed anomaly mask permits a transparent comparison with known synthetic truth. [Model summary](results_irregular/model_summary.csv), [sample comparison](results_irregular/sample_comparison.csv), [loadings](results_irregular/rpca_loadings.csv), and [detection metrics](results_irregular/detection_comparison.csv) are provided. [Tutorial](docs/TUTORIAL.md) explains the assumptions, parameters, preprocessing and limits.

![Synthetic EM blocks](results_irregular/figure_em.png)

![Synthetic clustered and regional anomaly maps](results_irregular/figure_anomalies.png)

![Synthetic RPCA loadings](results_irregular/figure_rpca.png)

## Study data and reproducibility

The study dataset cannot be publicly released. The reason and data-access arrangements have not yet been supplied. The synthetic example contains no real sample values or geographical coordinates and cannot reproduce the manuscript's numerical results. The repository does not currently contain the actual study data, all processing decisions, or verified manuscript-level reproduction instructions. See [data and reproducibility](docs/DATA_AND_REPRODUCIBILITY.md).

## License

MIT; see [LICENSE](LICENSE).
