#!/usr/bin/env python3
"""Evaluate saved mid.0 interventions; detection is not a facial-quality judgment."""
from pathlib import Path
import argparse, csv, hashlib, json, math, sys, time
from collections import defaultdict
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUNS = ROOT / 'layers/runs/mid0_sae_face_001/interventions/global_seed_average_001'


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def wilson(k, n):
    if not n:
        return None, None
    z = 1.959963984540054
    p = k/n; den = 1+z*z/n
    c = (p+z*z/(2*n))/den
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return c-h, c+h


def slug(alpha):
    return ('m' if alpha < 0 else 'p') + f'{abs(alpha):g}'


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        for group in ('ALL', r['group']):
            for cohort in ('all', 'active', 'active_baseline_detected'):
                if cohort != 'all' and not r['initially_active']:
                    continue
                if cohort == 'active_baseline_detected' and not r['baseline_detected']:
                    continue
                groups[(r['feature'], group, cohort, r['alpha'])].append(r)
    out = []
    for (feat, group, cohort, alpha), subset in sorted(groups.items()):
        n = len(subset); k = sum(r['face_detected'] for r in subset)
        lo, hi = wilson(k,n)
        out.append(dict(feature=feat, group=group, cohort=cohort, alpha=alpha,
            n=n, detected=k, detection_rate=k/n, ci_low=lo, ci_high=hi,
            mean_abs_scaled_coefficient=np.mean([r['scaled_abs_mean'] for r in subset]),
            median_abs_scaled_active_p95=np.median([r['scaled_abs_active_p95'] for r in subset]),
            mean_delta_fro=np.mean([r['delta_fro'] for r in subset])))
    return out


def boundaries(summary, threshold):
    grouped=defaultdict(dict)
    for r in summary:
        if r['group']=='ALL' and r['cohort']=='active_baseline_detected':
            grouped[r['feature']][r['alpha']]=r
    out=[]
    for feature, values in sorted(grouped.items()):
        for direction in ('positive_amplification','negative_reversal'):
            alphas=sorted((a for a in values if a>1),key=lambda a:a-1) if direction.startswith('positive') else sorted((a for a in values if a<0),key=lambda a:1-a)
            previous=1; first=None
            for a in alphas:
                if values[a]['detection_rate']<threshold:
                    first=a;break
                previous=a
            rates=[values[a]['detection_rate'] for a in alphas]
            out.append(dict(feature=feature,direction=direction,detection_threshold=threshold,
                last_passing_sample_before_first_failure=previous,
                first_failing_sample='' if first is None else first,
                status='not_reached_in_saved_sweep' if first is None else 'sampled_crossing',
                nonmonotonic_recovery=any(b>a for a,b in zip(rates,rates[1:])),
                interpretation='Observed grid crossing; not an exact or validated quality cliff'))
    return out


def plots(summary, rows, output):
    features=sorted({r['feature'] for r in rows})
    fig,axes=plt.subplots(1,3,figsize=(16,4.5))
    for ax,cohort in zip(axes,('all','active','active_baseline_detected')):
        for feat in features:
            s=sorted([r for r in summary if r['feature']==feat and r['group']=='ALL' and r['cohort']==cohort],key=lambda r:r['alpha'])
            if not s:continue
            x=np.array([r['alpha'] for r in s]); y=np.array([r['detection_rate'] for r in s])
            ax.errorbar(x,y,yerr=[np.maximum(0, y-np.array([r['ci_low'] for r in s])),np.maximum(0, np.array([r['ci_high'] for r in s])-y)],marker='o',capsize=2,label=str(feat))
        ax.set(title=cohort.replace('_',' '),xlabel='Multiplier alpha',ylabel='Landmark detection rate',ylim=(-.03,1.04))
        ax.axvline(1,color='gray',ls=':');ax.axhline(.95,color='gray',ls='--',lw=.7);ax.legend(title='mid.0 feature');ax.grid(alpha=.2)
    fig.suptitle('MediaPipe landmark detection (95% Wilson intervals; not facial quality)')
    fig.tight_layout();fig.savefig(output/'detection_curves.png',dpi=180);plt.close(fig)
    # Predeclared common bins, separately for each intervention direction.
    bins=np.array([0,25,50,100,150,200,300,400,600,1000,np.inf])
    binned=[]
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,direction in zip(axes,('positive','negative')):
        for feat in features:
            eligible=[r for r in rows if r['feature']==feat and r['initially_active'] and r['baseline_detected'] and (r['alpha']>1 if direction=='positive' else r['alpha']<0)]
            xs=[];ys=[]
            for l,h in zip(bins[:-1],bins[1:]):
                sub=[r for r in eligible if l<=r['scaled_abs_active_p95']<h]
                if not sub:continue
                k=sum(r['face_detected'] for r in sub);n=len(sub)
                xs.append(float(np.median([r['scaled_abs_active_p95'] for r in sub])));ys.append(k/n)
                binned.append(dict(feature=feat,direction=direction,bin_low=l,bin_high=h,n=n,detected=k,detection_rate=k/n))
            ax.plot(xs,ys,'o-',label=str(feat))
        ax.set(title=direction,xlabel='Per-image |alpha z|, p95 over initially active cells',ylabel='Landmark detection rate',ylim=(-.03,1.04));ax.grid(alpha=.2);ax.legend()
    fig.suptitle('Exploratory coefficient association; repeated images share prompt/seed')
    fig.tight_layout();fig.savefig(output/'coefficient_detection.png',dpi=180);plt.close(fig)
    write_csv(output/'coefficient_bins.csv',binned)


