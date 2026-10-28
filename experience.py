"""Shared bilingual UX and search metadata; build-time HTML, no client dependency."""
from consultation import profile, preview, about_details
import html
import json
import re
from urllib.parse import urlsplit

ORIGIN = 'https://halifaxlaw.ca'
NAME = 'Kostyantyn Mykhalchenko'
TOPICS = {
 'property': ('Real estate', 'Immobilier'),
 'family': ('Family & separation', 'Famille et séparation'),
 'wills-estates': ('Wills & estates', 'Testaments et successions'),
 'business': ('Business & contracts', 'Entreprises et contrats'),
 'housing': ('Residential tenancies', 'Location résidentielle'),
 'disputes': ('Civil disputes', 'Litiges civils'),
 'criminal-law': ('Criminal law', 'Droit criminel'),
}

def plain(s):
 return html.unescape(re.sub('<[^>]+>', '', s)).strip()

def enhance(body, route, title, fr):
 def t(en, french): return french if fr else en
 def link(r): return ('/fr/' if fr else '/') + (r.strip('/')+'/' if r else '')
 def anchor(url, text, cls=''):
  return f'<a class="{cls}" href="{html.escape(url,quote=True)}">{html.escape(text)}</a>'
 contact=link('contact')
 is_service=route.startswith('topics/')
 slug=route.split('/')[-1]
 enquiry=contact+(f'?topic={slug}' if is_service else '')+'#enquiry'
 question_pairs=[
  (t('How do I request an appointment?', 'Comment demander un rendez-vous?'),t('Call (289) 888-5878 or send a short enquiry to Kostyantyn Mykhalchenko. Include the general topic, any important dates and your preferred appointment language. The practice will confirm availability and whether it can assist.', 'Appelez le (289) 888-5878 ou envoyez une courte demande à Kostyantyn Mykhalchenko. Indiquez le sujet général, les dates importantes et votre langue de rendez-vous souhaitée. Le cabinet confirmera sa disponibilité et s’il peut vous aider.')),
  (t('What will legal services cost?', 'Combien coûtent les services juridiques?'),t('Ask the practice for the proposed scope, fee arrangement and any additional costs before agreeing to proceed. This website does not publish a fee schedule or promise a free consultation.', 'Demandez au cabinet la portée proposée, les modalités d’honoraires et les frais supplémentaires avant de donner votre accord. Ce site ne publie pas de grille tarifaire et ne promet pas de consultation gratuite.')),
  (t('Can I get help outside Halifax?', 'Puis-je obtenir de l’aide à l’extérieur de Halifax?'),t('Kostyantyn serves clients across Nova Scotia. Confirm the appointment location and format directly with the practice. Community guides do not indicate branch offices.', 'Kostyantyn sert des clients partout en Nouvelle-Écosse. Confirmez le lieu et le mode du rendez-vous avec le cabinet. Les guides locaux ne désignent pas des succursales.')),
  (t('Which languages are available?', 'Quelles langues sont offertes?'),t('Appointments are available in English, Ukrainian and Russian. French pages provide information; they do not indicate French-language representation.', 'Les rendez-vous sont offerts en anglais, ukrainien et russe. Les pages françaises sont informatives et n’indiquent pas une offre de représentation en français.')),
 ]
 faq='<section class="section answer-section" id="quick-answers"><div><span class="eyebrow">'+t('BEFORE YOU REACH OUT','AVANT DE COMMUNIQUER')+'</span><h2>'+t('Clear answers.<br>A simpler first step.','Des réponses claires.<br>Une première étape simple.')+'</h2>'+anchor(link('faq'),t('More questions & answers →','Autres questions et réponses →'),'text-link')+'</div><div>'+''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in question_pairs)+'</div></section>'
 if route=='':
  body=body.replace("Legal guidance.<br>Clear next steps.<br><em>Here in Halifax.</em>","Your Halifax lawyer.<br><em>A clear next step.</em>")
  body=body.replace('Des conseils juridiques.<br>Une prochaine étape claire.<br><em>À Halifax.</em>','Votre avocat à Halifax.<br><em>Une prochaine étape claire.</em>')
  start=body.index('<div class="actions">'); end=body.index('</div>',start)
  body=body[:start]+'<div class="actions">'+anchor(enquiry,t('Request an appointment','Demander un rendez-vous'),'button')+anchor('tel:+12898885878',t('Call (289) 888-5878','Appeler le (289) 888-5878'),'light-link')+body[end:]
  quick='<section class="quick-start" aria-labelledby="find-help"><div><span class="eyebrow">'+t('START WITH YOUR SITUATION','VOTRE POINT DE DÉPART')+'</span><h2 id="find-help">'+t('What can we help you with?','Comment pouvons-nous vous aider?')+'</h2></div><div class="topic-shortcuts">'+''.join(anchor(link('topics/'+key),names[fr]+' ↗') for key,names in TOPICS.items())+'</div></section>'
  body=re.sub(r'<div class="chapter-strip">.*?</div>',quick,body,count=1)
  body=body.replace('<section class="local-feature">',profile(fr)+'<section class="local-feature">',1)
  body=re.sub(r'<section class="section steps">.*?</section>',preview(fr),body,count=1,flags=re.S)
  body=body.replace('<section class="callout">',faq+'<section class="callout">',1)
 if route=='about':
  body=body.replace('<section class="callout">',about_details(fr)+'<section class="callout">',1)
 if route=='faq':
  body=body.replace('<section class="callout">',faq+'<section class="callout">',1)
 if is_service:
  body=re.sub(re.escape(contact)+r'(?:\?topic=criminal-law)?(?=")',enquiry,body)
  intro=re.search(r'<section class="page-hero">.*?</section>',body)
  if intro:
   bar='<div class="service-actions">'+anchor(enquiry,t('Ask about this service','Poser une question'),'button')+anchor('#prepare',t('What to prepare ↓','Que préparer ↓'),'text-link')+anchor('#quick-answers',t('Common questions ↓','Questions fréquentes ↓'),'text-link')+'</div>'
   body=body[:intro.end()]+bar+body[intro.end():]
  body=body.replace('</aside>', '<p class="guide-profile-link">'+anchor(link('first-consultation'),t('What to expect at your first consultation →','À quoi s’attendre à la première consultation →'),'text-link')+'</p></aside>',1)
  body=body.replace('<aside class="checklist">','<aside class="checklist" id="prepare">',1)
  body=body.replace('<section class="callout">',faq+'<section class="callout">',1)
 if route=='contact':
  body=body.replace('class="page-hero"','class="page-hero contact-hero"',1)
  body=body.replace('<h2>'+t('Get in touch','Communiquez directement')+'</h2>', '<h2>'+t('Choose how to get in touch','Choisissez votre moyen de contact')+'</h2><div class="contact-options">'+anchor('#enquiry',t('Send an enquiry ↓','Envoyer une demande ↓'),'button')+anchor('tel:+12898885878',t('Call (289) 888-5878','Appeler le (289) 888-5878'),'button button-outline')+'</div>')
  body=body.replace('class="enquiry-section"','class="enquiry-section" id="enquiry"',1)
  body=body.replace('<section class="enquiry-section"', '<p class="consultation-note">'+anchor(link('first-consultation'),t('New to the practice? Read the first-consultation guide →','Première démarche? Consultez le guide de première consultation →'))+'</p><section class="enquiry-section"',1)
  body=body.replace('</aside>', '<div class="next-expect"><h3>'+t('What happens next?','Que se passe-t-il ensuite?')+'</h3><ol><li>'+t('The practice reviews your enquiry.','Le cabinet examine votre demande.')+'</li><li>'+t('Availability, scope and conflict checks are confirmed.','La disponibilité, la portée et les conflits sont vérifiés.')+'</li><li>'+t('You agree on fees and the next step before proceeding.','Vous convenez des honoraires et de la prochaine étape avant de poursuivre.')+'</li></ol></div></aside>',1)
 # Complete breadcrumb trail on all non-home pages.
 crumbs=[(link(''),t('Home','Accueil'))]
 if '/' in route:
  parent=route.split('/')[0]
  crumbs.append((link(parent),t('Practice areas','Domaines') if parent=='topics' else t('Communities','Collectivités')))
 if route: crumbs.append((link(route),title.split(' — ')[0]))
 if route and 'class="breadcrumbs"' not in body:
  body='<nav class="breadcrumbs" aria-label="'+t('Breadcrumb','Fil d’Ariane')+'">'+''.join((anchor(url,label)+'<span aria-hidden="true">/</span>') if i<len(crumbs)-1 else '<span aria-current="page">'+html.escape(label)+'</span>' for i,(url,label) in enumerate(crumbs))+'</nav>'+body
 return body, crumbs

