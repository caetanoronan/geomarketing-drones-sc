"""Calculate agricultural drone market potential indicators and composite score for SC municipalities.
Indicators (with weights):
1. Agricultural area (35%): total planted area + key crops (soy/corn/rice/apple)
2. Target crops profile (25%): area of drone-friendly crops (pulverização/monitoramento)
3. Large producers concentration (20%): establishments >100ha (B2B sales potential)
4. Infrastructure/B2B access (10%): cooperatives + agrarian shops density
5. Competition (-10%): existing agricultural drone service providers

Outputs:
- Municipal ranking CSV with normalized indicators + composite score
- Top 10-15 municipalities for agricultural drone operations
"""
import pandas as pd
import json
import os

DATA_DIR = 'data/ibge_agro'
OUT_DIR = 'data/outputs'
os.makedirs(OUT_DIR, exist_ok=True)

# Load synthetic agro data
df_agro = pd.read_csv(os.path.join(DATA_DIR, 'dados_agro_sc_synthetic.csv'))
print(f"Loaded agro data for {len(df_agro)} municipalities\n")

# Load municipal areas (from malha) for density calculations
# For now, use rough estimates; can join with actual malha geojson later
# SC municipalities range from ~20 km² (small urban) to ~3000+ km² (large rural)
# We'll estimate area_km2 based on agricultural area (rough heuristic)
df_agro['area_municipio_km2_est'] = df_agro['area_total_ha'] / 100 * 1.5  # rough conversion + buffer

# Calculate raw indicators
print("Calculating indicators...")

# 1) Agricultural area indicator (35% weight)
# Sum of all planted area (could weight by crop value, but area is proxy for drone usage potential)
df_agro['ind_area_agricola'] = df_agro['area_total_ha']

# 2) Target crops (25% weight)
# Crops most suitable for drones: soy, corn (pulverização), rice (pulverização), apple (monitoramento)
df_agro['ind_culturas_alvo'] = (
    df_agro['area_soja_ha'] * 1.2 +  # soy/corn high potential
    df_agro['area_milho_ha'] * 1.2 +
    df_agro['area_arroz_ha'] * 1.5 +  # rice pulverização is classic use
    df_agro['area_maca_ha'] * 1.0     # orchards (monitoring)
)

# 3) Large producers (20% weight)
# Number of establishments >100ha (potential buyers for owned drones)
df_agro['ind_grandes_produtores'] = df_agro['estabelecimentos_grandes_100ha_plus']

# 4) Infrastructure/B2B (10% weight)
# For now, use proxy: production value / area (indicates commercial farming intensity)
# Later: add cooperative/agrarian shop counts from OSM
df_agro['ind_infraestrutura_b2b'] = df_agro['valor_producao_mil_reais'] / df_agro['area_total_ha'].replace(0, 1)

# 5) Competition (-10% weight)
# For now, assume zero drone competitors (will be negative in composite, so higher competition = lower score)
# Later: add OSM/web scraping for drone service providers
df_agro['ind_concorrencia_drones'] = 0  # placeholder

# Normalize indicators (min-max to 0-100 scale)
print("Normalizing indicators...")

def normalize_minmax(series):
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([50] * len(series), index=series.index)
    return ((series - min_val) / (max_val - min_val) * 100)

df_agro['norm_area_agricola'] = normalize_minmax(df_agro['ind_area_agricola'])
df_agro['norm_culturas_alvo'] = normalize_minmax(df_agro['ind_culturas_alvo'])
df_agro['norm_grandes_produtores'] = normalize_minmax(df_agro['ind_grandes_produtores'])
df_agro['norm_infraestrutura_b2b'] = normalize_minmax(df_agro['ind_infraestrutura_b2b'])
df_agro['norm_concorrencia'] = normalize_minmax(df_agro['ind_concorrencia_drones'])

# Calculate composite score (weighted sum)
weights = {
    'area': 0.35,
    'culturas': 0.25,
    'grandes': 0.20,
    'infra': 0.10,
    'concorrencia': -0.10,  # negative weight (higher competition = lower score)
}

df_agro['score_composto'] = (
    df_agro['norm_area_agricola'] * weights['area'] +
    df_agro['norm_culturas_alvo'] * weights['culturas'] +
    df_agro['norm_grandes_produtores'] * weights['grandes'] +
    df_agro['norm_infraestrutura_b2b'] * weights['infra'] +
    df_agro['norm_concorrencia'] * weights['concorrencia']
)

# Rank municipalities
df_agro = df_agro.sort_values('score_composto', ascending=False).reset_index(drop=True)
df_agro['ranking'] = df_agro.index + 1

# Save full ranking
output_cols = [
    'ranking', 'cod_municipio', 'nome_municipio', 'regiao_estimada',
    'area_total_ha', 'area_soja_ha', 'area_milho_ha', 'area_arroz_ha', 'area_maca_ha',
    'valor_producao_mil_reais', 'estabelecimentos_grandes_100ha_plus',
    'norm_area_agricola', 'norm_culturas_alvo', 'norm_grandes_produtores',
    'norm_infraestrutura_b2b', 'norm_concorrencia', 'score_composto'
]
df_out = df_agro[output_cols].copy()
df_out.to_csv(os.path.join(OUT_DIR, 'ranking_municipal_drones_agro.csv'), index=False, encoding='utf-8-sig')
print(f"\nFull ranking saved to ranking_municipal_drones_agro.csv")

# Display top 15
print("\n" + "="*80)
print("TOP 15 MUNICÍPIOS PARA OPERAÇÕES DE DRONES AGRÍCOLAS")
print("="*80)
top15 = df_out.head(15)
for idx, row in top15.iterrows():
    print(f"\n{int(row['ranking'])}. {row['nome_municipio']} ({row['regiao_estimada']})")
    print(f"   Score: {row['score_composto']:.1f}")
    print(f"   Área agrícola: {int(row['area_total_ha']):,} ha")
    print(f"   Culturas-alvo (soja/milho/arroz/maçã): {int(row['area_soja_ha'] + row['area_milho_ha'] + row['area_arroz_ha'] + row['area_maca_ha']):,} ha")
    print(f"   Grandes produtores (>100ha): {int(row['estabelecimentos_grandes_100ha_plus'])}")
    print(f"   Valor produção: R$ {int(row['valor_producao_mil_reais']):,} mil")

print("\n" + "="*80)
print("Análise concluída. Arquivos salvos em data/outputs/")
print("="*80)
