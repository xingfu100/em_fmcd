"""Exercise the manuscript-style pipeline using fictional data only.

The example follows the methods, not the original paper's observations or
geological decisions. K=5 and associations are fixed for demonstration.
"""
import importlib.util
import os
from pathlib import Path
import sys

# Keep the demonstration practical on common multi-core laptops.
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "examples" / "synthetic_1200x39.csv"
INDICATORS = ["Be", "Cr", "F", "La", "Li", "Nb", "P", "Ti", "V", "Y", "Al2O3", "Fe2O3", "K2O", "SiO2"]
# Labels are arbitrary: these are illustrative input associations, not new
# associations established by RPCA on the synthetic data.
ASSOCIATIONS = [["Pb", "Zn", "Cu", "F"], ["Pb", "W", "B", "Bi"],
                ["Pb", "Bi", "Sn"], ["Pb", "Cu", "Zn", "Ti", "Y", "Zr", "Cr", "Li"],
                ["Pb", "Li", "Be", "Sn", "Y"]]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(output_dir):
    em = load("em", "01_em_aic.py")
    rpca = load("rpca", "02_robust_pca.py")
    fmcd = load("fmcd", "03_fmcd.py")
    table = pd.read_csv(DATA)
    columns = list(table.columns[2:])
    raw = table[columns].to_numpy(dtype=float)
    assert raw.shape == (1200, 39) and np.all(np.isfinite(raw)) and np.all(raw > 0)
    clr = np.log(raw) - np.log(raw).mean(axis=1, keepdims=True)
    clr_df = pd.DataFrame(clr, columns=columns)
    X = clr_df[INDICATORS].to_numpy()
    models, trial_frames = {}, []
    for k in range(2, 7):
        models[k], trials = em.fit_best_gmm_by_seeds(X, k, [7, 42])
        trial_frames.append(trials)
    labels = models[5].predict(X)
    assert np.unique(labels).size == 5
    output_dir.mkdir(parents=True, exist_ok=True)
    table.to_excel(output_dir / "synthetic_concentrations.xlsx", index=False)
    pd.concat([table[["X_coord", "Y_coord"]], clr_df], axis=1).to_csv(output_dir / "synthetic_clr.csv", index=False)
    pd.concat(trial_frames, ignore_index=True).to_csv(output_dir / "gmm_trials.csv", index=False, encoding="utf-8-sig")
    summary, all_rows, loading_rows = [], [], []
    for label in sorted(np.unique(labels)):
        mask = labels == label
        assert mask.sum() > len(columns), f"Cluster {label} is too small for the 38 ILR coordinates"
        pc = rpca.运行ILR_MCD_RPCA(raw[mask], columns, 0.5, 42)
        selected = ASSOCIATIONS[int(label)]
        matrix = clr_df.loc[mask, selected].to_numpy()
        mcd = fmcd.fast_mcd(matrix, starts=30, keep_best=5, seed=42)
        dist = mcd["final_md2"]
        cutoff = fmcd.chi2_ppf(0.975, len(selected))
        assert np.all(np.isfinite(dist)) and np.all(dist >= 0)
        assert pc["clr_reconstruction_error"] < 1e-10
        np.testing.assert_allclose(pc["clr_loadings_all"].sum(axis=0), 0, atol=1e-9)
        summary.append({"cluster": int(label), "n": int(mask.sum()), "association": "+".join(selected),
                        "pc1_explained_fraction": float(pc["explained_ratio"][0]),
                        "chi_square_cutoff": cutoff, "anomalies": int((dist > cutoff).sum())})
        for j, name in enumerate(columns):
            loading_rows.append({"cluster": int(label), "element": name,
                                 "PC1": float(pc["clr_loadings_all"][j, 0]),
                                 "PC2": float(pc["clr_loadings_all"][j, 1])})
        all_rows.extend({"synthetic_row": int(idx), "cluster": int(label),
                         "md2": float(d), "anomaly_index": float(d / cutoff)}
                        for idx, d in zip(np.flatnonzero(mask), dist))
    pd.DataFrame(summary).to_csv(output_dir / "cluster_summary.csv", index=False)
    pd.DataFrame(loading_rows).to_csv(output_dir / "rpca_pc1_pc2_loadings.csv", index=False)
    pd.DataFrame(all_rows).sort_values("synthetic_row").to_csv(output_dir / "sample_results.csv", index=False)
    print(f"PASS: 1200 synthetic samples, 39 elements, five clusters; outputs: {output_dir}")


if __name__ == "__main__":
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "example_output")
