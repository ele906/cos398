"""Rank group differences using the fine-tuned SAE and cached mid.0 residuals."""
from pathlib import Path
import sys,csv,json,hashlib
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sdxl-unbox'))
from SAE import SparseAutoencoder

def main():
 torch.set_num_threads(4)
 checkpoint=ROOT/'layers/runs/mid0_sae_face_001/sae'
 capture=ROOT/'layers/runs/mid0_sae_finetune_001/capture'
 out=ROOT/'layers/mid0_stability/finetuned_ranking';out.mkdir(exist_ok=True)
 rows=list(csv.DictReader((capture/'manifest.csv').open()))
 groups=sorted({r['race_prompt'].replace(' ','_')+'_'+r['gender_prompt'] for r in rows})
 device='cuda' if torch.cuda.is_available() else 'cpu'
 sae=SparseAutoencoder.load_from_disk(str(checkpoint)).float().to(device).eval()
 sums=np.zeros((12,5120),dtype=np.float64);counts=np.zeros(12,dtype=int)
 with torch.inference_mode():
  for i,row in enumerate(rows):
   g=groups.index(row['race_prompt'].replace(' ','_')+'_'+row['gender_prompt'])
   x=np.load(capture/'residuals'/f"{row['sample_id']}.npy").astype(np.float32)
   z=sae.encode(torch.from_numpy(x).reshape(-1,1280).to(device))
   sums[g]+=z.mean(0).cpu().numpy();counts[g]+=1
   if (i+1)%100==0:print('Encoded',i+1,'of',len(rows),flush=True)
 means=sums/counts[:,None]
 candidates=sorted({int(f) for group in means for f in np.argsort(group)[-10:]})
 scores=[]
 for f in candidates:
  peak=int(means[:,f].argmax());other=float(np.delete(means[:,f],peak).mean())
  scores.append(dict(feature=f,peak_group=groups[peak],peak_mean=float(means[peak,f]),other_mean=other,gap=float(means[peak,f])-other))
 scores.sort(key=lambda r:r['gap'],reverse=True)
 for i,r in enumerate(scores):r['rank']=i+1
 with (out/'ranked_candidates.csv').open('w',newline='') as stream:
  w=csv.DictWriter(stream,fieldnames=list(scores[0]));w.writeheader();w.writerows(scores)
 selected=[r['feature'] for r in scores[:10]]
 norm={str(f):float(sae.decoder.weight[:,f].norm().item()) for f in selected}
 for f in (1650,2023,4228):norm[str(f)]=float(sae.decoder.weight[:,f].norm().item())
 (out.parent/'decoder_norms.json').write_text(json.dumps(norm,indent=2)+'\n')
 metadata=dict(checkpoint=str(checkpoint),checkpoint_sha256=hashlib.sha256((checkpoint/'state_dict.pth').read_bytes()).hexdigest(),layer='unet.mid_block.attentions.0',ranking='Union of each group top-10 raw means; descending peak group mean minus other 11 group means',groups=groups,images_per_group=counts.tolist(),capture=str(capture),discovery_seeds='100-199; descriptive ranking, not held-out causal evidence',features=selected)
 (out/'top10.json').write_text(json.dumps(metadata,indent=2)+'\n')
 np.savez_compressed(out/'group_means.npz',groups=np.array(groups),means=means)
 print(json.dumps(metadata,indent=2),flush=True)
if __name__=='__main__':main()
