#!/usr/bin/env python3
"""Fetch attributed Commons photographs; retain original response and provenance.
No API keys. Run from repository root: python3 scripts/collect.py
"""
import argparse, datetime, html, json, pathlib, re, subprocess, time, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[1]
HEADERS = {'User-Agent': 'RoamNotes/1.0 (personal educational travel atlas; Wikimedia Commons MediaWiki client)'}
def get(url):
    if urllib.parse.urlparse(url).hostname in ('thumb.wikimedia.org', 'upload.wikimedia.org'):
        url=url.split('?')[0]
    # Use the system curl CA store; keep TLS verification enabled.
    return subprocess.run(
        ['curl', '--http1.1', '--fail', '--location', '--silent', '--show-error',
         '--connect-timeout', '15', '--max-time', '30', '--retry', '1',
         '--user-agent', HEADERS['User-Agent'], url],
        check=True, capture_output=True,
    ).stdout
def clean(value):
    return html.unescape(re.sub('<[^>]*>', '', value or '')).strip()
def collect(refresh=False):
    seeds=json.loads((ROOT/'src/data/seed.json').read_text())
    output=ROOT/'src/data/places.json'
    prior={x['id']:x for x in json.loads(output.read_text())} if output.exists() else {}
    (ROOT/'public/images').mkdir(parents=True,exist_ok=True)
    (ROOT/'sources/commons').mkdir(parents=True,exist_ok=True)
    result=[]
    for seed in seeds:
        old=prior.get(seed['id'])
        if not refresh and old and (ROOT/'public'/old['image'].lstrip('/')).exists():
            result.append(old); continue
        candidates=[]
        queries=list(dict.fromkeys([seed['query'], seed['english'], ' '.join(seed['query'].split()[:2])]))
        for query_index, query in enumerate(queries):
            params={'action':'query','format':'json','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1280}
            if seed.get('photoFile'):
                params['titles']=seed['photoFile']
            else:
                params.update(generator='search',gsrsearch=query+' filetype:bitmap',gsrnamespace=6,gsrlimit=12)
            raw=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params))
            (ROOT/'sources/commons'/f"{seed['id']}-{query_index}.json").write_bytes(raw)
            response=json.loads(raw)
            if 'error' in response: raise RuntimeError(response['error'])
            pages=sorted(response.get('query',{}).get('pages',{}).values(), key=lambda x:x.get('index',0))
            for page in pages:
                info=page.get('imageinfo',[{}])[0]; meta=info.get('extmetadata',{})
                license=clean(meta.get('LicenseShortName',{}).get('value',''))
                if not re.fullmatch(r'cc by(?:-sa)? [\d.]+|cc0(?: [\d.]+)?|public domain', license.lower()): continue
                w,h=info.get('width',0),info.get('height',1)
                if w < 900 or not 1.15 < w/h < 3: continue
                if any(x in page['title'].lower() for x in ['collage','montage','map of','locator','(ia ', 'engraving','painting','drawing','illustration','map (','plan of']): continue
                candidates.append((page,info,meta,license))
            if candidates: break
            time.sleep(1)
        if not candidates: raise RuntimeError(f"No verified landscape photo: {seed['id']}")
        for page,info,meta,license in candidates:
            try:
                url=(info.get('thumburl') or info['url']).split('?')[0]
                photo=get(url)
                if not (photo[:3]==b'\xff\xd8\xff' or photo[:8]==b'\x89PNG\r\n\x1a\n'): raise ValueError('Unexpected image format')
                ext='jpg' if photo[:3]==b'\xff\xd8\xff' else 'png'
                local=f"/images/{seed['id']}.{ext}"
                (ROOT/'public'/local.lstrip('/')).write_bytes(photo)
                entry={**seed,'image':local,'sourceUrl':f"https://whc.unesco.org/en/list/{seed['unesco']}/",'textLicense':'CC BY-SA 3.0 IGO','textLicenseUrl':'https://creativecommons.org/licenses/by-sa/3.0/igo/','textNote':'依据 UNESCO 世界遗产资料进行中文整理，非逐字翻译。亮点为编辑观察建议。','collectedAt':datetime.date.today().isoformat(),'photo':{'title':page['title'],'author':clean(meta.get('Artist',{}).get('value','Wikimedia Commons contributor')),'license':license,'licenseUrl':meta.get('LicenseUrl',{}).get('value',''),'page':info['descriptionurl'],'originalUrl':info['url'],'downloadUrl':url,'description':clean(meta.get('ImageDescription',{}).get('value',''))}}
                result.append(entry)
                print(seed['id'], license, page['title'], flush=True)
                break
            except Exception as err: print('Photo retry:',err,flush=True)
        else: raise RuntimeError(f"Photo download failed: {seed['id']}")
        # Checkpoint each successful item so interrupted runs can resume.
        output.write_text(json.dumps(result+[x for x in prior.values() if x['id'] not in {v['id'] for v in result}],ensure_ascii=False,indent=2))
        time.sleep(.8)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(f'Collected {len(result)} destinations. All photos stored locally.',flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--refresh',action='store_true'); args=parser.parse_args(); collect(args.refresh)
