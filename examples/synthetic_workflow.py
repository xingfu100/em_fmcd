"""Run EM K=5, cluster-wise ILR-MCD RPCA and FMCD on fictional data."""
import importlib.util, os, sys
from pathlib import Path
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name] = '1'
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'examples' / 'synthetic_1600x39.csv'
INDICATORS = ['Be','Cr','F','La','Li','Nb','P','Ti','V','Y','Al2O3','Fe2O3','K2O','SiO2']

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'src' / file)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def run(out):
    em=load('em','01_em_aic.py'); rpca=load('rpca','02_robust_pca.py'); fmcd=load('fmcd','03_fmcd.py')
    df=pd.read_csv(DATA); cols=list(df.columns[2:]); raw=df[cols].to_numpy(float)
    assert raw.shape == (1600,39) and np.isfinite(raw).all() and (raw>0).all()
    clr=np.log(raw)-np.log(raw).mean(axis=1,keepdims=True); clr_df=pd.DataFrame(clr,columns=cols)
    model,trials=em.fit_best_gmm_by_seeds(clr_df[INDICATORS].to_numpy(),5,[42]); labels=model.predict(clr_df[INDICATORS].to_numpy())
    assert np.unique(labels).size == 5
    out.mkdir(parents=True,exist_ok=True)
    trials.to_csv(out/'gmm_trials.csv',index=False,encoding='utf-8-sig')
    pd.concat([df.iloc[:,:2],clr_df],axis=1).to_csv(out/'synthetic_clr.csv',index=False)
    rows=[]; summaries=[]; loadings=[]
    for group in range(5):
        mask=labels==group; pc=rpca.运行ILR_MCD_RPCA(raw[mask],cols,0.5,42)
        loadmat=np.asarray(pc['clr_loadings_all'])[:,:2]; anchor=loadmat[cols.index('Pb')]; norm=np.linalg.norm(loadmat,axis=1); anchor_norm=np.linalg.norm(anchor)
        if anchor_norm < 1e-12: raise ValueError('Pb has negligible PC1/PC2 loading; no directional association can be selected')
        cosine=np.divide(loadmat@anchor,norm*anchor_norm,out=np.full(len(cols),-1.0),where=norm>1e-12)
        # Heuristic ranks same-direction PC1/PC2 loadings; it is not a correlation coefficient.
        candidates=[i for i in range(len(cols)) if cols[i]!='Pb' and cosine[i]>0]
        candidates.sort(key=lambda i: float(cosine[i]*norm[i]), reverse=True)
        eligible=[i for i in candidates if cosine[i]>=0.8]
        chosen=eligible[:5] if len(eligible)>=2 else candidates[:2]
        if len(chosen)<2: raise ValueError('Fewer than two same-direction candidates')
        selected=['Pb']+[cols[i] for i in chosen]; matrix=clr_df.loc[mask,selected].to_numpy()
        result=fmcd.fast_mcd(matrix,seed=42); d=result['final_md2']; cutoff=fmcd.chi2_ppf(.975,len(selected))
        assert np.isfinite(d).all() and (d>=0).all() and pc['clr_reconstruction_error']<1e-10
        for i,col in enumerate(cols): loadings.append({'cluster':group,'element':col,'PC1':loadmat[i,0],'PC2':loadmat[i,1],'cosine_with_Pb':cosine[i],'selected':col in selected})
        for index,value in zip(np.flatnonzero(mask),d): rows.append({'row_id':int(index),'X_coord':int(df.iloc[index,0]),'Y_coord':int(df.iloc[index,1]),'cluster':group,'MD2':float(value),'threshold':float(cutoff),'anomaly_index':float(value/cutoff),'anomaly':int(value>cutoff)})
        summaries.append({'cluster':group,'n':int(mask.sum()),'association':'+'.join(selected),'n_elements':len(selected),'PC1_fraction':float(pc['explained_ratio'][0]),'PC2_fraction':float(pc['explained_ratio'][1]),'threshold':float(cutoff),'anomalies':int((d>cutoff).sum())})
    pd.DataFrame(summaries).to_csv(out/'cluster_summary.csv',index=False)
    pd.DataFrame(loadings).to_csv(out/'rpca_pc1_pc2_loadings.csv',index=False)
    pd.DataFrame(rows).sort_values('row_id').to_csv(out/'sample_results.csv',index=False)
    print(pd.DataFrame(summaries).to_string(index=False));print('PASS: 1600 samples, K=5, RPCA and cluster FMCD completed')

if __name__=='__main__': run(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'example_output')
