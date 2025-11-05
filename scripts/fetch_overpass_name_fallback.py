import requests, json, os
OUT_DIR = 'data/osm'
os.makedirs(OUT_DIR, exist_ok=True)
overpass_url = 'https://overpass-api.de/api/interpreter'
name_query2 = r'''
[out:json][timeout:180];
area["name"="Santa Catarina"][admin_level=4]->.searchArea;
(
  node["name"~"drone|Drone|DRONE|dji|DJI|mavic|Mavic|MAVIC|phantom|PHANTOM|fpv|FPV|aerofotografia|Aerofotografia|fotogrametria|Fotogrametria|aluguel|Aluguel|locadora|Locadora"](area.searchArea);
  way["name"~"drone|Drone|DRONE|dji|DJI|mavic|Mavic|MAVIC|phantom|PHANTOM|fpv|FPV|aerofotografia|Aerofotografia|fotogrametria|Fotogrametria|aluguel|Aluguel|locadora|Locadora"](area.searchArea);
  relation["name"~"drone|Drone|DRONE|dji|DJI|mavic|Mavic|MAVIC|phantom|PHANTOM|fpv|FPV|aerofotografia|Aerofotografia|fotogrametria|Fotogrametria|aluguel|Aluguel|locadora|Locadora"](area.searchArea);
);
out center;
'''
print('Posting fallback name query...')
resp = requests.post(overpass_url, data={'data': name_query2}, timeout=600)
resp.raise_for_status()
data = resp.json()
with open(os.path.join(OUT_DIR,'overpass_name_sc.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
# convert
features = []
for el in data.get('elements', []):
    geom = None
    if el['type'] == 'node':
        geom = {'type':'Point', 'coordinates': [el['lon'], el['lat']]}
    else:
        c = el.get('center')
        if c:
            geom = {'type':'Point', 'coordinates': [c.get('lon'), c.get('lat')]}
    if not geom:
        continue
    props = el.get('tags', {}).copy()
    props['osm_type'] = el['type']
    props['osm_id'] = el.get('id')
    features.append({'type':'Feature','geometry':geom,'properties':props})
fc = {'type':'FeatureCollection','features':features}
with open(os.path.join(OUT_DIR,'overpass_name_sc.geojson'), 'w', encoding='utf-8') as f:
    json.dump(fc, f, ensure_ascii=False)
print('Saved fallback name GeoJSON with', len(features), 'features')
