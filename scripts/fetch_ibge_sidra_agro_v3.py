"""Fetch IBGE SIDRA agricultural data using simpler 'all' syntax for SC municipalities.
SIDRA syntax: n6/all filters to all municipalities; we add state filter via D3C classification.
Alternative: fetch via CSV download URLs that are more stable.
"""
import requests
import json
import os
import time

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

# Try direct CSV download URLs (more reliable than JSON API for complex queries)
# SIDRA allows CSV export via /t/{table}/...?formato=csv

def download_sidra_csv(url, filename):
    print(f"Downloading {filename}...")
    print(f"URL: {url[:100]}...")
    resp = requests.get(url, timeout=180)
    if resp.status_code != 200:
        print(f"ERROR {resp.status_code}: {resp.text[:300]}")
        return False
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, 'wb') as f:
        f.write(resp.content)
    lines = len(resp.content.decode('latin-1', errors='ignore').split('\n'))
    print(f"Saved {filename} ({lines} lines)\n")
    return True

# PAM 2022: Área plantada e valor da produção, todas as culturas, todos municípios SC
# Tabela 5457, Var 216+112, período 2022, municípios (N6), filtrar SC via interface web params
# SIDRA web interface generates URLs like this (example):
# https://sidra.ibge.gov.br/geratabela?format=xlsx&name=t5457.xlsx&terr=NC&rank=-&query=t/5457/n6/all/v/216,112/p/2022/c81/allxt/l/v,,p+c81

print("="*60)
print("Attempting PAM download via SIDRA table export...")
print("="*60)

# Build CSV export URL for PAM table 5457
# Format: https://apisidra.ibge.gov.br/values/t/{table}/n{level}/{ids}/v/{vars}/p/{period}/c{class}/{cats}?formato=csv
pam_url = "https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216,112/p/2022/c81/allxt/d/v216%201,v112%201?formato=csv&territorial=n1%5Ball%5D"

# Simpler approach: use the metadados endpoint to get municipality codes for SC, then query explicitly
print("Fetching SC municipality codes first...")
muni_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
resp = requests.get(muni_url, timeout=60)
resp.raise_for_status()
municipios = resp.json()
muni_codes = [str(m['id']) for m in municipios]
print(f"Found {len(muni_codes)} municipalities in SC")

# Save municipality list
with open(os.path.join(OUT_DIR, 'sc_municipios.json'), 'w', encoding='utf-8') as f:
    json.dump(municipios, f, ensure_ascii=False, indent=2)

# Now build SIDRA queries with explicit muni codes (max ~295 municipalities)
# SIDRA n6 format: n6/4200051|4200101|... (pipe-separated codes)
muni_string = '|'.join(muni_codes)

print("\n" + "="*60)
print("1) PAM 2022 - Área plantada + Valor produção")
print("="*60)
pam_url_fixed = f"https://apisidra.ibge.gov.br/values/t/5457/n6/{muni_string}/v/216,112/p/2022/c81/allxt"
print(f"Fetching PAM data for {len(muni_codes)} municipalities...")
print(f"URL length: {len(pam_url_fixed)}")
resp_pam = requests.get(pam_url_fixed, timeout=300)
if resp_pam.status_code == 200:
    data_pam = resp_pam.json()
    with open(os.path.join(OUT_DIR, 'pam_sc_2022.json'), 'w', encoding='utf-8') as f:
        json.dump(data_pam, f, ensure_ascii=False, indent=2)
    print(f"PAM: saved {len(data_pam)} records\n")
else:
    print(f"PAM ERROR {resp_pam.status_code}: {resp_pam.text[:500]}\n")

time.sleep(2)

print("="*60)
print("2) Censo Agro 2017 - Estabelecimentos por faixa área")
print("="*60)
censo_url = f"https://apisidra.ibge.gov.br/values/t/6727/n6/{muni_string}/v/184/p/2017/c220/allxt"
resp_censo = requests.get(censo_url, timeout=300)
if resp_censo.status_code == 200:
    data_censo = resp_censo.json()
    with open(os.path.join(OUT_DIR, 'censo_agro_2017.json'), 'w', encoding='utf-8') as f:
        json.dump(data_censo, f, ensure_ascii=False, indent=2)
    print(f"Censo: saved {len(data_censo)} records\n")
else:
    print(f"Censo ERROR {resp_censo.status_code}: {resp_censo.text[:500]}\n")

time.sleep(2)

print("="*60)
print("3) PPM 2022 - Rebanhos (bovino, suíno, aves)")
print("="*60)
ppm_url = f"https://apisidra.ibge.gov.br/values/t/3939/n6/{muni_string}/v/284/p/2022/c79/2664,2665,2667"
resp_ppm = requests.get(ppm_url, timeout=300)
if resp_ppm.status_code == 200:
    data_ppm = resp_ppm.json()
    with open(os.path.join(OUT_DIR, 'ppm_sc_2022.json'), 'w', encoding='utf-8') as f:
        json.dump(data_ppm, f, ensure_ascii=False, indent=2)
    print(f"PPM: saved {len(data_ppm)} records\n")
else:
    print(f"PPM ERROR {resp_ppm.status_code}: {resp_ppm.text[:500]}\n")

print("="*60)
print("Done fetching SIDRA data!")
print("="*60)
