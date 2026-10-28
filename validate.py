"""Validate generated routes, anchors, language alternates and structured data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
 def __init__(self, text):
  super().__init__();self.ids=[];self.links=[];self.images=[];self.alternates=[];self.canonical=[];self.h1=0;self.schemas=[];self.current=None;self.feed(text)
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='img':self.images.append(a)
  if tag=='link' and a.get('rel')=='alternate':self.alternates.append(a)
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='script' and a.get('type')=='application/ld+json':self.current=''
 def handle_data(self,data):
  if self.current is not None:self.current+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.current is not None:self.schemas.append(json.loads(self.current));self.current=None
pages={str(p.relative_to(ROOT)):Page(p.read_text()) for p in ROOT.rglob('*.html')}
errors=[]
for path,page in pages.items():
 def check(ok,msg):
  if not ok:errors.append(f'{path}: {msg}')
 check(page.h1==1,'expected exactly one H1')
 check(len(page.ids)==len(set(page.ids)),'duplicate IDs')
 check(len(page.canonical)==1,'expected one canonical')
 check(bool(page.schemas),'missing schema')
 for img in page.images:
  check('alt' in img and 'width' in img and 'height' in img,'image needs alt/dimensions')
  check((ROOT/img['src'].lstrip('/')).exists(),'missing image '+img['src'])
 for href in page.links+[a['href'] for a in page.alternates]:
  u=urlsplit(href)
  if u.netloc and u.netloc!='halifaxlaw.ca' or u.scheme in ('mailto','tel'):continue
  target=u.path.lstrip('/') if u.path else path
  if target.endswith('/') or not target:target+='index.html'
  check((ROOT/target).is_file(),'broken local link '+href)
  if u.fragment and target in pages:check(unquote(u.fragment) in pages[target].ids,'broken anchor '+href)
 for schema in page.schemas:
  graph=schema.get('@graph',[])
  check(bool(graph),'expected linked entity graph')
  for item in graph:
   if item.get('@type')=='FAQPage':
    check(bool(item.get('mainEntity')),'empty FAQ schema')
    for q in item['mainEntity']:check(bool(q['acceptedAnswer']['text']),'empty answer')
xml=ET.parse(ROOT/'sitemap.xml')
urls=[e.text for e in xml.findall('{*}url/{*}loc')]
assert len(urls)==len(set(urls)), 'duplicate sitemap URLs'
for url in urls:
 path=urlsplit(url).path.lstrip('/')+'index.html'
 if path not in pages: errors.append('sitemap missing page '+url)
 if '/404/' in url or '/image-credits/' in url:errors.append('excluded page in sitemap '+url)
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML files; {len(urls)} sitemap URLs; local links, anchors, alternates, image dimensions and JSON-LD.')
