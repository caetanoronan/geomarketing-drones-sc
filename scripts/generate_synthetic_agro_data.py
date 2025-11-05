"""Generate synthetic but realistic agricultural data for SC municipalities for demonstration.
Based on known characteristics of SC regions:
- Oeste: high pig/poultry production, corn/soy
- Serra: apple orchards, forestry
- Sul/Vale: rice paddies
- Vale do Itajaí: mixed farming
This allows us to demonstrate the full geomarketing methodology while IBGE data downloads are sorted out.
"""
import pandas as pd
import json
import os
import random

OUT_DIR = 'data/ibge_agro'
os.makedirs(OUT_DIR, exist_ok=True)

# Load SC municipalities
import requests
muni_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
resp = requests.get(muni_url, timeout=60)
resp.raise_for_status()
municipios = resp.json()
print(f"Generating synthetic agro data for {len(municipios)} SC municipalities\n")

# Regional profiles (mesoregions approximate)
# Oeste: Chapecó, Concórdia, Xanxerê, São Miguel do Oeste
# Grande Florianópolis: Florianópolis, São José, Palhoça
# Norte: Joinville, Jaraguá do Sul, Mafra
# Sul: Criciúma, Araranguá, Tubarão
# Serrana: Lages, São Joaquim, Campos Novos
# Vale do Itajaí: Blumenau, Brusque, Itajaí

oeste_keywords = ['chapecó', 'concórdia', 'xanxerê', 'são miguel', 'maravilha', 'quilombo', 'palmitos']
serrana_keywords = ['lages', 'são joaquim', 'campos novos', 'curitibanos', 'bom retiro', 'urubici']
sul_keywords = ['criciúma', 'araranguá', 'tubarão', 'jaguaruna', 'meleiro', 'turvo', 'sombrio']
vale_keywords = ['blumenau', 'brusque', 'itajaí', 'indaial', 'timbó']

def classify_region(nome):
    nome_lower = nome.lower()
    if any(k in nome_lower for k in oeste_keywords):
        return 'Oeste'
    elif any(k in nome_lower for k in serrana_keywords):
        return 'Serrana'
    elif any(k in nome_lower for k in sul_keywords):
        return 'Sul'
    elif any(k in nome_lower for k in vale_keywords):
        return 'Vale'
    else:
        return 'Outras'

records = []
for m in municipios:
    cod = m['id']
    nome = m['nome']
    regiao = classify_region(nome)
    
    # Generate area (ha) and value (mil R$) by region profile
    # Oeste: high corn/soy/pig/poultry
    # Serrana: apple/forestry
    # Sul: rice
    # Vale: diversified
    
    if regiao == 'Oeste':
        area_total = random.randint(8000, 35000)
        area_soja = random.randint(2000, 12000)
        area_milho = random.randint(3000, 15000)
        area_arroz = random.randint(0, 500)
        area_maca = 0
        valor_total = random.randint(50000, 300000)
        bovinos = random.randint(15000, 80000)
        suinos = random.randint(50000, 400000)  # Oeste é líder em suínos
        aves = random.randint(500000, 5000000)  # e aves
        estabelec_total = random.randint(800, 3500)
        estabelec_grandes = random.randint(50, 250)  # >100ha
    
    elif regiao == 'Serrana':
        area_total = random.randint(5000, 25000)
        area_soja = random.randint(500, 3000)
        area_milho = random.randint(1000, 5000)
        area_arroz = 0
        area_maca = random.randint(500, 3000)  # maçã é forte na Serra
        valor_total = random.randint(30000, 180000)
        bovinos = random.randint(20000, 100000)  # pecuária de corte
        suinos = random.randint(5000, 30000)
        aves = random.randint(50000, 500000)
        estabelec_total = random.randint(600, 2800)
        estabelec_grandes = random.randint(80, 400)  # grandes áreas (fazendas)
    
    elif regiao == 'Sul':
        area_total = random.randint(6000, 28000)
        area_soja = random.randint(500, 4000)
        area_milho = random.randint(1000, 6000)
        area_arroz = random.randint(2000, 12000)  # arroz irrigado forte no Sul
        area_maca = 0
        valor_total = random.randint(40000, 220000)
        bovinos = random.randint(10000, 60000)
        suinos = random.randint(8000, 50000)
        aves = random.randint(100000, 1000000)
        estabelec_total = random.randint(700, 3200)
        estabelec_grandes = random.randint(40, 180)
    
    elif regiao == 'Vale':
        area_total = random.randint(3000, 15000)  # menor área (mais urbano)
        area_soja = random.randint(200, 2000)
        area_milho = random.randint(500, 3000)
        area_arroz = random.randint(300, 2000)
        area_maca = 0
        valor_total = random.randint(20000, 120000)
        bovinos = random.randint(5000, 30000)
        suinos = random.randint(3000, 20000)
        aves = random.randint(50000, 500000)
        estabelec_total = random.randint(400, 1800)
        estabelec_grandes = random.randint(20, 100)
    
    else:  # Outras
        area_total = random.randint(4000, 18000)
        area_soja = random.randint(300, 3000)
        area_milho = random.randint(800, 4000)
        area_arroz = random.randint(100, 2000)
        area_maca = random.randint(0, 500)
        valor_total = random.randint(25000, 150000)
        bovinos = random.randint(8000, 50000)
        suinos = random.randint(5000, 35000)
        aves = random.randint(80000, 800000)
        estabelec_total = random.randint(500, 2500)
        estabelec_grandes = random.randint(30, 150)
    
    records.append({
        'cod_municipio': cod,
        'nome_municipio': nome,
        'regiao_estimada': regiao,
        'area_total_ha': area_total,
        'area_soja_ha': area_soja,
        'area_milho_ha': area_milho,
        'area_arroz_ha': area_arroz,
        'area_maca_ha': area_maca,
        'valor_producao_mil_reais': valor_total,
        'rebanho_bovinos': bovinos,
        'rebanho_suinos': suinos,
        'rebanho_aves': aves,
        'estabelecimentos_total': estabelec_total,
        'estabelecimentos_grandes_100ha_plus': estabelec_grandes,
    })

df = pd.DataFrame(records)
df.to_csv(os.path.join(OUT_DIR, 'dados_agro_sc_synthetic.csv'), index=False, encoding='utf-8-sig')
df.to_json(os.path.join(OUT_DIR, 'dados_agro_sc_synthetic.json'), orient='records', force_ascii=False, indent=2)

print(f"Generated synthetic data for {len(df)} municipalities")
print(f"\nSummary by region:")
print(df.groupby('regiao_estimada')[['area_total_ha', 'valor_producao_mil_reais', 'estabelecimentos_grandes_100ha_plus']].sum())
print(f"\nFiles saved to {OUT_DIR}/dados_agro_sc_synthetic.[csv|json]")
print("\n** NOTE: This is SYNTHETIC data for demonstration. Replace with real IBGE data when available.")
