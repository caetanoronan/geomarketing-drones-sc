"""Fetch agricultural data from IBGE SIDRA API for Santa Catarina municipalities.
Downloads:
- PAM (Produção Agrícola Municipal): area planted + production value by crop
- Censo Agropecuário 2017: number of establishments, area by size class
- PPM (Pesquisa Pecuária Municipal): livestock counts (cattle, pigs, poultry)
"""
import requests
import json
import csv
import os

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

# SIDRA base URL
SIDRA_BASE = 'https://apisidra.ibge.gov.br/values'

# Helper to fetch and save SIDRA table
def fetch_sidra(table_id, variables, territorial_level='6', territorial_ids='4', classifications=None, periods='last', filename='output.json'):
    """
    table_id: SIDRA table number (e.g., '5457' for PAM)
    variables: comma-separated variable codes (e.g., '216,214' for area+quantity)
    territorial_level: 6=municipality, 3=state
    territorial_ids: '4' = Santa Catarina state code for municipalities in SC
    classifications: dict of classification_id: category_code (e.g., {'81':'2692,2691,...'} for crops)
    periods: 'last' or specific years like '2022'
    """
    # Build URL
    url = f"{SIDRA_BASE}/t/{table_id}/n{territorial_level}/{territorial_ids}/v/{variables}/p/{periods}"
    if classifications:
        for cls_id, cats in classifications.items():
            url += f"/c{cls_id}/{cats}"
    
    print(f"Fetching SIDRA table {table_id}...")
    print(f"URL: {url[:150]}...")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} records to {out_path}\n")
    return data

# 1) PAM - Produção Agrícola Municipal (Tabela 5457)
# Variables: 216=Área plantada (ha), 214=Quantidade produzida, 215=Rendimento médio, 112=Valor da produção (mil reais)
# Classification 81 = Produto das lavouras temporárias e permanentes
# Key crops for drones in SC:
# - Arroz (2692), Soja (2711), Milho (2707)
# - Maçã (2762), Uva (2767)
# We'll fetch all crops (code '0' = all), then filter in analysis
print("=" * 60)
print("1) PAM - Produção Agrícola Municipal (últimos dados)")
print("=" * 60)
pam_data = fetch_sidra(
    table_id='5457',
    variables='216,112',  # Área plantada (ha) + Valor da produção (mil R$)
    territorial_level='6',
    territorial_ids='4',  # SC state code for muni filter
    classifications={'81': '0'},  # All crops
    periods='last',
    filename='pam_sc_area_valor.json'
)

# 2) Censo Agropecuário 2017 - Tabela 6727 (Número de estabelecimentos por grupos de área)
# Variable: 184 = Número de estabelecimentos agropecuários
# Classification 220 = Grupos de área total (0-10ha, 10-50, 50-100, 100-500, 500+)
print("=" * 60)
print("2) Censo Agro 2017 - Estabelecimentos por faixa de área")
print("=" * 60)
censo_data = fetch_sidra(
    table_id='6727',
    variables='184',  # Número de estabelecimentos
    territorial_level='6',
    territorial_ids='4',
    classifications={'220': '0'},  # All size classes (will get breakdown)
    periods='2017',
    filename='censo_agro_2017_estabelecimentos.json'
)

# 3) PPM - Pesquisa Pecuária Municipal (Tabela 3939)
# Variables: 284=Efetivo dos rebanhos (número de cabeças)
# Classification 79 = Tipo de rebanho: Bovino (2664), Suíno (2665), Galináceos (2667), etc.
print("=" * 60)
print("3) PPM - Pesquisa Pecuária Municipal (últimos dados)")
print("=" * 60)
ppm_data = fetch_sidra(
    table_id='3939',
    variables='284',  # Efetivo dos rebanhos (cabeças)
    territorial_level='6',
    territorial_ids='4',
    classifications={'79': '2664,2665,2667'},  # Bovino, Suíno, Galináceos (aves)
    periods='last',
    filename='ppm_sc_rebanhos.json'
)

print("=" * 60)
print("All SIDRA data fetched successfully!")
print(f"Files saved to: {OUT_DIR}/")
print("=" * 60)
