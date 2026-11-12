"""Generate fictional concentrations; no observed study data are used."""
from pathlib import Path
import numpy as np
import pandas as pd

cols = ['Be','Cr','F','La','Li','Nb','P','Ti','V','Y','Al2O3','Fe2O3','K2O','SiO2','Pb','Zn','Cu','W','B','Bi','Sn','Zr','Ag','As','Ba','Cd','Co','Ga','Ge','Hg','Mn','Mo','Ni','Sb','Sc','Sr','Th','U','Rb']
rng = np.random.default_rng(2024)
n = 1200
group = np.arange(n) % 5
log_values = rng.normal(2, 0.27, size=(n, 39))
centers = np.array([[1.3,-.7,-.6,.1,.5],[-.4,1.3,-.6,.6,-.8],[-.6,-.5,1.3,-.5,.6],[-.4,.3,-.6,1.3,-.6],[-.5,-.5,.1,-.6,1.3]])
for j in range(5):
    log_values[:, j] += centers[group, j]
df = pd.DataFrame(np.exp(log_values), columns=cols)
df.insert(0, 'Y_coord', np.zeros(n, dtype=int))
df.insert(0, 'X_coord', np.arange(n))
out = Path(__file__).resolve().parent / 'synthetic_1200x39.csv'
df.to_csv(out, index=False, float_format='%.8f')
print(f'Wrote {out}: {n} artificial samples, {len(cols)} elements')