def review_sheets(rows, output):
    candidates=[]
    grouped=defaultdict(list)
    for r in rows:
        if r['initially_active'] and r['baseline_detected']:
            grouped[(r['feature'],r['group'],r['seed'])].append(r)
    for key,sub in sorted(grouped.items()):
        for direction in ('positive','negative'):
            ordered=sorted([r for r in sub if r['alpha']>1] if direction=='positive' else [r for r in sub if r['alpha']<0],key=lambda r:abs(r['alpha']-1))
            failure=next((i for i,r in enumerate(ordered) if not r['face_detected']),None)
            if failure is not None:
                selected=[next(r for r in sub if r['alpha']==1)]
                selected+=ordered[max(0,failure-1):failure+2]
                candidates.append((key,direction,selected))
    # Add baseline/strongest-strength audit cases even if detector never fails.
    for key,sub in sorted(grouped.items()):
        baseline=next((r for r in sub if r['alpha']==1),None)
        if baseline is None:continue
        for direction in ('positive','negative'):
            ordered=sorted([r for r in sub if r['alpha']>1] if direction=='positive' else [r for r in sub if r['alpha']<0],key=lambda r:abs(r['alpha']-1))
            if ordered and not any(c[0]==key and c[1]==direction for c in candidates):
                candidates.append((key,direction,[baseline]+ordered[-2:]))
    # Balanced cap per feature, spread across prompt groups.
    chosen=[]
    for feat in sorted({r['feature'] for r in rows}):
        per_group=defaultdict(list)
        for c in candidates:
            if c[0][0]==feat:per_group[c[0][1]].append(c)
        for i in range(2):
            for group,items in sorted(per_group.items()):
                if i<len(items):chosen.append(items[i])
    review=[]; folder=output/'review';folder.mkdir(exist_ok=True)
    for index,(key,direction,sub) in enumerate(chosen):
        sheet=Image.new('RGB',(256*len(sub),290),'white');draw=ImageDraw.Draw(sheet)
        for j,r in enumerate(sub):
            with Image.open(r['image']) as im:
                tile=im.convert('RGB');tile.thumbnail((256,256));sheet.paste(tile,(256*j,34))
            draw.text((256*j+5,4),f"alpha {r['alpha']:g}; detected {int(r['face_detected'])}",fill='black')
            review.append(dict(review_id=f'{index:03d}_{j}',feature=r['feature'],group=r['group'],seed=r['seed'],alpha=r['alpha'],image=r['image'],detected=r['face_detected'],human_label='',notes=''))
        sheet.save(folder/f'{index:03d}_feature{key[0]}_{key[1]}_seed{key[2]}_{direction}.jpg')
    write_csv(output/'human_review.csv',review)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runs',type=Path,default=DEFAULT_RUNS)
    p.add_argument('--features',nargs='+',type=int,default=[1650,2023,4228])
    p.add_argument('--output',type=Path,default=ROOT/'layers/mid0_stability/results')
    p.add_argument('--limit-seeds-per-group',type=int)
    p.add_argument('--detection-threshold',type=float,default=.95)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    sys.path.append(str(ROOT/'face-landmarker/.deps'))
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    model=ROOT/'face-landmarker/models/face_landmarker.task'
    model_hash=hashlib.sha256(model.read_bytes()).hexdigest()
    options=vision.FaceLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=str(model)),num_faces=1,min_face_detection_confidence=.5,min_face_presence_confidence=.5,min_tracking_confidence=.5)
    config=dict(layer='unet.mid_block.attentions.0',features=args.features,mediapipe_version=mp.__version__,model_sha256=model_hash,detector='MediaPipe FaceLandmarker IMAGE, num_faces=1',min_face_detection_confidence=.5,min_face_presence_confidence=.5,min_tracking_confidence=.5,limit_seeds_per_group=args.limit_seeds_per_group,detection_threshold=args.detection_threshold)
    (args.output/'settings.json').write_text(json.dumps(config,indent=2)+'\n')
    cachefile=args.output/'detection_cache.jsonl';cache={}
    if cachefile.exists():
        for line in cachefile.read_text().splitlines():
            if line.strip():
                c=json.loads(line);cache[c['key']]=c['detected']
    norms_path=Path(__file__).with_name('decoder_norms.json')
    norms=json.loads(norms_path.read_text()) if norms_path.exists() else {}
    rows=[];start=time.time();counter=0
    with vision.FaceLandmarker.create_from_options(options) as detector, cachefile.open('a',buffering=1) as cf:
        def detect(path):
            nonlocal counter
            data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
            key=f'{model_hash}:{mp.__version__}:0.5:0.5:1:{digest}'
            if key not in cache:
                im=np.array(Image.open(path).convert('RGB'))
                result=detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=im))
                cache[key]=bool(result.face_landmarks)
                cf.write(json.dumps(dict(key=key,detected=cache[key]))+'\n')
            counter+=1
            if counter%500==0:print(f'Processed {counter} image lookups in {time.time()-start:.0f}s',flush=True)
            return cache[key],digest
        for feat in args.features:
            run=args.runs/f'feature_{feat}';settings=json.loads((run/'settings.json').read_text())
            if settings['block']!='unet.mid_block.attentions.0' or settings.get('face_box_mask'):
                raise ValueError(f'{run}: requires unmasked mid.0 intervention')
            maps=np.load(run/'activation_maps.npz');key_index={str(k):i for i,k in enumerate(maps['map_keys'])}
            pre=maps['pre_maps'];metrics=list(csv.DictReader((run/'metrics.csv').open()))
            seeds=defaultdict(set)
            for r in metrics:seeds[r['group']].add(int(r['seed']))
            selected={g:set(sorted(s)[:args.limit_seeds_per_group] if args.limit_seeds_per_group else sorted(s)) for g,s in seeds.items()}
            references={}
            for group,ss in selected.items():
                for seed in sorted(ss):
                    ref=run/'images'/group/f'seed{seed:03d}_alpha_p1.png'
                    baseline=run/'images'/group/'baseline'/f'seed{seed:03d}.png'
                    detected,digest=detect(ref)
                    if baseline.exists():
                        with Image.open(ref) as a,Image.open(baseline) as b:
                            mae=float(np.mean(np.abs(np.array(a,dtype=float)-np.array(b,dtype=float))))
                    else:mae=None
                    references[(group,seed)]=(detected,digest,mae)
            for m in metrics:
                group=m['group'];seed=int(m['seed']);alpha=float(m['alpha'])
                if seed not in selected[group]:continue
                z=pre[key_index[f'{group}|{seed}']];active=z[z>0];is_active=bool(active.size)
                path=run/'images'/group/f'seed{seed:03d}_alpha_{slug(alpha)}.png'
                detected,digest=detect(path);base,bdigest,mae=references[(group,seed)]
                norm=norms.get(str(feat));delta_coeff=abs(alpha-1)*float(np.linalg.norm(z))
                rows.append(dict(feature=feat,group=group,seed=seed,alpha=alpha,image=str(path),image_sha256=digest,
                    face_detected=detected,baseline_detected=base,initially_active=is_active,
                    active_fraction=float(np.mean(z>0)),scaled_abs_mean=abs(alpha)*float(z.mean()),
                    scaled_abs_active_p95=abs(alpha)*float(np.percentile(active,95)) if is_active else 0.,
                    scaled_abs_max=abs(alpha)*float(z.max()),coefficient_delta_l2=delta_coeff,
                    decoder_norm=norm,delta_fro=delta_coeff*norm if norm is not None else float('nan'),
                    relative_delta_fro=m.get('relative_delta_block_fro',''),
                    relative_delta_residual_fro=m.get('relative_delta_residual_fro',''),
                    delta_fro_applied=m.get('delta_fro_applied',''),baseline_mae=mae,equals_alpha1_pixels=digest==bdigest,
                    alpha1_reference_sha256=bdigest))
            print(f'Finished feature {feat}: {len(rows)} cumulative rows',flush=True)
    write_csv(args.output/'per_image.csv',rows)
    summary=summarize(rows);write_csv(args.output/'detection_summary.csv',summary)
    crossing=boundaries(summary,args.detection_threshold);write_csv(args.output/'sampled_boundaries.csv',crossing)
    plots(summary,rows,args.output);review_sheets(rows,args.output)
    # Cluster resample by seed, preserving all prompt groups and alphas for that seed.
    rng=np.random.default_rng(20261114);ci=[]
    for feat in args.features:
        for alpha in sorted({r['alpha'] for r in rows if r['feature']==feat}):
            sub=[r for r in rows if r['feature']==feat and r['alpha']==alpha and r['initially_active'] and r['baseline_detected']]
            cluster=defaultdict(list)
            for r in sub:cluster[r['seed']].append(int(r['face_detected']))
            if not cluster:continue
            values=list(cluster.values());success=np.array([sum(v) for v in values]);counts=np.array([len(v) for v in values])
            ix=rng.integers(0,len(values),size=(2000,len(values)));boot=success[ix].sum(1)/counts[ix].sum(1)
            lo,hi=np.quantile(boot,[.025,.975])
            ci.append(dict(feature=feat,alpha=alpha,n=len(sub),seed_clusters=len(values),detection_rate=success.sum()/counts.sum(),bootstrap_ci_low=lo,bootstrap_ci_high=hi))
    write_csv(args.output/'seed_cluster_bootstrap.csv',ci)
    report=['# Mid.0 intervention stability analysis','',f'Layer: `{config["layer"]}`. {len(rows):,} intervention records.','',
      'Endpoint: MediaPipe landmark detection, not a judgment of facial coherence. Human labels remain blank for review.',
      '','## Sampled crossings','', '| Feature | Direction | Last passing sampled alpha | First failing sampled alpha | Status |','|---|---|---|---|---|']
    for c in crossing:report.append(f'| {c["feature"]} | {c["direction"]} | {c["last_passing_sample_before_first_failure"]} | {c["first_failing_sample"]} | {c["status"]} |')
    report+=['','Detection threshold is an exploratory 95%, applied to initially active, alpha=1-detected samples. A crossing is not evidence of a discontinuous cliff. Negative reversal excludes alpha=0 ablation and 0<alpha<1 attenuation.','',
      'Curves include all images, initially active images, and initially active images with a detected alpha=1 reference. Wilson intervals are descriptive; use seed_cluster_bootstrap.csv for uncertainty preserving shared noise seeds across prompt groups. These are pointwise intervals, not simultaneous bounds.','',
      'Coefficient plots use per-image p95 over initially active spatial cells, not pooled pixel histogram values. They pool repeated interventions and are exploratory associations; their bins do not establish universal coefficient limits.','',
      'delta_fro is the pre-cast intervention Frobenius norm calculated from saved feature maps and the checkpoint decoder norm. relative_delta_fro uses the recorded original-block normalization where available; it is empty for older runs whose original activation norms were not saved. delta_fro_applied additionally records the actual change after floating-point casting in new runs.','',
      'Original-versus-alpha=1 pixel MAE is recorded per image where the saved baseline exists. Inactive maps provide a no-change implementation check.','',
      'Review sheets prioritize detector transition cases and include strongest-strength audit cases (up to two per prompt group per feature); they are not an unbiased human evaluation set. Label human_review.csv with coherent_face, distorted_face, plausible_pose_or_occlusion, or face_replaced; leave uncertain examples marked uncertain.','',
      'These runs use the same mid.0 SAE and SDXL-Turbo single-step configuration. Feature selection is inherited, not a random or matched control sample. No attribute segmentation or prediction of held-out feature boundaries is claimed.','',
      '![Detection curves](detection_curves.png)','![Coefficient associations](coefficient_detection.png)']
    (args.output/'REPORT.md').write_text('\n'.join(report)+'\n')
    print(f'Completed: {args.output}',flush=True)

if __name__=='__main__':main()
