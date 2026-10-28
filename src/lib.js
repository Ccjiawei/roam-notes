export function readStore(key, fallback, validate) {
  try { const data = JSON.parse(localStorage.getItem(key)); return validate(data) ? data : fallback; }
  catch { return fallback; }
}
export function filterPlaces(places, filters) {
  const q=filters.search.trim().toLocaleLowerCase();
  return places.filter(p => (!filters.continent || p.continent===filters.continent) && (!filters.country || p.country===filters.country) && (!filters.province || p.province===filters.province) && (!filters.city || p.city===filters.city) && (!filters.category || p.category===filters.category) && (!q || [p.name,p.english,p.country,p.province,p.city,...p.tags].join(' ').toLocaleLowerCase().includes(q)));
}
export function unique(items,field){return [...new Set(items.map(p=>p[field]))];}
export function today(){ const d=new Date(); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`; }
