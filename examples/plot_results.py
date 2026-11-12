"""Create manuscript-inspired figures for the fictional case only."""
from pathlib import Path
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'results_irregular'
d=pd.read_csv(ROOT/'examples/synthetic_1600x39.csv');r=pd.read_csv(out/'sample_comparison.csv');load=pd.read_csv(out/'rpca_loadings.csv');summ=pd.read_csv(out/'model_summary.csv');
plt.rcParams.update({'font.family':'serif','font.size':9,'axes.linewidth':.8})
fig,axes=plt.subplots(1,2,figsize=(9,4.4),constrained_layout=True)
x=d.X_coord.to_numpy();y=d.Y_coord.to_numpy();im=axes[0].scatter(x,y,c=d.Pb,s=10,marker='s',cmap='YlOrRd',linewidths=0);fig.colorbar(im,ax=axes[0],label='Synthetic Pb (arbitrary units)',shrink=.75)
colors=['#225ea8','#e41a1c','#ffdf26','#6cae3c','#77cdd2']; cmap=ListedColormap(colors);im2=axes[1].scatter(x,y,c=r.cluster,s=10,marker='s',cmap=cmap,vmin=-.5,vmax=4.5,linewidths=0)
axes[1].legend(handles=[Line2D([0],[0],marker='s',linestyle='',color=colors[i],label=f'Cluster {i+1}') for i in range(5)],loc='lower left',fontsize=7,frameon=True)
for a,lab in zip(axes,['(a) Simulated Pb','(b) EM clusters']):a.set(title=lab,xlabel='Synthetic X (grid index)',ylabel='Synthetic Y (grid index)',xlim=(-1,40),ylim=(-1,40),aspect='equal')
fig.suptitle('Synthetic data only — no geographic coordinates',fontsize=10);fig.savefig(out/'figure_em.png',dpi=300);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(10,7),constrained_layout=True);levels=['background','weak','moderate','strong']; color=['#dddddd','#f3df32','#ed8b24','#c51b2c']
for i,ax in enumerate(axes.flat):
 subset=r if i==5 else r[r.cluster==i];col='regional_level' if i==5 else 'clustered_level'
 ax.scatter(subset.X_coord,subset.Y_coord,s=5,c='#d3d3d3',marker='s',linewidths=0)
 for j in range(1,4):
  q=subset[subset[col]==j];ax.scatter(q.X_coord,q.Y_coord,s=8,c=color[j],marker='s',linewidths=0)
 ax.set(xlim=(-1,40),ylim=(-1,40),aspect='equal',xlabel='Synthetic X',ylabel='Synthetic Y',title=f'({chr(97+i)}) '+('Whole-region model' if i==5 else f'EM cluster {i+1}'))
fig.legend(handles=[Line2D([0],[0],marker='s',linestyle='',color=color[j],label=levels[j]) for j in range(1,4)],loc='outside lower center',ncol=3,frameon=False);fig.suptitle('Synthetic anomaly maps — clustered vs whole-region',fontsize=10);fig.savefig(out/'figure_anomalies.png',dpi=300);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(10,7),constrained_layout=True)
for i,ax in enumerate(axes.flat):
 key=str(i) if i<5 else 'regional';v=load[load.model.astype(str)==key];sel=v[v.selected];ax.axhline(0,c='0.5',lw=.5);ax.axvline(0,c='0.5',lw=.5)
 for _,row in v.iterrows():
  c='crimson' if row.element=='Pb' else ('#1f5e92' if row.selected else '#aaaaaa'); ax.arrow(0,0,row.PC1,row.PC2,color=c,width=.0015,length_includes_head=True,head_width=.015,alpha=.9)
  if row.selected:ax.text(row.PC1,row.PC2,row.element,fontsize=7,color=c)
 ax.set_aspect('equal',adjustable='datalim');ax.set_title(f'({chr(97+i)}) '+('Whole region' if i==5 else f'Cluster {i+1}'));ax.set_xlabel('PC1 CLR loading');ax.set_ylabel('PC2 CLR loading')
fig.suptitle('Synthetic RPCA loadings; selected elements labeled',fontsize=10);fig.savefig(out/'figure_rpca.png',dpi=300);plt.close(fig)
print('Wrote three synthetic figure panels')
