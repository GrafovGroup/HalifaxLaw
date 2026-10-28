"""Each rendered placement owns an asset; no category-based image fallback."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parent
mapping_path=ROOT/'image-placements.json'
placements=json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
active_images=[item for entries in placements.values() for item in entries if not item.get('skip')]
if len({item['asset'] for item in active_images}) != len(active_images):
    raise ValueError('Each photograph must belong to exactly one placement.')
if any(not item.get('relevance_reason') for item in active_images):
    raise ValueError('Every photograph needs an explicit relevance reason before publication.')

def apply_images(body,route,fr):
    key=('/fr/' if fr else '/')+route.strip('/')+('/' if route else '')
    if key not in placements:
        if placements and '<img' in body: raise ValueError('Assign unique images before building page: '+key)
        return body
    entries=iter(placements[key])
    def replace(match):
        try: item=next(entries)
        except StopIteration: raise ValueError('Missing image placement: '+key)
        if item.get('skip'): return ''
        tag=match.group(0)
        for name,value in [('src','/assets/'+item['asset']),('alt',item['alt_fr' if fr else 'alt_en']),('width',item['width']),('height',item['height'])]:
            tag=re.sub(r'\b'+name+r'="[^"]*"',name+'="'+html.escape(str(value),quote=True)+'"',tag)
        if item.get('small_asset'):
            sizes='(max-width: 800px) 88vw, 660px' if 'article-image' in tag else '(max-width: 800px) 88vw, 600px'
            tag=tag.replace('>', ' srcset="/assets/'+item['small_asset']+' 600w, /assets/'+item['asset']+' '+str(item['width'])+'w" sizes="'+sizes+'" decoding="async">')
        return tag
    result=re.sub(r'<img\b[^>]*>',replace,body)
    if next(entries,None) is not None: raise ValueError('Unused image placement: '+key)
    return result

def credits(fr):
    rows=[]
    for route,entries in placements.items():
        for entry in entries:
            if entry.get('skip') or not entry.get('license_url'):continue
            def e(v):return html.escape(str(v),quote=True)
            rows.append(f'<li><a href="{e(route)}">{e(route)}</a> — {e(entry["alt_fr" if fr else "alt_en"])}. {e(entry["author"])}. <a href="{e(entry["source_page"])}">{e(entry.get("title", "Source"))}</a> · <a href="{e(entry["license_url"])}">{e(entry["license"])}</a>.</li>')
    note='Photographies redimensionnées et converties au format WebP. Les licences indiquées s’appliquent aux photographies correspondantes.' if fr else 'Photographs resized and converted to WebP. The listed licences apply to their respective photographs.'
    return '<section class="section narrow"><h1>'+('Crédits photographiques' if fr else 'Photography credits')+'</h1><p>'+note+'</p><ol class="photo-credits">'+''.join(rows)+'</ol></section>'
