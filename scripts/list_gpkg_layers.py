#!/usr/bin/env python3
"""List layers in a GeoPackage by querying its gpkg_contents table using sqlite3.
Usage: python list_gpkg_layers.py --gpkg "C:\path\to\file.gpkg"
"""
import argparse
import sqlite3
import json
import os

parser = argparse.ArgumentParser(description='List layers inside a GeoPackage (.gpkg)')
parser.add_argument('--gpkg', required=False, help='Path to .gpkg file',
                    default=r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Geomarkenting\SC_setores_CD2022.gpkg')
parser.add_argument('--out', required=False, help='Optional JSON output file to save layer list')
args = parser.parse_args()

gpkg_path = args.gpkg
if not os.path.isfile(gpkg_path):
    raise SystemExit(f"GeoPackage not found: {gpkg_path}")

conn = sqlite3.connect(gpkg_path)
cur = conn.cursor()

# gpkg_contents standard table lists offered tables/layers
cur.execute("SELECT table_name, identifier, description, data_type FROM gpkg_contents")
rows = cur.fetchall()

layers = []
for r in rows:
    table_name, identifier, description, data_type = r
    layers.append({
        'table_name': table_name,
        'identifier': identifier,
        'description': description,
        'data_type': data_type,
    })

# Try to get geometry column info where applicable
geom_info = {}
cur.execute("SELECT table_name, column_name, geometry_type_name, srs_id, z, m FROM gpkg_geometry_columns")
for table_name, column_name, geom_type, srs_id, z, m in cur.fetchall():
    geom_info[table_name] = {
        'column_name': column_name,
        'geometry_type_name': geom_type,
        'srs_id': srs_id,
        'z': z,
        'm': m,
    }

# Merge geom info
for layer in layers:
    if layer['table_name'] in geom_info:
        layer['geometry'] = geom_info[layer['table_name']]

conn.close()

# Print a readable list
if not layers:
    print('No entries found in gpkg_contents — file may be empty or not a valid GeoPackage.')
else:
    print(f"Found {len(layers)} layer(s) in: {gpkg_path}\n")
    for i, l in enumerate(layers, 1):
        print(f"{i}. table_name: {l['table_name']}")
        if l.get('identifier'):
            print(f"   identifier: {l['identifier']}")
        if l.get('description'):
            print(f"   description: {l['description']}")
        print(f"   data_type: {l.get('data_type')}")
        if 'geometry' in l:
            g = l['geometry']
            print(f"   geometry column: {g['column_name']} ({g['geometry_type_name']}) srs_id={g['srs_id']} z={g['z']} m={g['m']}")
        print()

# Optionally save JSON
if args.out:
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(layers, f, ensure_ascii=False, indent=2)
    print(f"Saved layer list to {args.out}")
