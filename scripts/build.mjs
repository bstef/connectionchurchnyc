import { createHash } from 'node:crypto';
import { cp, mkdir, rm, writeFile, readFile } from 'node:fs/promises';
await rm('dist', {recursive:true, force:true});
await mkdir('dist', {recursive:true});
for (const path of ['index.html','assets','archive','sermons']) await cp(path, `dist/${path}`, {recursive:true});
const catalog = JSON.parse(await readFile('assets/sermons/catalog.json','utf8'));
const available = catalog.filter(e=>e.youtube_url);
const archived = catalog.filter(e=>!e.youtube_url);
await writeFile('dist/assets/sermons/catalog.json', JSON.stringify(available));
await writeFile('dist/sermons/catalog-archive/catalog.json', JSON.stringify(archived));
// Browsers cache CSS and JS for four hours. Version their URLs so each HTML
// deployment loads the matching assets, even when an earlier version is cached.
for (const page of ['sermons/index.html','sermons/calendar/index.html','sermons/catalog-archive/index.html']) {
  let html = await readFile(`dist/${page}`, 'utf8');
  const assets = new Set([...html.matchAll(/\/assets\/sermons\/[a-z-]+\.(?:css|js)/g)].map(match=>match[0]));
  for (const asset of assets) {
    const hash = createHash('sha256').update(await readFile(`dist${asset}`)).digest('hex').slice(0,12);
    html = html.replaceAll(asset, `${asset}?v=${hash}`);
  }
  await writeFile(`dist/${page}`, html);
}
await writeFile('dist/_routes.json', JSON.stringify({version:1,include:['/api/sermons/*'],exclude:[]}));
console.log(`Built ${available.length} public YouTube sermons and ${archived.length} unlisted catalog records. No transcription or AI calls.`);
