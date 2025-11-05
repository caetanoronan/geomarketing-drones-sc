import shapefile
import json
import os

BASE_DIR = r"C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Geomarkenting"
INPUT_DIR = os.path.join(BASE_DIR, 'bc25_sc_shapefile_2020-10-01')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'bc25_geojson')

os.makedirs(OUTPUT_DIR, exist_ok=True)

layers = [
    'aer_pista_ponto_pouso_a',
    'aer_pista_ponto_pouso_l',
    'aer_pista_ponto_pouso_p',
    'tra_caminho_aereo_l',
    'enc_torre_energia_p',
    'enc_trecho_energia_l',
    'edf_edificacao_a',
    'edf_edificacao_p',
    'cbge_area_uso_especifico_a',
    'lml_area_densamente_edificada_a',
    'lml_municipio_a'
]

results = {}
for layer in layers:
    shp_path = os.path.join(INPUT_DIR, f"{layer}.shp")
    out_path = os.path.join(OUTPUT_DIR, f"{layer}.geojson")
    try:
        if not os.path.exists(shp_path):
            results[layer] = f"MISSING: {shp_path}"
            continue
        sf = shapefile.Reader(shp_path)
        fields = [f[0] for f in sf.fields[1:]]
        features = []
        for sr in sf.iterShapeRecords():
            shape = sr.shape
            record = sr.record
            props = dict(zip(fields, record))
            geom = shape.__geo_interface__
            feature = {
                'type': 'Feature',
                'geometry': geom,
                'properties': props
            }
            features.append(feature)
        fc = {
            'type': 'FeatureCollection',
            'features': features
        }
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(fc, f, ensure_ascii=False)
        results[layer] = f"OK -> {out_path} (features: {len(features)})"
    except Exception as e:
        results[layer] = f"ERROR: {str(e)}"

print('Conversion results:')
for k, v in results.items():
    print(f'{k}: {v}')

print('\nDone.')
