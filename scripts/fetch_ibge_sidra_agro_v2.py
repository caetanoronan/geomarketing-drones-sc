"""Fetch agricultural data from IBGE SIDRA API for Santa Catarina municipalities.
Updated approach: use 'all' territorial filter for municipalities in SC (IBGE returns all SC munis automatically when we filter by state in classifications or use proper N-level syntax).
"""
import requests
import json
import os

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

SIDRA_BASE = 'https://apisidra.ibge.gov.br/values'

def fetch_sidra(table_id, variables, territorial, classifications=None, periods='last', filename='output.json'):
    """
    territorial: e.g. 'n6/N3[4]' means municipalities (n6) in state 4 (SC)
    """
    url = f"{SIDRA_BASE}/t/{table_id}/{territorial}/v/{variables}/p/{periods}"
    if classifications:
        for cls_id, cats in classifications.items():
            url += f"/c{cls_id}/{cats}"
    
    print(f"Fetching SIDRA table {table_id}...")
    print(f"URL: {url}")
    resp = requests.get(url, timeout=180)
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code} - {resp.text[:500]}")
        return None
    data = resp.json()
    
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} records to {out_path}\n")
    return data

print("="*60)
print("1) PAM - Área plantada + Valor produção (2022)")
print("="*60)
# Tabela 5457, Variables 216 (área ha) + 112 (valor mil R$), all crops, SC municipalities
pam = fetch_sidra(
    table_id='5457',
    variables='216,112',
    territorial='n6/N3[4]',  # municipalities in state 4 (SC)
    classifications={'81':'allxt'},  # all crops
    periods='2022',
    filename='pam_sc_2022.json'
)

print("="*60)
print("2) Censo Agro 2017 - Estabelecimentos + Área")
print("="*60)
# Tabela 6727, Variable 184 (número de estabelecimentos), all size classes, SC
censo = fetch_sidra(
    table_id='6727',
    variables='184',
    territorial='n6/N3[4]',
    classifications={'220':'allxt'},  # all size classes
    periods='2017',
    filename='censo_agro_2017.json'
)

print("="*60)
print("3) PPM - Rebanhos bovino/suíno/aves (2022)")
print("="*60)
# Tabela 3939, Variable 284 (efetivo rebanhos), bovino+suíno+galináceos, SC
ppm = fetch_sidra(
    table_id='3939',
    variables='284',
    territorial='n6/N3[4]',
    classifications={'79':'2664,2665,2667'},  # bovino, suíno, galináceos
    periods='2022',
    filename='ppm_sc_2022.json'
)

print("="*60)
print("All done!")
