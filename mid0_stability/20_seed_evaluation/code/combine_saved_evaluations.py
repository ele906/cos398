"""Combine same-environment saved detections for disjoint seeds; no detector replay."""
from pathlib import Path
import argparse,importlib.util,json,itertools
import numpy as np
import pandas as pd
ROOT=Path('/n/fs/goose')

def main():
 p=argparse.ArgumentParser();p.add_argument('--extra',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 original=ROOT/'cos398/mid0_stability';extra=args.extra;out=args.output
 if out.exists():raise FileExistsError(out)
 spec=importlib.util.spec_from_file_location('saved_analysis',ROOT/'layers/mid0_stability/analyze_stability.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 old_config=json.loads((original/'experiment.json').read_text());new_config=json.loads((extra/'experiment.json').read_text())
 for k in ['checkpoint_sha256','layer','features','alphas']:
  if old_config[k]!=new_config[k]:raise ValueError('Configuration mismatch: '+k)
 old=pd.read_csv(original/'per_image.csv');new=pd.read_csv(extra/'per_image.csv')
 if set(old.seed)&set(new.seed):raise ValueError('Overlapping seeds; refusing duplicate observations')
 detector=json.loads((original/'settings.json').read_text());newdet=json.loads((extra/'settings.json').read_text())
 for key in ['layer','features','mediapipe_version','model_sha256','detector','min_face_detection_confidence','min_face_presence_confidence','detection_threshold']:
  if detector[key]!=newdet[key]:raise ValueError('Detector mismatch: '+key)
 # Per-feature generation software versions are also checked against the original run.
 old_root=Path(old_config['output_root']);new_root=Path(new_config['output_root'])
 for feat in old_config['features']:
  a=json.loads((old_root/f'feature_{feat}/settings.json').read_text());b=json.loads((new_root/f'feature_{feat}/settings.json').read_text())
  for key in ['software_versions','block','sae_weights_sha256','model','vae','steps','guidance_scale','scheduler','timestep_spacing','height','width','face_box_mask']:
   if a[key]!=b[key]:raise ValueError(f'Generation mismatch {feat}: {key}')
 d=pd.concat([old,new],ignore_index=True)
 for key in ['face_detected','baseline_detected','initially_active']:
  if d[key].isna().any() or not set(d[key].unique())<={True,False}:raise ValueError('Invalid detection flag')
 if d.duplicated(['feature','group','seed','alpha']).any():raise ValueError('Duplicate conditions')
 seeds=sorted(int(s) for s in d.seed.unique());groups=sorted(d.group.unique())
 expected=set(itertools.product(old_config['features'],groups,seeds,old_config['alphas']))
 actual=set(map(tuple,d[['feature','group','seed','alpha']].to_numpy()))
 if expected!=actual:raise ValueError('Incomplete condition grid')
 out.mkdir(parents=True)
 d.image=d.image.map(lambda v:str(ROOT/v) if not Path(v).is_absolute() else v)
 d.to_csv(out/'per_image.csv',index=False);rows=d.to_dict('records')
 summary=m.summarize(rows);m.write_csv(out/'detection_summary.csv',summary);m.write_csv(out/'sampled_boundaries.csv',m.boundaries(summary,detector['detection_threshold']))
 m.plots(summary,rows,out)
 config=dict(old_config);config.update(seeds=seeds,total_conditions=len(d),source_experiments=[str(original/'experiment.json'),str(extra/'experiment.json')],output_root='Combined saved evaluation CSVs; images remain in source runs',analysis_output=str(out))
 (out/'experiment.json').write_text(json.dumps(config,indent=2)+'\n');(out/'settings.json').write_text(json.dumps(detector,indent=2)+'\n')
 pd.DataFrame([dict(source='original',rows=len(old),seeds=str(sorted(old.seed.unique()))),dict(source='extra',rows=len(new),seeds=str(sorted(new.seed.unique())))]).to_csv(out/'source_audit.csv',index=False)
 print(f'Combined {len(d)} records, {len(seeds)} seeds per group: {out}',flush=True)
if __name__=='__main__':main()
