"""Fetch two Overpass queries (tag-based and name-based) for Santa Catarina and save GeoJSONs.
Outputs:
 - data/osm/overpass_tag_sc.geojson
 - data/osm/overpass_name_sc.geojson
"""
import requests
import json
import os

OUT_DIR = 'data/osm'
os.makedirs(OUT_DIR, exist_ok=True)

overpass_url = 'https://overpass-api.de/api/interpreter'

# tag-based query: shops and hotels
tag_query = r'''
[out:json][timeout:180];
area["name"="Santa Catarina"][admin_level=4]->.searchArea;
(
  node["shop"~"^(electronics|computer|photo|hobby|car_repair|tools)$"](area.searchArea);
  way["shop"~"^(electronics|computer|photo|hobby|car_repair|tools)$"](area.searchArea);
  relation["shop"~"^(electronics|computer|photo|hobby|car_repair|tools)$"](area.searchArea);
  node["tourism"="hotel"](area.searchArea);
  way["tourism"="hotel"](area.searchArea);
  relation["tourism"="hotel"](area.searchArea);
);
out center;
'''

# name-based query: drone-related keywords (case-insensitive where supported)
name_query = r'''
[out:json][timeout:180];
area["name"="Santa Catarina"][admin_level=4]->.searchArea;
(
  node["name"~"(?i)drone|dji|mavic|phantom|fpv|aerofotografia|fotogrametria|aluguel|locador|locadora"](area.searchArea);
  way["name"~"(?i)drone|dji|mavic|phantom|fpv|aerofotografia|fotogrametria|aluguel|locador|locadora"](area.searchArea);
  relation["name"~"(?i)drone|dji|mavic|phantom|fpv|aerofotografia|fotogrametria|aluguel|locador|locadora"](area.searchArea);
);
out center;
'''

def fetch_and_save(query, out_json, out_geojson):
    print('Posting query to Overpass...')
    resp = requests.post(overpass_url, data={'data': query}, timeout=600)
    resp.raise_for_status()
    data = resp.json()
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print('Saved raw JSON to', out_json)
    # convert to GeoJSON FeatureCollection (points) using node lat/lon or way/relation center
    features = []
    for el in data.get('elements', []):
        geom = None
        if el['type'] == 'node':
            geom = {'type':'Point', 'coordinates': [el['lon'], el['lat']]}
        else:
            # ways/relations with center
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
    with open(out_geojson, 'w', encoding='utf-8') as f:
        json.dump(fc, f, ensure_ascii=False)
    print('Saved GeoJSON to', out_geojson, 'with', len(features), 'features')

if __name__ == '__main__':
    fetch_and_save(tag_query, os.path.join(OUT_DIR,'overpass_tag_sc.json'), os.path.join(OUT_DIR,'overpass_tag_sc.geojson'))
    fetch_and_save(name_query, os.path.join(OUT_DIR,'overpass_name_sc.json'), os.path.join(OUT_DIR,'overpass_name_sc.geojson'))
    print('All done.')
