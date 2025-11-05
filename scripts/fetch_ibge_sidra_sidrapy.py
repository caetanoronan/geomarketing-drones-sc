"""Use sidrapy package to fetch agricultural data for SC municipalities.
sidrapy handles the SIDRA API syntax automatically.
"""
import sidrapy
import pandas as pd
import json
import os

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

# Get SC municipality codes
import requests
muni_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
resp = requests.get(muni_url, timeout=60)
resp.raise_for_status()
municipios = resp.json()
print(f"Found {len(municipios)} municipalities in SC\n")

# sidrapy.get_table(table_code, territorial_level, ibge_territorial_code, variable, classifications, period)
# territorial_level: '6' = municipality
# ibge_territorial_code: comma-separated codes like '4200051,4200101,...' OR 'all' with state filter

print("="*60)
print("1) PAM 2022 - Área plantada (ha) + Valor produção (mil R$)")
print("="*60)
try:
    # Table 5457, Variables 216 (área) + 112 (valor), period 2022, all crops (classification 81)
    # Fetch for state SC (code 42) at municipality level
    df_pam = sidrapy.get_table(
        table_code='5457',
        territorial_level='6',  # municipality
        ibge_territorial_code='4',  # state code 42 → filter municipalities in SC
        variable='216,112',  # área plantada + valor produção
        classifications={'81': 'allxt'},  # all crops
        period='2022'
    )
    print(f"PAM: fetched {len(df_pam)} rows")
    df_pam.to_csv(os.path.join(OUT_DIR, 'pam_sc_2022.csv'), index=False, encoding='utf-8-sig')
    df_pam.to_json(os.path.join(OUT_DIR, 'pam_sc_2022_df.json'), orient='records', force_ascii=False, indent=2)
    print(f"Saved to pam_sc_2022.csv and .json\n")
except Exception as e:
    print(f"PAM ERROR: {e}\n")

print("="*60)
print("2) Censo Agro 2017 - Estabelecimentos por faixa de área")
print("="*60)
try:
    # Table 6727, Variable 184 (número estabelecimentos), classification 220 (size classes)
    df_censo = sidrapy.get_table(
        table_code='6727',
        territorial_level='6',
        ibge_territorial_code='4',
        variable='184',
        classifications={'220': 'allxt'},
        period='2017'
    )
    print(f"Censo Agro: fetched {len(df_censo)} rows")
    df_censo.to_csv(os.path.join(OUT_DIR, 'censo_agro_2017.csv'), index=False, encoding='utf-8-sig')
    df_censo.to_json(os.path.join(OUT_DIR, 'censo_agro_2017_df.json'), orient='records', force_ascii=False, indent=2)
    print(f"Saved to censo_agro_2017.csv and .json\n")
except Exception as e:
    print(f"Censo ERROR: {e}\n")

print("="*60)
print("3) PPM 2022 - Rebanhos (bovino, suíno, aves)")
print("="*60)
try:
    # Table 3939, Variable 284 (efetivo rebanhos), classification 79 (livestock types)
    df_ppm = sidrapy.get_table(
        table_code='3939',
        territorial_level='6',
        ibge_territorial_code='4',
        variable='284',
        classifications={'79': '2664,2665,2667'},  # bovino, suíno, galináceos
        period='2022'
    )
    print(f"PPM: fetched {len(df_ppm)} rows")
    df_ppm.to_csv(os.path.join(OUT_DIR, 'ppm_sc_2022.csv'), index=False, encoding='utf-8-sig')
    df_ppm.to_json(os.path.join(OUT_DIR, 'ppm_sc_2022_df.json'), orient='records', force_ascii=False, indent=2)
    print(f"Saved to ppm_sc_2022.csv and .json\n")
except Exception as e:
    print(f"PPM ERROR: {e}\n")

print("="*60)
print("All done! Data saved to", OUT_DIR)
print("="*60)
