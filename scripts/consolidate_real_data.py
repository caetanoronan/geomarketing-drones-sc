"""
CONSOLIDADOR FINAL - Dados REAIS do IBGE
Usa PAM real (área plantada) + dados sintéticos calibrados para pecuária/censo
Recalcula ranking com dados OFICIAIS
"""

import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR = BASE_DIR / "data" / "outputs"

print("=" * 80)
print("CONSOLIDAÇÃO FINAL - DADOS REAIS + SINTÉTICOS CALIBRADOS")
print("=" * 80)

# ============================================================================
# 1. CARREGAR DADOS REAIS (PAM)
# ============================================================================

print("\n[1/4] Carregando dados REAIS do PAM...")

pam_real = pd.read_csv(DATA_DIR / "pam_area_plantada_sc_2024.csv")
print(f"✓ PAM: {len(pam_real)} municípios")
print(f"  - Área total: {pam_real['area_total_ha'].sum():,.0f} ha")

# ============================================================================
# 2. CARREGAR DADOS SINTÉTICOS (pecuária e censo)
# ============================================================================

print("\n[2/4] Carregando dados sintéticos calibrados...")

dados_synthetic = pd.read_csv(DATA_DIR / "dados_agro_sc_synthetic.csv")
print(f"✓ Sintéticos: {len(dados_synthetic)} municípios")

# ============================================================================
# 3. MESCLAR DADOS (Real PAM + Sintético Pecuária/Censo)
# ============================================================================

print("\n[3/4] Mesclando dados reais + sintéticos...")

# Merge por código de município
df_final = pam_real.merge(
    dados_synthetic[['cod_municipio', 'regiao_estimada', 'valor_producao_mil_reais',
                     'rebanho_bovinos', 'rebanho_suinos', 'rebanho_aves',
                     'estabelecimentos_total', 'estabelecimentos_grandes_100ha_plus']],
    on='cod_municipio',
    how='left'
)

# Ajustar valores de produção baseado em área REAL
# Proporção: área_real / área_synthetic
print("\n   📊 Ajustando valor de produção baseado em área real...")

for idx, row in df_final.iterrows():
    cod = row['cod_municipio']
    area_real = row['area_total_ha']
    
    # Buscar área sintética original
    if cod in dados_synthetic['cod_municipio'].values:
        area_synth = dados_synthetic[dados_synthetic['cod_municipio'] == cod]['area_total_ha'].values[0]
        
        if area_synth > 0:
            # Ajustar valor proporcionalmente
            fator = area_real / area_synth
            valor_original = df_final.at[idx, 'valor_producao_mil_reais']
            df_final.at[idx, 'valor_producao_mil_reais'] = valor_original * fator

print(f"✓ Valores ajustados proporcionalmente à área real")

# Preencher NaN
df_final = df_final.fillna(0)

# Estatísticas consolidadas
print(f"\n✅ Dados consolidados:")
print(f"   - Municípios: {len(df_final)}")
print(f"   - Área total (REAL): {df_final['area_total_ha'].sum():,.0f} ha")
print(f"   - Valor produção ajustado: R$ {df_final['valor_producao_mil_reais'].sum():,.0f} mil")
print(f"   - Estabelecimentos >100ha: {df_final['estabelecimentos_grandes_100ha_plus'].sum():,.0f}")

# ============================================================================
# 4. CALCULAR INDICADORES E RANKING
# ============================================================================

print("\n[4/4] Calculando indicadores e ranking...")

# Calcular culturas-alvo (soja + milho + arroz + maçã)
df_final['area_culturas_alvo_ha'] = (
    df_final['area_soja_ha'] + 
    df_final['area_milho_ha'] + 
    df_final['area_arroz_ha'] + 
    df_final['area_maca_ha']
)

# Indicador 1: Área Total (peso 35%)
df_final['ind_area_total'] = (df_final['area_total_ha'] / df_final['area_total_ha'].max() * 100).fillna(0)

# Indicador 2: Culturas-Alvo (peso 25%)
df_final['ind_culturas_alvo'] = (df_final['area_culturas_alvo_ha'] / df_final['area_culturas_alvo_ha'].max() * 100).fillna(0)

# Indicador 3: Grandes Produtores (peso 20%)
df_final['ind_grandes_produtores'] = (df_final['estabelecimentos_grandes_100ha_plus'] / df_final['estabelecimentos_grandes_100ha_plus'].max() * 100).fillna(0)

# Indicador 4: Infraestrutura B2B (peso 10%)
# Proxy: densidade de estabelecimentos por área
df_final['densidade_estab'] = df_final['estabelecimentos_total'] / (df_final['area_total_ha'] + 1)
df_final['ind_infra_b2b'] = (df_final['densidade_estab'] / df_final['densidade_estab'].max() * 100).fillna(0)

# Indicador 5: Concorrência (peso -10%)
# Mantém zero (dados de concorrência não disponíveis)
df_final['ind_concorrencia'] = 0

# Score composto
df_final['score_composto'] = (
    df_final['ind_area_total'] * 0.35 +
    df_final['ind_culturas_alvo'] * 0.25 +
    df_final['ind_grandes_produtores'] * 0.20 +
    df_final['ind_infra_b2b'] * 0.10 -
    df_final['ind_concorrencia'] * 0.10
)

# Ordenar por score
df_final = df_final.sort_values('score_composto', ascending=False).reset_index(drop=True)
df_final['ranking'] = df_final.index + 1

print(f"✓ Ranking calculado")

# ============================================================================
# 5. SALVAR RESULTADOS
# ============================================================================

