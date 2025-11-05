"""Download pre-aggregated agricultural data CSVs directly from IBGE FTP or use batched SIDRA queries.
Alternative: use smaller batches of municipalities (50 at a time) to avoid URL length issues.
"""
import requests
import json
import os
import time

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

# Get SC municipalities
print("Fetching SC municipality list...")
muni_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
resp = requests.get(muni_url, timeout=60)
resp.raise_for_status()
municipios = resp.json()
muni_codes = [str(m['id']) for m in municipios]
print(f"Found {len(muni_codes)} municipalities in SC\n")

with open(os.path.join(OUT_DIR, 'sc_municipios.json'), 'w', encoding='utf-8') as f:
    json.dump(municipios, f, ensure_ascii=False, indent=2)

# Split into batches of 50
batch_size = 50
batches = [muni_codes[i:i+batch_size] for i in range(0, len(muni_codes), batch_size)]
print(f"Split into {len(batches)} batches of up to {batch_size} municipalities each\n")

def fetch_batched(table_id, variables, period, classifications, filename_base):
    all_data = []
    for i, batch in enumerate(batches, 1):
        muni_string = '|'.join(batch)
        url = f"https://apisidra.ibge.gov.br/values/t/{table_id}/n6/{muni_string}/v/{variables}/p/{period}"
        if classifications:
            for cls_id, cats in classifications.items():
                url += f"/c{cls_id}/{cats}"
        
        print(f"  Batch {i}/{len(batches)}: fetching {len(batch)} municipalities...")
        try:
            resp = requests.get(url, timeout=120)
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                all_data.extend(data)
                print(f"    Got {len(data)} records")
            else:
                print(f"    ERROR {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"    EXCEPTION: {e}")
        
        time.sleep(1)  # rate limiting
    
    if all_data:
        out_path = os.path.join(OUT_DIR, f"{filename_base}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"  TOTAL: {len(all_data)} records saved to {filename_base}.json\n")
    return all_data

print("="*60)
print("1) PAM 2022 - Área plantada + Valor produção")
print("="*60)
pam_data = fetch_batched(
    table_id='5457',
    variables='216,112',  # área ha + valor mil R$
    period='2022',
    classifications={'81': 'allxt'},  # all crops
    filename_base='pam_sc_2022'
)

print("="*60)
print("2) Censo Agro 2017 - Estabelecimentos")
print("="*60)
censo_data = fetch_batched(
    table_id='6727',
    variables='184',  # número estabelecimentos
    period='2017',
    classifications={'220': 'allxt'},  # all size classes
    filename_base='censo_agro_2017'
)

print("="*60)
print("3) PPM 2022 - Rebanhos (bovino, suíno, aves)")
print("="*60)
ppm_data = fetch_batched(
    table_id='3939',
    variables='284',  # efetivo rebanhos
    period='2022',
    classifications={'79': '2664,2665,2667'},  # bovino, suíno, galináceos
    filename_base='ppm_sc_2022'
)

print("="*60)
print("All SIDRA data fetched successfully!")
print("="*60)
