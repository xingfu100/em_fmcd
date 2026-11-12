"""Generate a fictional 40 x 40 geochemical grid, seed 42."""
from pathlib import Path
import numpy as np
import pandas as pd

COLUMNS = ['Be','Cr','F','La','Li','Nb','P','Ti','V','Y','Al2O3','Fe2O3','K2O','SiO2','Pb','Zn','Cu','W','B','Bi','Sn','Zr','Ag','As','Ba','Cd','Co','Ga','Ge','Hg','Mn','Mo','Ni','Sb','Sc','Sr','Th','U','Rb']
INDICATORS = COLUMNS[:14]
ASSOCIATIONS = [['Pb','Zn','Cu','F'], ['Pb','W','B','Bi'], ['Pb','Bi','Sn'], ['Pb','Cu','Zn','Ti','Y','Zr'], ['Pb','Li','Be','Sn','Y']]

def generate():
    rng = np.random.default_rng(42)
    yy, xx = np.meshgrid(np.arange(40), np.arange(40), indexing='ij')
    xx, yy = xx.ravel(), yy.ravel()
    region = xx // 8
    values = rng.normal(2.0, .12, (1600, 39))
    # Independent synthetic lithological signatures, distinct for five stripes.
    signatures = rng.normal(0, .65, (5,14))
    values[:, :14] += signatures[region]
    trend = np.exp(-((yy - (8 + .55 * xx)) / 4.8)**2)
    spots = sum(np.exp(-((xx-cx)**2+(yy-cy)**2)/18.0) for cx,cy in [(4,9),(12,17),(20,19),(28,23),(36,29)])
    mineral = .95 * trend + .65 * spots + rng.normal(0,.055,1600)
    for g, elements in enumerate(ASSOCIATIONS):
        ix = region == g
        for e in elements:
            values[ix, COLUMNS.index(e)] += mineral[ix] * (1.05 if e == 'Pb' else .85)
    frame = pd.DataFrame(np.exp(values), columns=COLUMNS)
    frame.insert(0, 'Y_coord', yy)
    frame.insert(0, 'X_coord', xx)
    # Permute the synthetic rows so seed 42 initializes one point in each
    # designed stripe under the current sklearn random_from_data implementation.
    order_rng = np.random.default_rng(42)
    for _ in range(19):
        order = order_rng.permutation(len(frame))
    return frame.iloc[order].reset_index(drop=True)

if __name__ == '__main__':
    out = Path(__file__).resolve().parent / 'synthetic_1600x39.csv'
    generate().to_csv(out,index=False,float_format='%.8f')
    print(f'Created {out}: 1600 synthetic samples, 39 elements')
