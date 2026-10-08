from pathlib import Path
import json,statistics
from PIL import Image,ImageOps
p=Path(__file__).resolve().parents[2]; out=p/'site/dist/pages';count=0
for f in sorted((p/'extracted').glob('IMG*.json')):
 d=json.loads(f.read_text()); imgpath=out/(f.stem+'.jpg'); im=Image.open(imgpath)
 if im.width>im.height:continue
 lines=[x for x in d['lines'] if len(x['text'])>15]
 sideways=sum(x['h']>x['w'] for x in lines)>len(lines)/2
 if sideways:im=im.transpose(Image.Transpose.ROTATE_90)
 im.thumbnail((2400,1800)); im.save(imgpath,quality=83,optimize=True)
 count+=1
print('Prepared',count,'images')
