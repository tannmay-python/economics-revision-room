from pathlib import Path
from PIL import Image
import json,statistics
root=Path(__file__).resolve().parents[2]
for f in sorted((root/'extracted/ied').glob('ied-*.json')):
 p=root/'site/dist/ied-pages'/(f.stem+'.jpg'); im=Image.open(p)
 if im.width<im.height:
  ls=json.loads(f.read_text())['lines']; xs=[x['x'] for x in ls if x['h']>x['w']]
  dx=[b-a for a,b in zip(xs,xs[1:]) if .002<abs(b-a)<.08]
  im=im.transpose(Image.Transpose.ROTATE_270 if statistics.median(dx)>0 else Image.Transpose.ROTATE_90)
 im.thumbnail((2400,1800));im.convert('RGB').save(p,quality=82,optimize=True)
print('Prepared 71 upright source spreads')
