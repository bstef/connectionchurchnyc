"""Preserve publicly listed metadata. Does not download audio or create transcripts."""
import subprocess
import concurrent.futures, hashlib, html, json, re, urllib.request
from pathlib import Path
from urllib.parse import urlparse
BASE = 'https://podcast.app/connection-church-nyc-sermons-p282311'
def page(number):
    source = subprocess.check_output(['curl','--fail','-L','-s','--max-time','30',f'{BASE}?page={number}'], text=True)
    data = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', source).group(1))
    props = data['props']['pageProps']
    if props['podcast']['name'] != 'Connection Church NYC Sermons':
        raise ValueError('Unexpected podcast identity')
    return props['episodesPage']
first = page(1)
count = first['count']
pages = (count + len(first['episodeList']) - 1) // len(first['episodeList'])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    batches = [first] + list(pool.map(page, range(2, pages + 1)))
rows = {}
for batch in batches:
    for e in batch['episodeList']:
        audio = e['audio_url']
        if not urlparse(audio).hostname.endswith('buzzsprout.com'):
            raise ValueError('Unexpected audio host: '+urlparse(audio).hostname)
        audio = audio.replace('http://','https://',1)
        eid = hashlib.sha256(f"podcast.app:{e['pk']}".encode()).hexdigest()[:20]
        description = html.unescape(e['html_clean_description']).split('Support the show')[0].split('We are a Christian Church')[0].strip()
        credit = re.search(r'\bPastor Daniel\b', description)
        rows[eid] = dict(id=eid,title=e['title'],date=e['published'][:10],audio_url=audio,description=description,
            link='https://podcast.app/'+e['slug'],speaker='Pastor Daniel' if credit else '',speaker_source='description' if credit else '',passages=0)
if len(rows) != count:
    raise ValueError(f'Incomplete archive: {len(rows)} of {count}')
rows = sorted(rows.values(), key=lambda e:(e['date'],e['id']), reverse=True)
existing_path=Path('assets/sermons/catalog.json')
existing={e['id']:e for e in json.loads(existing_path.read_text())} if existing_path.exists() else {}
for e in rows:
    for key in ['youtube_url','transcript_source']:
        if key in existing.get(e['id'],{}): e[key]=existing[e['id']][key]
Path('assets/sermons/catalog.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
quote = lambda s: "'"+s.replace("'", "''")+"'"
columns = ['id','title','date','audio_url','description','link','speaker','speaker_source']
# Runs after schema and speaker-column migrations; metadata refresh preserves transcripts.
statements = ['-- Public podcast.app metadata snapshot; no audio or transcript text.']
for e in rows:
    values = ','.join(quote(e[c]) for c in columns)
    updates = ','.join(f'{c}=excluded.{c}' for c in columns if c != 'id')
    statements.append(f"INSERT INTO episodes({','.join(columns)}) VALUES({values}) ON CONFLICT(id) DO UPDATE SET {updates};")
Path('migrations/0005_connection_catalog.sql').write_text('\n'.join(statements)+'\n')
print(f"Preserved {len(rows)} episode records: {rows[-1]['date']} to {rows[0]['date']}. No transcripts generated.")
