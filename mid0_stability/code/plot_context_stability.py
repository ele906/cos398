#!/usr/bin/env python3
"""Create descriptive context-stability figures from saved CSVs only."""
from pathlib import Path
import argparse, hashlib, itertools, json, math, platform
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

GRID=[-100,-70,-50,-40,-30,-20,-15,-12,-10,-7,-5,-3,-2,-1,0,1,2,3,5,7,10,12,15,20,30,40,50,70,100]
COHORTS=['all','active','active_baseline_detected']
LABELS={'all':'All samples','active':'Initially active','active_baseline_detected':'Initially active; baseline detected'}
SELECTED=[-100,-70,-40,-20,1,20,40,70,100]
SHA='cbb3a0a2d0c43c822c7ba97a494de38ae56ea25401a8d31484ffa32e7cc329a6'


def wilson(k,n):
    if not n:return np.nan,np.nan
    z=1.959963984540054;p=k/n;den=1+z*z/n
    c=(p+z*z/(2*n))/den;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0,c-h),min(1,c+h)


def cohort_rows(d,c):
    if c=='all':return d
    return d[d.initially_active & (d.baseline_detected if c=='active_baseline_detected' else True)]


def save(fig,path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path.with_suffix('.png'),dpi=300,bbox_inches='tight',facecolor='white')
    fig.savefig(path.with_suffix('.pdf'),bbox_inches='tight',facecolor='white',metadata={'Creator':'Saved mid.0 stability CSV analysis'})
    data.to_csv(path.with_suffix('.csv'),index=False)
    plt.close(fig)


def alpha_axis(ax):
    ax.set_xscale('symlog',linthresh=3)
    ticks=[-100,-20,-5,0,1,5,20,100]
    ax.set_xticks(ticks,[str(a) for a in ticks]);ax.set_xlim(-110,110)
    ax.set_ylim(-.04,1.04);ax.set_yticks([0,.25,.5,.75,1])
    ax.axhline(.95,color='.55',lw=.7,ls='--',zorder=0)
    ax.axvline(1,color='.65',lw=.7,ls=':',zorder=0)
    ax.set_xlabel('Multiplier α (symmetric log axis; linear near zero)')
    ax.set_ylabel('Landmark detection rate');ax.grid(alpha=.15)


def line(ax,t,color,label):
    t=t.sort_values('alpha');valid=t.n>0
    x=t.alpha.to_numpy();y=t.detection_rate.to_numpy();lo=t.ci_low.to_numpy();hi=t.ci_high.to_numpy()
    ax.plot(x,y,color=color,lw=1.25,label=label)
    ax.fill_between(x,lo,hi,color=color,alpha=.045,linewidth=0)
    ax.errorbar(x[valid],y[valid],yerr=[np.maximum(0,y[valid]-lo[valid]),np.maximum(0,hi[valid]-y[valid])],fmt='none',ecolor=color,alpha=.22,lw=.5)
    low=valid & t.insufficient
    ax.scatter(x[low],y[low],marker='x',s=13,color=color,zorder=4)


def aggregate(d,features,groups,min_n):
    out=[]
    for c in COHORTS:
        eligible=cohort_rows(d,c)
        lookup={key:sub for key,sub in eligible.groupby(['feature','group','alpha'])}
        for f,g,a in itertools.product(features,groups,GRID):
            sub=lookup.get((f,g,float(a)))
            n=0 if sub is None else len(sub);k=0 if sub is None else int(sub.face_detected.sum())
            lo,hi=wilson(k,n)
            out.append(dict(feature=f,group=g,cohort=c,alpha=a,n=n,seed_count=0 if sub is None else sub.seed.nunique(),detected=k,
                detection_rate=k/n if n else np.nan,ci_low=lo,ci_high=hi,ci_width=hi-lo,insufficient=n<min_n,
                status='no_eligible_observations' if not n else ('insufficient_observations' if n<min_n else 'exploratory_sample'),
                median_delta_fro_applied=np.nan if not n else sub.delta_fro_applied.median(),
                median_relative_delta_fro=np.nan if not n else sub.relative_delta_fro.median()))
    return pd.DataFrame(out)


