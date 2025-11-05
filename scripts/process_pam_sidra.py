"""
Processador de dados REAIS do SIDRA - Tabela PAM 5457
Lê o CSV baixado e transforma no formato necessário
"""

import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
INPUT_FILE = BASE_DIR / "data" / "ibge_agro" / "pam_raw" / "tabela5457.csv"
OUTPUT_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PROCESSANDO DADOS REAIS - PAM (Tabela 5457)")
print("=" * 80)

print(f"\n📂 Lendo arquivo: {INPUT_FILE}")

# Ler arquivo com configurações especiais para SIDRA
# SIDRA pode ter linhas de cabeçalho múltiplas ou formato especial

# Tentar diferentes encodings e formatos
encodings = ['latin1', 'utf-8', 'iso-8859-1', 'cp1252']
separators = [';', ',', '\t']

df = None

for encoding in encodings:
    for sep in separators:
        try:
            print(f"\n🔍 Tentando encoding={encoding}, sep='{sep}'...")
            
            # Ler linhas iniciais para entender estrutura
            with open(INPUT_FILE, 'r', encoding=encoding) as f:
                lines = [f.readline() for _ in range(10)]
            
            print(f"   Primeiras linhas:")
            for i, line in enumerate(lines[:3]):
                print(f"   [{i}] {line[:100]}")
            
            # Detectar linha de header (procura por palavras-chave)
            header_line = 0
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in ['município', 'produto', 'valor', 'ano']):
                    header_line = i
                    print(f"   ✓ Header detectado na linha {i}")
                    break
            
            # Ler CSV pulando linhas antes do header
            df = pd.read_csv(INPUT_FILE, sep=sep, encoding=encoding, skiprows=header_line)
            
            print(f"   ✓ Sucesso! {len(df)} linhas, {len(df.columns)} colunas")
            print(f"   Colunas: {df.columns.tolist()[:5]}...")
            break
            
        except Exception as e:
            print(f"   ✗ Falhou: {str(e)[:80]}")
            continue
    
    if df is not None:
        break

if df is None:
    print("\n❌ Não consegui ler o arquivo com nenhuma combinação.")
    print("\n📋 Vou tentar abordagem linha por linha...")
    
    # Abordagem alternativa: ler linha por linha
    with open(INPUT_FILE, 'r', encoding='latin1') as f:
        all_lines = f.readlines()
    
    print(f"\n📄 Arquivo tem {len(all_lines)} linhas")
    print("\nPrimeiras 20 linhas:")
    for i, line in enumerate(all_lines[:20]):
        print(f"[{i:2d}] {line.rstrip()[:120]}")
    
    print("\n" + "=" * 80)
    print("ANÁLISE DO ARQUIVO")
    print("=" * 80)
    print("\nO arquivo do SIDRA tem formato especial com metadados no topo.")
    print("Vou identificar onde começam os dados reais...\n")
    
    # Encontrar linha onde começam dados (tem separador ';' com valores numéricos)
    data_start = 0
    for i, line in enumerate(all_lines):
        parts = line.split(';')
        if len(parts) > 3 and any(re.search(r'\d', part) for part in parts[:3]):
            data_start = i
            print(f"✓ Dados começam na linha {i}: {line.rstrip()[:100]}")
            break
    
    # Linha anterior deve ser o header
    if data_start > 0:
        header_line = data_start - 1
        print(f"✓ Header na linha {header_line}: {all_lines[header_line].rstrip()[:100]}")
        
        # Ler CSV a partir do header
        df = pd.read_csv(INPUT_FILE, sep=';', encoding='latin1', skiprows=header_line)
        print(f"\n✓ Arquivo lido: {len(df)} linhas, {len(df.columns)} colunas")

if df is not None:
    print("\n" + "=" * 80)
    print("ESTRUTURA DOS DADOS")
    print("=" * 80)
    
    print(f"\nColunas detectadas ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  [{i}] {col}")
    
    print(f"\nPrimeiras 5 linhas:")
    print(df.head())
    
    print(f"\nÚltimas 5 linhas:")
    print(df.tail())
    
    # Identificar colunas importantes
    print("\n" + "=" * 80)
    print("MAPEAMENTO DE COLUNAS")
    print("=" * 80)
    
    col_map = {}
    
    for col in df.columns:
        col_lower = col.lower()
        if 'município' in col_lower or 'municipio' in col_lower:
            col_map['municipio'] = col
            print(f"✓ Município: {col}")
        elif 'produto' in col_lower or 'cultura' in col_lower:
            col_map['produto'] = col
            print(f"✓ Produto: {col}")
        elif 'ano' in col_lower:
            col_map['ano'] = col
            print(f"✓ Ano: {col}")
        elif 'valor' in col_lower or 'área' in col_lower or 'area' in col_lower:
            col_map['valor'] = col
            print(f"✓ Valor/Área: {col}")
        elif 'código' in col_lower or 'codigo' in col_lower or 'cod' in col_lower:
            col_map['cod_municipio'] = col
            print(f"✓ Código: {col}")
    
    print(f"\n✅ Mapeamento completo: {col_map}")
    
    # Salvar versão processada
    output_file = OUTPUT_DIR / "pam_processado.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ Arquivo salvo: {output_file}")
    
    # Estatísticas
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)
    
    if 'municipio' in col_map:
        municipios_unicos = df[col_map['municipio']].nunique()
        print(f"\nMunicípios únicos: {municipios_unicos}")
    
    if 'produto' in col_map:
        produtos = df[col_map['produto']].unique()
        print(f"\nProdutos encontrados ({len(produtos)}):")
        for prod in produtos[:10]:
            print(f"  - {prod}")
        if len(produtos) > 10:
            print(f"  ... e mais {len(produtos) - 10}")
    
    print("\n" + "=" * 80)
    print("✅ PROCESSAMENTO CONCLUÍDO!")
    print("=" * 80)
    
else:
    print("\n❌ Não foi possível processar o arquivo.")
    print("\n📧 Me mostre as primeiras 30 linhas do arquivo para eu entender o formato.")
