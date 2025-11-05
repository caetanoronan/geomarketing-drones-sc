"""Convert a specific layer from a GeoPackage to GeoJSON using geopandas.
Usage: python convert_gpkg_to_geojson.py --gpkg <path> --layer <layername> --out <out.geojson>
"""
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--gpkg', default=r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Geomarkenting\SC_setores_CD2022.gpkg')
parser.add_argument('--layer', default='SC_setores_CD2022')
parser.add_argument('--out', default=r'data/SC_setores_CD2022.geojson')
args = parser.parse_args()

if not os.path.isfile(args.gpkg):
    raise SystemExit(f"GeoPackage not found: {args.gpkg}")

import geopandas as gpd

print(f"Reading layer '{args.layer}' from {args.gpkg}...")
gdf = gpd.read_file(args.gpkg, layer=args.layer)
print(f"Loaded {len(gdf)} features; CRS={gdf.crs}")

out_dir = os.path.dirname(args.out)
if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir, exist_ok=True)

print(f"Saving to {args.out} (GeoJSON)...")
gdf.to_file(args.out, driver='GeoJSON')
print('Done.')