def crossings(t,threshold,min_n):
    out=[]
    for (f,g,c),sub in t.groupby(['feature','group','cohort']):
        values=sub.set_index('alpha');base=values.loc[1]
        for direction,aa in [('positive',[a for a in GRID if a>1]),('negative',sorted([a for a in GRID if a<0],reverse=True))]:
            previous=1;first=None;status='not_reached';recovery=False
            if base.n==0:status='no_eligible_observations'
            elif base.detection_rate<threshold:status='baseline_below_threshold'
            else:
                for a in aa:
                    r=values.loc[a]
                    if r.n==0:status='missing_observations';break
                    if r.detection_rate<threshold:first=a;status='sampled_crossing';break
                    previous=a
            rates=[values.loc[a].detection_rate for a in aa]
            recovery=any(y>x+1e-12 for x,y in zip(rates,rates[1:]) if np.isfinite(x) and np.isfinite(y))
            low=base.n<min_n or (first is not None and values.loc[first]['n']<min_n)
            if status=='sampled_crossing' and low:status='observed_crossing_insufficient_n'
            out.append(dict(feature=f,group=g,cohort=c,direction=direction,threshold=threshold,n=int(base.n),insufficient=low,
                last_passing_alpha=previous if status in ('sampled_crossing','observed_crossing_insufficient_n','not_reached') else np.nan,
                first_failing_alpha=first if first is not None else np.nan,status=status,nonmonotonic_recovery=recovery,
                last_passing_ci_low=values.loc[previous].ci_low if base.n else np.nan,
                last_passing_ci_high=values.loc[previous].ci_high if base.n else np.nan,
                first_failing_ci_low=values.loc[first].ci_low if first is not None else np.nan,
                first_failing_ci_high=values.loc[first].ci_high if first is not None else np.nan))
    return pd.DataFrame(out)


def heatmaps(t,b,features,groups,out):
    cmap=plt.get_cmap('viridis').copy();cmap.set_bad('#dedede')
    for a in SELECTED:
        data=t[t.alpha==a]
        fig,axes=plt.subplots(3,2,figsize=(18,15),layout='constrained')
        for row,c in enumerate(COHORTS):
            sub=data[data.cohort==c].set_index(['feature','group'])
            for col,(metric,title) in enumerate([('detection_rate','Landmark detection rate'),('ci_width','95% Wilson interval width')]):
                ax=axes[row,col];matrix=np.array([[sub.loc[(f,g),metric] for g in groups] for f in features])
                im=ax.imshow(matrix,vmin=0,vmax=1,cmap=cmap,aspect='auto')
                ax.set_xticks(range(len(groups)),[g.replace('_',' ') for g in groups],rotation=50,ha='right',fontsize=8)
                ax.set_yticks(range(len(features)),[str(f) for f in features]);ax.set_ylabel('Fine-tuned mid.0 SAE feature')
                ax.set_title(f'{LABELS[c]} — {title}',fontsize=11)
                for i,f in enumerate(features):
                    for j,g in enumerate(groups):
                        r=sub.loc[(f,g)];v=r[metric]
                        label='∅' if r.n==0 else (f'{v:.0%}\nn={int(r.n)}'+('†' if r.insufficient else '') if col==0 else f'{v:.2f}')
                        ax.text(j,i,label,ha='center',va='center',fontsize=6.6,color='white' if np.isfinite(v) and v<.45 else 'black')
                        if r.insufficient:ax.add_patch(Rectangle((j-.5,i-.5),1,1,fill=False,hatch='///',edgecolor=(.35,.35,.35,.4),lw=0))
                fig.colorbar(im,ax=ax,fraction=.025,pad=.02)
        fig.suptitle(f'Multiplier α={a}: feature × demographic prompt context\nCounts and pointwise 95% Wilson intervals; † insufficient observations; ∅ no eligible observations',fontsize=15)
        save(fig,out/'heatmaps'/f'alpha_{"m" if a<0 else "p"}{abs(a):03d}',data)
    for c in COHORTS:
        data=b[b.cohort==c];fig,axes=plt.subplots(1,2,figsize=(19,7),layout='constrained')
        for ax,direction in zip(axes,['negative','positive']):
            sub=data[data.direction==direction].set_index(['feature','group']);matrix=np.full((len(features),len(groups)),np.nan)
            for i,f in enumerate(features):
                for j,g in enumerate(groups):
                    r=sub.loc[(f,g)]
                    if np.isfinite(r.first_failing_alpha):matrix[i,j]=abs(r.first_failing_alpha)
            im=ax.imshow(matrix,cmap=cmap,vmin=0,vmax=100,aspect='auto')
            ax.set_xticks(range(len(groups)),[g.replace('_',' ') for g in groups],rotation=55,ha='right',fontsize=8)
            ax.set_yticks(range(len(features)),[str(f) for f in features]);ax.set_title(direction+' branch');ax.set_ylabel('SAE feature')
            for i,f in enumerate(features):
                for j,g in enumerate(groups):
                    r=sub.loc[(f,g)]
                    if np.isfinite(r.first_failing_alpha):text=f'{int(r.last_passing_alpha)}→{int(r.first_failing_alpha)}'
                    elif r.status=='not_reached':text='NR'
                    elif r.status=='baseline_below_threshold':text='B'
                    else:text='∅'
                    if r.insufficient:text+='†'
                    if r.nonmonotonic_recovery:text+='*'
                    ax.text(j,i,text,ha='center',va='center',fontsize=6.5,color='white' if np.isfinite(matrix[i,j]) and matrix[i,j]<45 else 'black')
                    if r.insufficient:ax.add_patch(Rectangle((j-.5,i-.5),1,1,fill=False,hatch='///',edgecolor=(.4,.4,.4,.4),lw=0))
            fig.colorbar(im,ax=ax,fraction=.025,label='|First failing sampled α| (not a continuous threshold)')
        fig.suptitle(f'{LABELS[c]}: sampled crossings below 95% detection\nNR: not reached; B: baseline below criterion; ∅: unavailable; †: low n; *: nonmonotonic recovery',fontsize=14)
        save(fig,out/'heatmaps'/f'crossing_brackets_{c}',data)


