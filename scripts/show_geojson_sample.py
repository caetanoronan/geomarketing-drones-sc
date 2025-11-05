"""Print fields and the first N feature properties from a GeoJSON file.
Usage: python show_geojson_sample.py --geojson data/SC_setores_CD2022.geojson --n 10
"""
import argparse
import json
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('--geojson', default=r'data/SC_setores_CD2022.geojson')
parser.add_argument('--n', type=int, default=10)
args = parser.parse_args()

print(f"Loading GeoJSON (may be large): {args.geojson}")
with open(args.geojson, 'r', encoding='utf-8') as f:
    gj = json.load(f)

features = gj.get('features', [])
print(f"Total features: {len(features)}")

# Collect field names from properties
field_names = set()
for feat in itertools.islice(features, 0, min(len(features), 200)):
    props = feat.get('properties', {})
    field_names.update(props.keys())

print('\nDetected property fields (sampled from first 200 features):')
for fn in sorted(field_names):
    print(' -', fn)

print(f"\nShowing first {args.n} feature properties:\n")
for i, feat in enumerate(itertools.islice(features, args.n), 1):
    props = feat.get('properties', {})
    print(f"Feature {i}:")
    # print a compact view
    for k, v in list(props.items())[:20]:
        print(f"  {k}: {v}")
    # show geometry type and bbox if present
    geom = feat.get('geometry')
    if geom:
        print(f"  geometry.type: {geom.get('type')}")
    print()

print('Done.')
