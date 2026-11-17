#!/usr/bin/env python3
"""Re-layout existing overlay strips into 3x3 pages; no model inference.

Each source row is three 256px tiles plus its existing 28px label strip.
PNG pages preserve the decoded source pixels without resizing or JPEG recompression.
"""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--results-dir',type=Path,required=True);a=p.parse_args();root=a.results_dir.resolve();out=root/'contact_sheets_3x3'
 if out.exists():raise FileExistsError('Refusing to overwrite existing gallery: '+str(out))
 sources=sorted((root/'contact_sheets').glob('*.jpg'));assert len(sources)==12
 rows=[];index='# Beard overlays: 3 × 3 pages\n\nEach page shows three seeds (rows) and multipliers **−7, +1, +7** (columns). The last page has two seeds. These are the existing DINOv3-backed FaceParsing class14 overlays, unchanged; no new segmentation or image generation. Original long strips remain in `../contact_sheets/`.\n\n| Prompt group | Pages |\n|---|---|\n'
 out.mkdir()
 for source in sources:
  group=source.stem;dest=out/group;dest.mkdir();text=f'# {group.replace("_"," ").title()} — beard overlays\n\nThree columns: **α = −7, +1, +7**. Three seeds per page, in order30–49. Magenta denotes the parser’s predicted class14 region; it is not ground truth.\n\n'
  with Image.open(source) as original:
   image=original.convert('RGB');assert image.size==(768,5680)
   for page,start in enumerate(range(0,20,3),1):
    count=min(3,20-start);canvas=Image.new('RGB',(768,900),'white');draw=ImageDraw.Draw(canvas)
    draw.text((8,8),f'{group} | page {page}/7 | seeds {start+30}-{start+count+29}',fill='black')
    draw.text((8,27),'Columns: multiplier -7, +1 (unchanged), +7',fill='black')
    box=(0,start*284,768,(start+count)*284);crop=image.crop(box);canvas.paste(crop,(0,48))
    path=dest/f'page_{page:02d}.png';canvas.save(path)
    with Image.open(path) as check:assert check.crop((0,48,768,48+count*284)).tobytes()==crop.tobytes()
    rows.append(dict(prompt_group=group,page=page,first_seed=start+30,last_seed=start+count+29,n_images=count*3,source_path=str(source.relative_to(root)),source_sha256=sha(source),source_crop_box=json.dumps(box),page_path=str(path.relative_to(out)),page_sha256=sha(path)))
    text+=f'## Seeds {start+30}–{start+count+29}\n\n![Page {page}](page_{page:02d}.png)\n\n'
  (dest/'README.md').write_text(text)
  index+=f'| [{group.replace("_"," ").title()}]({group}/README.md) | '+ ' · '.join(f'[{j}]({group}/page_{j:02d}.png)' for j in range(1,8))+' |\n'
 (out/'README.md').write_text(index)
 with (out/'manifest.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 assert sum(r['n_images'] for r in rows)==720 and len(rows)==84
 print('Created84 pages,12 groups,720 existing overlays; decoded pixels verified exactly.')
if __name__=='__main__':main()