def curves(t,features,groups,out,gcolors,fcolors):
    for mode,identifiers,other,colors in [('feature',features,groups,gcolors),('category',groups,features,fcolors)]:
        for ident in identifiers:
            data=t[t.feature==ident] if mode=='feature' else t[t.group==ident]
            fig,axes=plt.subplots(3,1,figsize=(12,12),layout='constrained')
            for ax,c in zip(axes,COHORTS):
                sub=data[data.cohort==c]
                for item in other:
                    q=sub[sub.group==item] if mode=='feature' else sub[sub.feature==item]
                    ns=q.n.unique();ntext=str(ns[0]) if len(ns)==1 else f'{ns.min()}–{ns.max()}'
                    label=(item.replace('_',' ') if mode=='feature' else str(item))+f' (n={ntext})'
                    line(ax,q,colors[item],label)
                alpha_axis(ax);ax.set_title(LABELS[c],loc='left');ax.legend(loc='center left',bbox_to_anchor=(1.01,.5),fontsize=8,frameon=False)
            fig.suptitle(f'{"Feature "+str(ident) if mode=="feature" else str(ident).replace("_"," ").title()} — detection across saved multipliers\nPointwise 95% Wilson intervals; × marks n below minimum; missing cohorts stay unplotted',fontsize=13)
            save(fig,out/('per_feature' if mode=='feature' else 'per_category')/f'{mode}_{ident}',data)


