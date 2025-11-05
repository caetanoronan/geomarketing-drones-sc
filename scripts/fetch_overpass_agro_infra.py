"""Fetch agricultural infrastructure POIs from OSM: cooperatives, agrarian shops, farm supply stores.
Uses Overpass API to find:
- shop=agrarian, shop=farm, shop=trade
- office=cooperative (agricultural cooperatives)
- amenity=fuel + agrarian tags
"""
import requests
import json
import os

OUT_DIR = 'data/osm'
os.makedirs(OUT_DIR, exist_ok=True)

overpass_url = 'https://overpass-api.de/api/interpreter'

# Query for agricultural infrastructure in SC
agro_query = r'''
[out:json][timeout:180];
area["name"="Santa Catarina"][admin_level=4]->.searchArea;
(
  node["shop"~"agrarian|farm|trade"](area.searchArea);
  way["shop"~"agrarian|farm|trade"](area.searchArea);
  relation["shop"~"agrarian|farm|trade"](area.searchArea);
  node["office"="cooperative"](area.searchArea);
  way["office"="cooperative"](area.searchArea);
  relation["office"="cooperative"](area.searchArea);
);
out center;
'''

print('Posting Overpass query for agricultural infrastructure...')
resp = requests.post(overpass_url, data={'data': agro_query}, timeout=600)
resp.raise_for_status()
data = resp.json()

# Save raw JSON
with open(os.path.join(OUT_DIR, 'overpass_agro_infra_sc.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Saved raw JSON with {len(data.get('elements', []))} elements")

# Convert to GeoJSON
features = []
for el in data.get('elements', []):
    geom = None
    if el['type'] == 'node':
        geom = {'type': 'Point', 'coordinates': [el['lon'], el['lat']]}
    else:
        c = el.get('center')
        if c:
            geom = {'type': 'Point', 'coordinates': [c.get('lon'), c.get('lat')]}
    if not geom:
        continue
    props = el.get('tags', {}).copy()
    props['osm_type'] = el['type']
    props['osm_id'] = el.get('id')
    features.append({'type': 'Feature', 'geometry': geom, 'properties': props})

fc = {'type': 'FeatureCollection', 'features': features}
with open(os.path.join(OUT_DIR, 'overpass_agro_infra_sc.geojson'), 'w', encoding='utf-8') as f:
    json.dump(fc, f, ensure_ascii=False, indent=2)
print(f"Saved GeoJSON with {len(features)} features")
print("Done.")
