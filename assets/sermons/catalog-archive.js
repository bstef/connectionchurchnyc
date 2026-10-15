const input=document.getElementById('archive-query');
const count=document.getElementById('archive-count');
const results=document.getElementById('archive-results');
let records=[];
function element(tag,text,cls){const el=document.createElement(tag);el.textContent=text;if(cls)el.className=cls;return el;}
function render(){
  const terms=input.value.toLocaleLowerCase().match(/[\p{L}\p{N}]+/gu)||[];
  const matches=records.filter(e=>terms.every(t=>(e.title+' '+e.description+' '+e.speaker+' '+e.date).toLocaleLowerCase().includes(t)));
  count.textContent=`${matches.length} of ${records.length} preserved records · recording unavailable`;
  results.replaceChildren();
  for(const e of matches){
    const article=document.createElement('article');article.className='archive-card';
    const body=document.createElement('div');body.append(element('h3',e.title),element('p',e.date+(e.speaker?' · '+e.speaker:''),'meta'),element('p',e.description,'catalogue-excerpt'));
    const source=element('a','Original catalog listing ↗','source-link');source.href=e.link;source.target='_blank';source.rel='noopener';body.append(source);article.append(body);results.append(article);
  }
  if(!matches.length)results.append(element('p','No matching preserved records.','empty'));
}
input.addEventListener('input',render);
(async()=>{try{const response=await fetch('/sermons/catalog-archive/catalog.json');if(!response.ok)throw new Error();records=await response.json();render();}catch{count.textContent='The preserved catalog could not be loaded. Refresh to try again.';}})();
