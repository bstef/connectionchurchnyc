import { cp, mkdir, rm, writeFile } from 'node:fs/promises';
await rm('dist', {recursive:true, force:true});
await mkdir('dist', {recursive:true});
for (const path of ['index.html','assets','archive','sermons']) await cp(path, `dist/${path}`, {recursive:true});
await writeFile('dist/_routes.json', JSON.stringify({version:1,include:['/api/sermons/*'],exclude:[]}));
console.log('Built church site and Connection sermon archive. No transcription or AI calls.');
