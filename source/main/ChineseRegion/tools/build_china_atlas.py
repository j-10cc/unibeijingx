#!/usr/bin/env python3
"""Generate a read-only province/city/district/postcode atlas from China Post."""
import collections,gzip,hashlib,json,re
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p / 'source/main').is_dir())
SOURCE=ROOT/'external/data/china-post/chinapost-sites-2026-10-15.json.gz'
OUT=ROOT/'source/main/ChineseRegion'
def main():
 raw=gzip.decompress(SOURCE.read_bytes());d=json.loads(raw)
 assert d['success'] and len(d['list'])==d['total']==54622
 unique=set()
 for row in d['list']:
  key=tuple(row[k].strip() for k in ['province','cities','county','zipcode'])
  assert all(key) and len(key[3])==6 and key[3].isascii() and key[3].isdigit(),key
  unique.add(key)
 tree={}
 for p,c,a,z in sorted(unique):tree.setdefault(p,{}).setdefault(c,{}).setdefault(a,[]).append(z)
 def quote(s):return json.dumps(s,ensure_ascii=False)
 # Compile each province separately: tntk cannot compile one 350 KB nested literal.
 files=[]; symbols=[]; packed=bytearray()
 for index,(p,cities) in enumerate(tree.items()):
  symbol='ubxChinaProvince'+str(index);symbols.append(symbol)
  lines=["// Generated China Post outlet atlas; do not edit.","DefGlobalVar('"+symbol+",'{name:"+quote(p)+",cities:["]
  for c,areas in cities.items():
   lines.append('{name:'+quote(c)+',areas:[')
   for a,zips in areas.items():
    offset=len(packed)
    for code in zips:packed.extend(int(code[i:i+2]) for i in (0,2,4))
    lines.append('{name:'+quote(a)+',codesOffset:'+str(offset)+',codesCount:'+str(len(zips))+'},')
   lines.append(']},')
  lines.append(']});')
  filename='ChinaProvince'+str(index)+'.newt';files.append(filename)
  (OUT/filename).write_text(re.sub(r',\s*\]',']','\n'.join(lines))+'\n')
 (OUT/'ChinaCodes.bin').write_bytes(packed)
 (OUT/'ChinaData.newt').write_text("// Generated atlas root.\nDefGlobalVar('ubxChinaAtlas,{version:\"ChinaPost 2026-10-15\",codes:LoadBinary(\"ChinaCodes.bin\"),provinces:["+',\n'.join(symbols)+"]});\n")

 counts=dict(provinces=len(tree),cities=sum(len(c) for c in tree.values()),districts=sum(len(a) for c in tree.values() for a in c.values()),region_postcode_pairs=len(unique),unique_postcodes=len({r[3] for r in unique}),source_outlets=d['total'])
 manifest=dict(source_url='https://iframe.chinapost.com.cn/api/institutionalsite/findlist.do',request='act=list&page=1&size=60000&community=ChinaPostJT',source_page='https://iframe.chinapost.com.cn/jsp/type/institutionalsite/SiteSearchJTApi.jsp?community=ChinaPostJT',retrieved='2026-10-15',source_sha256=hashlib.sha256(raw).hexdigest(),snapshot=str(SOURCE.relative_to(ROOT)),snapshot_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),counts=counts,packed_postcode_bytes=len(packed),packed_encoding='Three unsigned base-100 byte pairs per six-digit code; offsets/counts in district tables; left-pad decimal decode to six ASCII digits.',coverage='Published postal outlets in 31 mainland provincial-level regions; outlet codes are candidates, not street-delivery guarantees. No invented codes, no inferred city-to-code one-to-one mapping.')
 (OUT/'geodata').mkdir(exist_ok=True)
 (OUT/'geodata/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (OUT/'geodata/atlas.json').write_text(json.dumps(tree,ensure_ascii=False,separators=(',',':'))+'\n')
 from build_supplemental_atlas import generate
 generate()
 print(counts)
if __name__=='__main__':main()
