"""Aggregate POIs (Overpass GeoJSON) by sector polygons (GeoJSON).
Outputs a CSV with counts per sector.
Usage:
  python aggregate_pois_by_sector.py --sectors data/SC_setores_CD2022.geojson \
    --pois data/osm/overpass_tag_sc.geojson data/osm/overpass_name_sc.geojson \
    --out data/outputs/sectors_poi_counts.csv
"""
import argparse
import json
import os
import csv
from shapely.geometry import shape, Point
from shapely.prepared import prep

parser = argparse.ArgumentParser()
parser.add_argument('--sectors', required=False, default=r'data/SC_setores_CD2022.geojson')
parser.add_argument('--pois', nargs='+', required=False, default=[r'data/osm/overpass_tag_sc.geojson', r'data/osm/overpass_name_sc.geojson'])
parser.add_argument('--out', required=False, default=r'data/outputs/sectors_poi_counts.csv')
args = parser.parse_args()

if not os.path.isfile(args.sectors):
    raise SystemExit(f"Sectors GeoJSON not found: {args.sectors}")
for p in args.pois:
    if not os.path.isfile(p):
        raise SystemExit(f"POI GeoJSON not found: {p}")

print('Loading sectors...')
with open(args.sectors, 'r', encoding='utf-8') as f:
    sectors_gj = json.load(f)
sectors = sectors_gj.get('features', [])
print(f"Sectors features: {len(sectors)}")

# Build list of sector geometries and props
sector_geoms = []
for feat in sectors:
    geom = feat.get('geometry')
    if not geom:
        sector_geoms.append((None, feat.get('properties', {})))
        continue
    poly = shape(geom)
    sector_geoms.append((prep(poly), poly, feat.get('properties', {})))

# Initialize counts dict keyed by CD_SETOR or index
counts = {}
for i, entry in enumerate(sector_geoms):
    props = entry[-1]
    key = props.get('CD_SETOR') or props.get('CD_SETOR') or f'idx_{i}'
    counts[key] = {
        'CD_SETOR': props.get('CD_SETOR'),
        'CD_MUN': props.get('CD_MUN'),
        'NM_MUN': props.get('NM_MUN'),
        'AREA_KM2': props.get('AREA_KM2'),
        'count_total': 0,
        'count_tag_pois': 0,
        'count_name_pois': 0,
        'sample_poi_names': set(),
    }

# helper to assign a point to a sector index
def find_sector_index(pt):
    # iterate and return the key of the first sector that contains point
    for idx, entry in enumerate(sector_geoms):
        if entry[0] is None:
            continue
        prepared, poly, props = entry
        if prepared.contains(pt):
            key = props.get('CD_SETOR') or f'idx_{idx}'
            return key
    return None

# tokens to detect drone-related names (case-insensitive)
DRONE_TOKENS = ['drone','drones','aerofoto','aerofotografia','fotogrametria','fpv','dji','mavic','phantom','aluguel','locadora','locacao','locadora','locador','dronecenter','drone shop']

print('Processing POI files...')
for poi_path in args.pois:
    name_category = 'tag' if 'tag' in os.path.basename(poi_path) else 'name'
    print(' -', os.path.basename(poi_path), 'as', name_category)
    with open(poi_path, 'r', encoding='utf-8') as f:
        gj = json.load(f)
    features = gj.get('features', [])
    for feat in features:
        geom = feat.get('geometry')
        if not geom:
            continue
        try:
            pt = shape(geom)
        except Exception:
            continue
        if not pt.is_empty:
            key = find_sector_index(pt)
            if not key:
                continue
            counts[key]['count_total'] += 1
            # increment category-specific
            if name_category == 'tag':
                counts[key]['count_tag_pois'] += 1
            else:
                counts[key]['count_name_pois'] += 1
            # sample name if available
            props = feat.get('properties', {})
            name = props.get('name') or props.get('tags', {}).get('name') if isinstance(props.get('tags'), dict) else props.get('name')
            if name:
                counts[key]['sample_poi_names'].add(name)
            # detect drone keywords
            lower_name = (name or '').lower()
            if any(tok in lower_name for tok in DRONE_TOKENS):
                counts[key].setdefault('count_drone_named', 0)
                counts[key]['count_drone_named'] += 1

# Prepare output dir
out_dir = os.path.dirname(args.out)
if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir, exist_ok=True)

print('Writing CSV...')
with open(args.out, 'w', encoding='utf-8', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['CD_SETOR','CD_MUN','NM_MUN','AREA_KM2','count_total','count_tag_pois','count_name_pois','count_drone_named','sample_poi_names'])
    for key, vals in counts.items():
        sample = ';'.join(list(vals['sample_poi_names'])[:5])
        writer.writerow([
            vals.get('CD_SETOR'),
            vals.get('CD_MUN'),
            vals.get('NM_MUN'),
            vals.get('AREA_KM2'),
            vals.get('count_total',0),
            vals.get('count_tag_pois',0),
            vals.get('count_name_pois',0),
            vals.get('count_drone_named',0),
            sample,
        ])

print('Done. CSV saved to', args.out)