def magnitudes(t,features,groups,out):
    # Aggregate each sampled alpha within its feature/group, never bin repeated observations together.
    for c in COHORTS:
        for metric,title in [('median_relative_delta_fro','Applied perturbation / original block norm'),('median_delta_fro_applied','Applied perturbation Frobenius norm')]:
            data=t[t.cohort==c].copy()
            data['branch']=np.select([data.alpha>1,data.alpha<0,data.alpha==1],['positive','negative','baseline'],default='attenuation_or_ablation')
            for f in features:
                sub=data[data.feature==f];fig,axes=plt.subplots(3,4,figsize=(16,10),layout='constrained')
                for ax,g in zip(axes.flat,groups):
                    q=sub[sub.group==g];n=int(q[q.alpha==1].n.iloc[0]);ax.set_title(g.replace('_',' ')+f' | n={n}'+(' †' if q.insufficient.any() else ''),fontsize=10)
                    for branch,color,style in [('negative','#2166ac','--'),('positive','#b2182b','-'),('attenuation_or_ablation','#777777',':')]:
                        v=q[(q.branch==branch)&(q.n>0)].sort_values(metric)
                        if v.empty:continue
                        x=v[metric].to_numpy();y=v.detection_rate.to_numpy();lo=v.ci_low.to_numpy();hi=v.ci_high.to_numpy()
                        ax.plot(x,y,style,color=color,lw=1.2,marker='o',ms=2.5)
                        ax.fill_between(x,lo,hi,color=color,alpha=.10,linewidth=0)
                        low=v.insufficient.to_numpy();ax.scatter(x[low],y[low],s=18,marker='x',color=color)
                    if n==0:ax.text(.5,.5,'No eligible observations',transform=ax.transAxes,ha='center',fontsize=8)
                    ax.set_xscale('symlog',linthresh=.1 if 'relative' in metric else 10);ax.set_xlim(0, max(float(t[metric].max())*1.05, .1 if 'relative' in metric else 10));ax.set_ylim(-.04,1.04);ax.axhline(.95,color='.6',ls='--',lw=.6);ax.grid(alpha=.15)
                    ax.set_ylabel('Landmark detection rate',fontsize=9);ax.set_xlabel(title,fontsize=8)
                handles=[Line2D([0],[0],color=color,ls=style,label=label) for label,color,style in [('Negative α (reversal)','#2166ac','--'),('α > 1 (amplification)','#b2182b','-'),('0 ≤ α < 1 (ablation/attenuation)','#777777',':')]]
                fig.legend(handles=handles,loc='outside lower center',ncol=3,frameon=False)
                fig.suptitle(f'Feature {f} | {LABELS[c]}\nEach point: median measured magnitude and detection rate at one saved α; shaded 95% Wilson intervals',fontsize=13)
                save(fig,out/'magnitude'/f'feature_{f}_{metric}_{c}',sub)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--output',type=Path)
    p.add_argument('--min-seeds',type=int,default=5,help='Exploratory flag threshold; not a power calculation')
    args=p.parse_args();src=args.source.resolve();out=args.output or src/'visualizations_v1'
    if out.exists():raise FileExistsError(f'Refusing to overwrite {out}')
    experiment=json.loads((src/'experiment.json').read_text());settings=json.loads((src/'settings.json').read_text())
    assert experiment['checkpoint_sha256']==SHA and experiment['layer']=='unet.mid_block.attentions.0'
    assert experiment['alphas']==GRID
    features=experiment['features'];seeds=experiment['seeds'];d=pd.read_csv(src/'per_image.csv');saved=pd.read_csv(src/'detection_summary.csv');bins=pd.read_csv(src/'coefficient_bins.csv')
    for col in ['face_detected','baseline_detected','initially_active']:
        if d[col].isna().any() or not set(d[col].unique())<={True,False}:raise ValueError(f'Invalid detection/filter flag {col}')
    if d.duplicated(['feature','group','seed','alpha']).any():raise ValueError('Duplicate image conditions')
    groups=sorted(d.group.unique());assert len(groups)==12 and set(d.feature)==set(features) and set(d.alpha)==set(GRID) and set(d.seed)==set(seeds)
    expected=set(itertools.product(features,groups,seeds,GRID));actual=set(map(tuple,d[['feature','group','seed','alpha']].to_numpy()))
    missing=expected-actual;unexpected=actual-expected
    if missing or unexpected:raise ValueError(f'Condition audit: {len(missing)} missing, {len(unexpected)} unexpected; no conditions silently dropped')
    if d[['delta_fro_applied','relative_delta_fro']].isna().any().any():raise ValueError('Missing measured perturbations; not imputed')
    for _,sub in d.groupby(['feature','group','seed']):
        if sub.initially_active.nunique()!=1 or sub.baseline_detected.nunique()!=1:raise ValueError('Changing cohort flag across alpha')
        if sub[sub.alpha==1].face_detected.iloc[0]!=sub.baseline_detected.iloc[0]:raise ValueError('Baseline flag mismatch')
    t=aggregate(d,features,groups,args.min_seeds)
    # Check every saved category-level aggregate against the reconstruction.
    q=saved[saved.group!='ALL'].merge(t,on=['feature','group','cohort','alpha'],suffixes=('_saved','_new'),validate='one_to_one')
    assert len(q)==len(saved[saved.group!='ALL'])
    for col in ['n','detected','detection_rate','ci_low','ci_high']:
        if not np.allclose(q[col+'_saved'],q[col+'_new'],atol=1e-12):raise ValueError('Saved summary disagreement: '+col)
    pooled_verified=0
    for row in saved[saved.group=='ALL'].itertuples():
        eligible=cohort_rows(d,row.cohort)
        sub=eligible[(eligible.feature==row.feature)&(eligible.alpha==row.alpha)]
        n=len(sub);k=int(sub.face_detected.sum());lo,hi=wilson(k,n)
        if n!=row.n or k!=row.detected or not np.allclose([k/n,lo,hi],[row.detection_rate,row.ci_low,row.ci_high],atol=1e-12):
            raise ValueError('Saved pooled summary disagreement')
        pooled_verified+=1
    # Verify the old coefficient bins without reusing them as perturbation magnitudes.
    for r in bins.itertuples():
        sub=cohort_rows(d,'active_baseline_detected');sub=sub[(sub.feature==r.feature)&(sub.alpha>1 if r.direction=='positive' else sub.alpha<0)]
        sub=sub[(sub.scaled_abs_active_p95>=r.bin_low)&(sub.scaled_abs_active_p95<r.bin_high)]
        assert len(sub)==r.n and int(sub.face_detected.sum())==r.detected
    out.mkdir(parents=True);b=crossings(t,settings['detection_threshold'],args.min_seeds)
    t.to_csv(out/'aggregated_detection.csv',index=False);b.to_csv(out/'sampled_crossing_brackets.csv',index=False)
    t[t.insufficient].to_csv(out/'insufficient_observations.csv',index=False)
    hashes={name:hashlib.sha256((src/name).read_bytes()).hexdigest() for name in ['per_image.csv','detection_summary.csv','coefficient_bins.csv','experiment.json','settings.json']}
    audit=dict(input_hashes=hashes,checkpoint_sha256=SHA,expected_conditions=len(expected),observed_conditions=len(d),failed_detections=int((~d.face_detected).sum()),missing_conditions=0,unexpected_conditions=0,seeds=seeds,features=features,grid=GRID,selected_heatmap_alphas=SELECTED,min_seeds=args.min_seeds,insufficient_cells=int(t.insufficient.sum()),empty_cells=int((t.n==0).sum()),saved_category_summary_rows_verified=len(q),saved_pooled_summary_rows_verified=pooled_verified,coefficient_bins_verified=len(bins),versions=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,matplotlib=matplotlib.__version__))
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
    gc={g:plt.get_cmap('tab20')(i) for i,g in enumerate(groups)};fc={f:plt.get_cmap('tab10')(i) for i,f in enumerate(features)}
    print('Audit passed; creating heatmaps',flush=True);heatmaps(t,b,features,groups,out)
    print('Creating per-feature and per-category curves',flush=True);curves(t,features,groups,out,gc,fc)
    print('Creating feature/group perturbation panels',flush=True);magnitudes(t,features,groups,out)
    files=sorted(out.rglob('*.png'))
    readme=f'''# Fine-tuned mid.0 context-stability visualizations

Generated exclusively from the saved CSVs in `{src.name}`; no images generated, diffusion replayed, detector run, or old-environment sweeps pooled. Checkpoint SHA-256: `{SHA}`. All {len(d):,} saved conditions are accounted for; {audit['failed_detections']} failed detections remain in their denominators. Missing or duplicate conditions and missing detection flags cause an explicit error, rather than an inferred value or silent exclusion. Full audit: [audit.json](audit.json).

## Cohorts and uncertainty

- **all**: every saved condition.
- **active**: initially_active is True.
- **active baseline detected**: initially_active AND baseline_detected are True.

Each feature–group–alpha point reports n independent seeds, k detections, k/n, and a pointwise 95% Wilson interval, exactly matching the existing category-level summary. These intervals are descriptive; they are not simultaneous bounds or a repeated-measures hypothesis test. No independence is claimed between alphas/features or prompt groups sharing a noise seed. Saved pooled ALL rows are also audited against the CSV; they are not plotted here.

The default insufficient-observation flag is n < {args.min_seeds}, an explicit exploratory display rule rather than a power calculation. Low-n data remain displayed with †/× or hatching; n=0 has a missing rate/interval and ∅. Even n=5 with 5/5 detections has a wide interval and does not establish 95% population validity. With only {len(seeds)} seed values, interaction-model and demographic-vulnerability claims are unsupported by these figures alone.

## Figures

Each of the {len(files)} figures has a PNG at 300 dpi, a vector PDF with embedded fonts, and a same-stem CSV containing its aggregated plotting data (including n, k, confidence limits, and low-n flags).

1. **heatmaps/alpha_*.png**: rows are the ten fixed feature IDs in rank order, columns are twelve demographic prompt groups. Selected saved alphas: {SELECTED}. For each cohort, paired panels show detection rate and Wilson interval width, both with fixed 0–1 color scales. Rate cells print percentage and n. Grey missing cells are not zeros.
2. **heatmaps/crossing_brackets_*.png**: separate negative reversal and positive amplification branches, per cohort. Cells print last passing → first failing sampled alpha under the saved exploratory 0.95 detection criterion. NR means not reached, B means baseline already below criterion, ∅ unavailable, † low n, and * any nonmonotonic recovery. Low-n observed brackets are explicitly flagged, not established boundaries. No continuous interpolation or precise threshold is estimated. Alpha=0 ablation and 0<alpha<1 attenuation are excluded from these branch crossings, matching the old code. Confidence intervals for both bracket endpoints are in the figure CSVs.
3. **per_feature/**: ten figures, one per feature, with three cohort panels and twelve consistently colored prompt-group curves. Legends report n. Error bars and translucent bands show Wilson intervals. Symmetric-log alpha axes retain every saved grid point, including 0 and no-op 1; lines only connect sampled observations.
4. **per_category/**: twelve figures, one per prompt group, with the same cohort panels and ten consistently colored feature curves. Every plot uses identical alpha and detection axes.
5. **magnitude/**: for each feature, cohort, and measured metric, twelve prompt-group panels show median magnitude versus detection rate at each sampled alpha. The relative metric is the saved applied perturbation norm divided by original block norm; the absolute metric is saved delta_fro_applied. Negative reversal, positive amplification, and attenuation/ablation use consistent branch colors/styles. The alpha=1 baseline is present in the CSV but excluded from magnitude branch curves. Symmetric-log magnitude axes include zero and share the same metric-specific limits across all features, prompt groups, and cohorts. No magnitude bins, smoothers, or pooled repeated-image denominators are used. Magnitude medians summarize different seeds at the same alpha; they do not match individual magnitudes or control for confounding. Wilson bands quantify detection uncertainty, not uncertainty in median magnitude.

The original coefficient_bins.csv describes scaled coefficients, not actual perturbation norms. Its counts were audited against per_image.csv; it is not relabeled as a perturbation measurement.

## Data and reproducibility

[Aggregated detection data](aggregated_detection.csv), [crossing brackets](sampled_crossing_brackets.csv), and [insufficient-observation cells](insufficient_observations.csv) retain all cohorts, groups, and saved multipliers. Input hashes and dependency versions are in audit.json. Source script: ../code/plot_context_stability.py. Run:

```bash
python code/plot_context_stability.py --source . --output visualizations_v2
```

Existing output directories are refused. Existing report files are untouched. Exact multiplier grid: `{GRID}`. The source experiment configuration preserves the checkpoint and feature IDs. MediaPipe landmark detection is not facial quality; prompt groups are prompt conditions, not inferred demographic identities. Human validation remains necessary.

## Gallery

'''
    for section in ['heatmaps','per_feature','per_category','magnitude']:
        readme+=f'### {section}\n\n'
        for path in files:
            if path.parent.name==section:
                rel=path.relative_to(out);readme+=f'- [{path.stem}]({rel}) · [PDF]({rel.with_suffix(".pdf")}) · [data]({rel.with_suffix(".csv")})\n'
        readme+='\n'
    (out/'README.md').write_text(readme)
    print(f'Completed {len(files)} figures: {out}',flush=True)

if __name__=='__main__':main()