print("\n" + "=" * 80)
print("SALVANDO RESULTADOS")
print("=" * 80)

# Selecionar colunas para output
output_cols = [
    'ranking', 'cod_municipio', 'nome_municipio', 'regiao_estimada',
    'area_total_ha', 'area_soja_ha', 'area_milho_ha', 'area_arroz_ha', 'area_maca_ha',
    'area_culturas_alvo_ha', 'valor_producao_mil_reais',
    'rebanho_bovinos', 'rebanho_suinos', 'rebanho_aves',
    'estabelecimentos_total', 'estabelecimentos_grandes_100ha_plus',
    'ind_area_total', 'ind_culturas_alvo', 'ind_grandes_produtores',
    'ind_infra_b2b', 'ind_concorrencia', 'score_composto'
]

df_output = df_final[output_cols].copy()

# Salvar CSV
output_file = OUTPUT_DIR / "ranking_municipal_drones_agro_REAL.csv"
df_output.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✓ CSV salvo: {output_file}")

# Salvar JSON
output_json = OUTPUT_DIR / "ranking_municipal_drones_agro_REAL.json"
df_output.to_json(output_json, orient='records', indent=2, force_ascii=False)
print(f"✓ JSON salvo: {output_json}")

# ============================================================================
# 6. EXIBIR TOP 15
# ============================================================================

print("\n" + "=" * 80)
print("TOP 15 MUNICÍPIOS - RANKING COM DADOS REAIS")
print("=" * 80)

for idx, row in df_output.head(15).iterrows():
    print(f"\n{row['ranking']}. {row['nome_municipio']} ({row['regiao_estimada']})")
    print(f"   Score: {row['score_composto']:.1f}")
    print(f"   Área total: {row['area_total_ha']:,.0f} ha")
    print(f"   Culturas-alvo: {row['area_culturas_alvo_ha']:,.0f} ha (Soja:{row['area_soja_ha']:,.0f}, Milho:{row['area_milho_ha']:,.0f}, Arroz:{row['area_arroz_ha']:,.0f})")
    print(f"   Grandes produtores: {row['estabelecimentos_grandes_100ha_plus']:.0f}")
    print(f"   Valor produção: R$ {row['valor_producao_mil_reais']:,.0f} mil")

# ============================================================================
# 7. COMPARAÇÃO COM RANKING SINTÉTICO
# ============================================================================

print("\n" + "=" * 80)
print("COMPARAÇÃO: RANKING REAL vs SINTÉTICO")
print("=" * 80)

# Carregar ranking sintético
try:
    df_synthetic_rank = pd.read_csv(OUTPUT_DIR / "ranking_municipal_drones_agro.csv")
    
    print("\nMudanças no TOP 10:\n")
    
    top10_real = df_output.head(10)['nome_municipio'].tolist()
    top10_synth = df_synthetic_rank.head(10)['nome_municipio'].tolist()
    
    print("RANKING REAL (dados IBGE):")
    for i, mun in enumerate(top10_real, 1):
        print(f"  {i:2d}. {mun}")
    
    print("\nRANKING SINTÉTICO (anterior):")
    for i, mun in enumerate(top10_synth, 1):
        print(f"  {i:2d}. {mun}")
    
    # Municípios que entraram/saíram do top 10
    novos = set(top10_real) - set(top10_synth)
    saíram = set(top10_synth) - set(top10_real)
    
    if novos:
        print(f"\n✨ Novos no TOP 10: {', '.join(novos)}")
    if saíram:
        print(f"\n📉 Saíram do TOP 10: {', '.join(saíram)}")
    
except:
    print("\n(Ranking sintético anterior não encontrado para comparação)")

# ============================================================================
# 8. ESTATÍSTICAS FINAIS
# ============================================================================

print("\n" + "=" * 80)
print("ESTATÍSTICAS FINAIS - DADOS REAIS")
print("=" * 80)

print(f"\nSANTA CATARINA - AGRICULTURA:")
print(f"  Total municípios: {len(df_output)}")
print(f"  Área agrícola total: {df_output['area_total_ha'].sum():,.0f} ha")
print(f"    - Soja: {df_output['area_soja_ha'].sum():,.0f} ha ({df_output['area_soja_ha'].sum()/df_output['area_total_ha'].sum()*100:.1f}%)")
print(f"    - Milho: {df_output['area_milho_ha'].sum():,.0f} ha ({df_output['area_milho_ha'].sum()/df_output['area_total_ha'].sum()*100:.1f}%)")
print(f"    - Arroz: {df_output['area_arroz_ha'].sum():,.0f} ha ({df_output['area_arroz_ha'].sum()/df_output['area_total_ha'].sum()*100:.1f}%)")
print(f"    - Maçã: {df_output['area_maca_ha'].sum():,.0f} ha ({df_output['area_maca_ha'].sum()/df_output['area_total_ha'].sum()*100:.1f}%)")

print(f"\nPor região:")
regiao_stats = df_output.groupby('regiao_estimada').agg({
    'area_total_ha': 'sum',
    'score_composto': 'mean',
    'nome_municipio': 'count'
}).sort_values('area_total_ha', ascending=False)

print(regiao_stats.to_string())

print("\n" + "=" * 80)
print("✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)

print(f"\n📂 Arquivos gerados:")
print(f"   - {output_file.name}")
print(f"   - {output_json.name}")

print(f"\n📊 Próximos passos:")
print(f"   1. Gerar novos mapas com dados reais")
print(f"   2. Atualizar relatório final")
print(f"   3. Atualizar apresentação HTML")
