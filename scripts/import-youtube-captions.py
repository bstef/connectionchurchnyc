"""Import a timestamped browser-exported caption file; no AI requests or downloads.
Usage: python3 scripts/import-youtube-captions.py EPISODE_ID VIDEO_ID FILE OUTPUT_SQL
Times are relative to the YouTube video, not the original podcast MP3.
"""
import argparse, json, re
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('episode_id');p.add_argument('video_id');p.add_argument('file',type=Path);p.add_argument('output_sql',type=Path)
a=p.parse_args()
rows=json.loads(Path('assets/sermons/catalog.json').read_text());episode=next(e for e in rows if e['id']==a.episode_id)
if episode.get('youtube_url') != 'https://www.youtube.com/watch?v='+a.video_id: raise ValueError('Episode has no matching YouTube source')
source=a.file.read_text()
if 'Video ID: '+a.video_id not in source: raise ValueError('Caption source video does not match')
segments=[]
for line in source.splitlines():
 m=re.fullmatch(r'\[(\d+):(\d{2})(?::(\d{2}))?\] (.+)',line)
 if not m: continue
 start=int(m[1])*60+int(m[2]) if m[3] is None else int(m[1])*3600+int(m[2])*60+int(m[3])
 if segments and start<segments[-1]['start']: raise ValueError('Captions are out of order')
 if segments and start==segments[-1]['start']: segments[-1]['text']+=' '+m[4]
 else: segments.append({'start':start,'text':m[4]})
if not segments: raise ValueError('No timed captions found')
for i,s in enumerate(segments):s['end']=segments[i+1]['start'] if i+1<len(segments) else s['start']+2
chunks=[];i=0
while i<len(segments):
 j=i+1
 while j<len(segments) and segments[j]['end']-segments[i]['start']<=60 and sum(len(s['text'].split()) for s in segments[i:j+1])<=220:j+=1
 chunks.append({'start':segments[i]['start'],'end':segments[j-1]['end'],'text':' '.join(s['text'] for s in segments[i:j])})
 i=j-1 if j-i>1 and j<len(segments) else j
quote=lambda s:"'"+s.replace("'","''")+"'"
sql=['-- Actual YouTube automatic captions; unreviewed; video-relative timestamps.',f'DELETE FROM passages WHERE episode_id={quote(a.episode_id)};']
for c in chunks:sql.append(f"INSERT INTO passages(episode_id,start,end,text) VALUES({quote(a.episode_id)},{c['start']},{c['end']},{quote(c['text'])});")
a.output_sql.parent.mkdir(parents=True,exist_ok=True);a.output_sql.write_text('\n'.join(sql)+'\n')
episode['transcript_source']='YouTube automatic captions (unreviewed)'
Path('assets/sermons/catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'Imported {len(segments)} caption segments into {len(chunks)} passages. No AI calls.')