def metadata(body, route, title, desc, fr, crumbs):
 lang='fr-CA' if fr else 'en-CA'
 url=ORIGIN+('/fr/' if fr else '/')+(route+'/' if route else '')
 org={'@type':'Organization','@id':ORIGIN+'/#practice','name':'Pavel Boubnov – Barrister & Solicitor','url':ORIGIN,'telephone':'+12898885878','email':'info@halifaxlaw.ca'}
 person={'@type':'Person','@id':ORIGIN+'/#lawyer','name':NAME,'url':ORIGIN+'/about/','jobTitle':'Barrister, Solicitor & Notary Public','knowsLanguage':['English','Ukrainian','Russian'],'worksFor':{'@id':ORIGIN+'/#practice'},'sameAs':['https://members.nsbs.org/NSBSWEB/Lawyer_Search/Results_Page2.aspx?ID=125622']}
 website={'@type':'WebSite','@id':ORIGIN+'/#website','name':'HalifaxLaw.ca','url':ORIGIN+'/','inLanguage':['en-CA','fr-CA'],'publisher':{'@id':ORIGIN+'/#practice'}}
 page={'@type':'WebPage','@id':url+'#webpage','name':title,'description':desc,'url':url,'inLanguage':lang,'isPartOf':{'@id':ORIGIN+'/#website'},'about':{'@id':ORIGIN+'/#lawyer'}}
 if route=='about': page['@type']='ProfilePage';page['mainEntity']={'@id':ORIGIN+'/#lawyer'}
 if route=='contact':page['@type']='ContactPage'
 graph=[org,person,website,page]
 if route:
  breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i+1,'name':label,'item':ORIGIN+href} for i,(href,label) in enumerate(crumbs)]}
  graph.append(breadcrumb);page['breadcrumb']={'@id':breadcrumb['@id']}
 if route.startswith('topics/'):
  graph.append({'@type':'Service','@id':url+'#service','name':title.split(' — ')[0],'url':url,'description':desc,'provider':{'@id':ORIGIN+'/#lawyer'},'areaServed':{'@type':'AdministrativeArea','name':'Nova Scotia'}})
 # Mark up only the Q&A that visitors can read on the same page.
 pairs=re.findall(r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',body,re.S)
 if pairs and route=='faq':
  page['@type']='FAQPage' if route=='faq' else page['@type']
  faq={'@type':'FAQPage','@id':url+'#questions','url':url+'#quick-answers','inLanguage':lang,'mainEntity':[{'@type':'Question','name':plain(q),'acceptedAnswer':{'@type':'Answer','text':plain(a)}} for q,a in pairs]}
  if route=='faq':page['mainEntity']=faq['mainEntity']
  else: graph.append(faq)
 hero=re.search(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"',body)
 tags='<meta property="og:site_name" content="HalifaxLaw.ca"><meta property="og:locale" content="'+lang.replace('-','_')+'"><meta property="og:locale:alternate" content="'+('en_CA' if fr else 'fr_CA')+'">'
 if hero:
  image_url=ORIGIN+hero[1]
  tags+=f'<meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{hero[2]}"><meta name="twitter:image" content="{image_url}"><meta name="twitter:image:alt" content="{hero[2]}">'
 tags+='<meta name="theme-color" content="#102c3b"><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
 return tags
