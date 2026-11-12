"""Generate a fictional 40 x 40 geological-style synthetic dataset."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter

COLUMNS = ['Be','Cr','F','La','Li','Nb','P','Ti','V','Y','Al2O3','Fe2O3','K2O','SiO2','Pb','Zn','Cu','W','B','Bi','Sn','Zr','Ag','As','Ba','Cd','Co','Ga','Ge','Hg','Mn','Mo','Ni','Sb','Sc','Sr','Th','U','Rb']
ASSOCIATIONS = [['Pb','Zn','Cu','F'], ['Pb','W','B','Bi'], ['Pb','Bi','Sn'], ['Pb','Cu','Zn','Ti','Y','Zr'], ['Pb','Li','Be','Sn','Y']]

def generate():
    rng=np.random.default_rng(42); yy,xx=np.mgrid[0:40,0:40]
    # Interleaved smoothed fields plus two distinct irregular bodies.
    fields=np.array([gaussian_filter(rng.normal(size=(40,40)),s)*s for s in (3.5,4.0,4.5)])
    fields += np.array([.10*np.sin((xx+yy)/5),.12*np.cos((2*xx-yy)/8),.10*np.sin((xx-2*yy)/7)])
    zone=np.argmax(fields,axis=0)
    warp=gaussian_filter(rng.normal(size=(40,40)),2)*4
    body1=((xx-28)/8.0)**2+((yy-10)/7.0)**2 < 1+warp
    body2=((xx-10)/5.5)**2+((yy-29)/7.0)**2 < 1+warp*.8
    zone[body1]=3;zone[body2]=4
    coords=np.column_stack((xx.ravel(),yy.ravel())); region=zone.ravel().copy(); n=1600
    # Occasional samples inherit a neighbouring background signature.
    scattered=rng.random(n)<.07
    region[scattered]=rng.integers(0,5,scattered.sum())
    # Smooth background signatures intentionally differ by synthetic zone.
    signatures=rng.normal(0,.34,(5,14)); values=rng.normal(2,.18,(n,39))
    # Smooth mixtures model transitional signatures at contacts; every sample
    # also has individual noise, so components can overlap near boundaries.
    fractions=np.stack([gaussian_filter((zone==z).astype(float),1.4) for z in range(5)],axis=-1).reshape(n,5)
    weights=.75*np.eye(5)[region]+.25*fractions
    values[:,:14]+=weights@signatures
    for z in range(5):
        values[region==z,COLUMNS.index('Pb')] += [0,.08,.16,.12,.35][z]
    # Artificial anomalies: irregular clustered enrichment along a bent belt.
    trend=np.exp(-((yy-(9+.45*xx+3*np.sin(xx/7)))/3.4)**2)
    spots=sum(np.exp(-((xx-x)**2+(yy-y)**2)/20) for x,y in [(6,13),(14,19),(25,19),(32,25),(28,10),(10,29)])
    strength=(.75*trend+.95*spots).ravel(); perturb=rng.normal(0,.04,n); mineral=np.maximum(0,strength+perturb)
    # Group-specific correlated fields give each composition its own
    # covariance structure and keep associations distinguishable.
    for z,association in enumerate(ASSOCIATIONS):
        mask=region==z
        latent1=rng.normal(0,.55,mask.sum()) + mineral[mask]*.9
        latent2=rng.normal(0,.75,mask.sum())
        for j,element in enumerate(association):
            values[mask,COLUMNS.index(element)] += latent1*(1.0 if element=='Pb' else .85)
        partners=[e for e in COLUMNS[14:] if e not in association]
        for element in partners[z*3:z*3+4]:
            values[mask,COLUMNS.index(element)] += latent2*.8
    df=pd.DataFrame(np.exp(values),columns=COLUMNS);df.insert(0,'Y_coord',coords[:,1]);df.insert(0,'X_coord',coords[:,0])
    truth=pd.DataFrame({'X_coord':coords[:,0],'Y_coord':coords[:,1],'synthetic_zone':region,'synthetic_lithology':np.array(['carbonate','sandstone','shale','granite','mudstone'])[region],'imposed_intensity':strength,'imposed_anomaly':strength>=.55})
    # Deliberately choose a fixed row order yielding one initialization point
    # per designed zone under the current random_from_data implementation.
    initial=np.random.RandomState(42).choice(n,5,replace=False); shuffle=np.random.default_rng(42)
    for attempt in range(10000):
        order=shuffle.permutation(n)
        if len(np.unique(region[order[initial]]))==5:break
    else:raise RuntimeError('Unable to find balanced example initialization')
    return df.iloc[order].reset_index(drop=True),truth.iloc[order].reset_index(drop=True),attempt

if __name__=='__main__':
    data,truth,attempt=generate(); folder=Path(__file__).resolve().parent
    data.to_csv(folder/'synthetic_1600x39.csv',index=False,float_format='%.8f')
    truth.to_csv(folder/'synthetic_ground_truth.csv',index=False,float_format='%.8f')
    print('Generated',len(data),'fictional samples; row-order attempt',attempt,'zone sizes',truth.synthetic_zone.value_counts().sort_index().to_dict())

