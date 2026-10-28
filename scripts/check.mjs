import assert from 'node:assert/strict';
import fs from 'node:fs';
import {filterPlaces} from '../src/lib.js';
const seeds=JSON.parse(fs.readFileSync(new URL('../src/data/seed.json',import.meta.url)));
const data=JSON.parse(fs.readFileSync(new URL('../src/data/places.json',import.meta.url)));
assert.equal(data.length,seeds.length); assert.equal(new Set(data.map(p=>p.id)).size,data.length);
assert.equal(new Set(data.map(p=>p.continent)).size,6);
for(const p of data){
 for(const field of ['name','continent','country','province','city','category','intro','image','sourceUrl']) assert(p[field],`${p.id}: ${field}`);
 assert(['人文','古迹','自然风光'].includes(p.category)); assert(p.photo.author&&p.photo.license&&p.photo.page);
 assert(fs.statSync(new URL('../public'+p.image,import.meta.url)).size>10000,p.image);
}
const filters={search:'',continent:'',country:'',province:'',city:'',category:''};
assert.equal(filterPlaces(data,filters).length,data.length);
assert.deepEqual(filterPlaces(data,{...filters,country:'中国',province:'四川',city:'阿坝'}).map(p=>p.id),['jiuzhaigou']);
assert(filterPlaces(data,{...filters,continent:'欧洲',category:'古迹'}).every(p=>p.continent==='欧洲'&&p.category==='古迹'));
assert.deepEqual(filterPlaces(data,{...filters,search:'  MOUNT FUJI  '}).map(p=>p.id),['fuji']);
assert.equal(filterPlaces(data,{...filters,continent:'欧洲',country:'中国'}).length,0);
console.log(`Verified ${data.length} unique destinations, 6 continents, taxonomy, sources, licenses, and local assets.`);
