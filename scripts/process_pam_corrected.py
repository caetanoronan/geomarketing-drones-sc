"""
Processador CORRIGIDO - PAM SIDRA Tabela 5457
Formato identificado: header na linha 5 (0-indexed), dados começam linha 6
"""

import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
INPUT_FILE = BASE_DIR / "data" / "ibge_agro" / "pam_raw" / "tabela5457.csv"
OUTPUT_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PROCESSANDO PAM - Tabela 5457 (Área Plantada)")
print("=" * 80)

# Ler CSV: header na linha 5 (0-indexed linha 4), dados começam linha 6
print(f"\n📂 Lendo: {INPUT_FILE}")

df = pd.read_csv(
    INPUT_FILE,
    sep=';',
    encoding='utf-8',
    skiprows=4,  # Pula as 4 primeiras linhas de metadados
    dtype=str  # Ler tudo como string primeiro
)

print(f"✓ {len(df)} linhas carregadas")
print(f"✓ Colunas: {df.columns.tolist()}")

# Renomear colunas para facilitar
df.columns = ['Nivel', 'Cod', 'Localidade', 'Total', 'Arroz', 'Maca', 'Milho', 'Soja']

print(f"\n📊 Primeiras 10 linhas:")
print(df.head(10))

# Filtrar apenas municípios de SC
# Municípios têm código que começa com 42 (UF de SC)
print(f"\n🔍 Filtrando municípios de Santa Catarina (Cod começa com 42)...")

# Remover aspas do código se houver
df['Cod'] = df['Cod'].str.replace('"', '').str.strip()

# Filtrar SC: códigos começam com 42 e têm 7 dígitos (municípios)
df_sc_municipios = df[
    (df['Cod'].str.startswith('42', na=False)) & 
    (df['Cod'].str.len() == 7)
].copy()

print(f"✓ {len(df_sc_municipios)} municípios de SC encontrados")

# Limpar dados: remover aspas, converter "-" e "..." para 0
print(f"\n🧹 Limpando dados...")

for col in ['Total', 'Arroz', 'Maca', 'Milho', 'Soja']:
    # Remover aspas
    df_sc_municipios[col] = df_sc_municipios[col].str.replace('"', '').str.strip()
    
    # Substituir "-" e "..." por 0
    df_sc_municipios[col] = df_sc_municipios[col].replace(['-', '...', ''], '0')
    
    # Converter para numérico
    df_sc_municipios[col] = pd.to_numeric(df_sc_municipios[col], errors='coerce').fillna(0)

# Limpar nome do município
df_sc_municipios['Localidade'] = df_sc_municipios['Localidade'].str.replace('"', '').str.strip()

# Renomear para formato final
df_final = df_sc_municipios[['Cod', 'Localidade', 'Total', 'Arroz', 'Maca', 'Milho', 'Soja']].copy()
df_final.columns = ['cod_municipio', 'nome_municipio', 'area_total_ha', 'area_arroz_ha', 'area_maca_ha', 'area_milho_ha', 'area_soja_ha']

# Converter código para inteiro
df_final['cod_municipio'] = df_final['cod_municipio'].astype(int)

print(f"\n✅ Dados processados:")
print(df_final.head(10))

# Estatísticas
print(f"\n" + "=" * 80)
print("ESTATÍSTICAS")
print("=" * 80)

print(f"\nTotal de municípios: {len(df_final)}")
print(f"Área total SC: {df_final['area_total_ha'].sum():,.0f} ha")
print(f"  - Arroz: {df_final['area_arroz_ha'].sum():,.0f} ha")
print(f"  - Maçã: {df_final['area_maca_ha'].sum():,.0f} ha")
print(f"  - Milho: {df_final['area_milho_ha'].sum():,.0f} ha")
print(f"  - Soja: {df_final['area_soja_ha'].sum():,.0f} ha")

print(f"\nTop 10 municípios por área total:")
top10 = df_final.nlargest(10, 'area_total_ha')[['nome_municipio', 'area_total_ha', 'area_soja_ha', 'area_milho_ha']]
print(top10.to_string(index=False))

# Salvar
output_file = OUTPUT_DIR / "pam_area_plantada_sc_2024.csv"
df_final.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✓ Arquivo salvo: {output_file}")

print(f"\n" + "=" * 80)
print("✅ PROCESSAMENTO CONCLUÍDO!")
print("=" * 80)

print(f"\n📋 Próximos passos:")
print(f"   1. Baixar mais 2 arquivos do SIDRA:")
print(f"      - Tabela 3939 (PPM - Pecuária)")
print(f"      - Tabela 6727 (Censo Agro - Estabelecimentos)")
print(f"   2. Ou me avise que está pronto para consolidar os dados!")
