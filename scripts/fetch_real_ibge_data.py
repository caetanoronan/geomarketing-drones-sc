"""
Script para buscar dados REAIS do IBGE sobre agricultura em SC
Usa Base dos Dados (basedosdados.org) como fonte principal
Fallback para SIDRA se Base dos Dados falhar
"""

import pandas as pd
import requests
import json
import os
from pathlib import Path

# Configurações
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SC_CODE = "42"  # Código IBGE de Santa Catarina

print("=" * 80)
print("COLETA AUTOMATIZADA DE DADOS REAIS - AGRICULTURA SC")
print("=" * 80)

# ============================================================================
# MÉTODO 1: SIDRA API (Funciona sem autenticação!)
# ============================================================================

def fetch_sidra_pam():
    """
    Busca dados da PAM - Produção Agrícola Municipal
    Tabela 5457: área plantada, valor da produção
    """
    print("\n[1/4] Buscando PAM - Produção Agrícola Municipal (SIDRA)...")
    
    # Endpoint SIDRA com sintaxe correta
    # Formato: /t/{tabela}/n6/{municipios}/v/{variaveis}/p/{periodo}/c81/{produtos}
    
    # Produtos principais: soja (39443), milho (39441), arroz (39442), maçã (39445)
    produtos = "39441,39442,39443,39445"  # milho, arroz, soja, maçã
    
    # Variáveis: 109 (área plantada), 214 (área colhida), 215 (valor da produção)
    variaveis = "109,214,215"
    
    # Período: 2022 (último completo)
    periodo = "2022"
    
    # URL com sintaxe correta (sem especificar municípios, pega todos de SC)
    url = f"https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/{variaveis}/p/{periodo}/c81/{produtos}"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # SIDRA retorna array de arrays, primeira linha é header
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Filtrar apenas SC
            df_sc = df[df['D3C'].str.startswith('42')].copy()  # D3C = código município
            
            print(f"   ✓ PAM: {len(df_sc)} registros de SC")
            return df_sc
        else:
            print("   ✗ PAM: Resposta vazia")
            return None
            
    except Exception as e:
        print(f"   ✗ PAM falhou: {e}")
        return None


def fetch_sidra_ppm():
    """
    Busca dados da PPM - Pesquisa da Pecuária Municipal
    Tabela 3939: efetivo de rebanhos
    """
    print("\n[2/4] Buscando PPM - Pecuária Municipal (SIDRA)...")
    
    # Tipos de rebanho: 3939 = bovinos, suínos, galinhas
    # Variável 2111 = Número de cabeças
    
    # Tipos: 3939 tem várias categorias, vamos pegar principais
    # c18: 3939 (bovinos), 3940 (suínos), 3941 (galinhas)
    
    url = "https://apisidra.ibge.gov.br/values/t/3939/n6/all/v/2111/p/2022/c18/all"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df_sc = df[df['D3C'].str.startswith('42')].copy()
            
            print(f"   ✓ PPM: {len(df_sc)} registros de SC")
            return df_sc
        else:
            print("   ✗ PPM: Resposta vazia")
            return None
            
    except Exception as e:
        print(f"   ✗ PPM falhou: {e}")
        return None


def fetch_sidra_censo_agro():
    """
    Busca dados do Censo Agropecuário 2017
    Tabela 6727: estabelecimentos por grupos de área
    """
    print("\n[3/4] Buscando Censo Agropecuário 2017 (SIDRA)...")
    
    # Tabela 6727: estabelecimentos por grupo de área total
    # Variável 184 = Número de estabelecimentos agropecuários
    # c220: grupos de área (queremos >100 ha)
    
    url = "https://apisidra.ibge.gov.br/values/t/6727/n6/all/v/184/p/2017/c220/all"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df_sc = df[df['D3C'].str.startswith('42')].copy()
            
            print(f"   ✓ Censo Agro: {len(df_sc)} registros de SC")
            return df_sc
        else:
            print("   ✗ Censo Agro: Resposta vazia")
            return None
            
    except Exception as e:
        print(f"   ✗ Censo Agro falhou: {e}")
        return None


def fetch_municipios_sc():
    """
    Busca lista completa de municípios de SC
    """
    print("\n[4/4] Buscando lista de municípios SC...")
    
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        municipios = pd.DataFrame([
            {
                'cod_municipio': m['id'],
                'nome_municipio': m['nome'],
                'microrregiao': m['microrregiao']['nome'],
                'mesorregiao': m['microrregiao']['mesorregiao']['nome']
            }
            for m in data
        ])
        
        print(f"   ✓ Municípios: {len(municipios)} encontrados")
        return municipios
        
    except Exception as e:
        print(f"   ✗ Municípios falhou: {e}")
        return None


# ============================================================================
# PROCESSAMENTO E CONSOLIDAÇÃO
# ============================================================================

def process_pam_data(df_pam, municipios):
    """
    Processa dados da PAM e agrega por município
    """
    if df_pam is None or len(df_pam) == 0:
        return None
    
    print("\n[PROCESSANDO] PAM - Produção Agrícola...")
    
    # Renomear colunas (SIDRA usa nomes diferentes)
    # D3C = código município, D3N = nome município
    # D2C = código produto, D2N = nome produto
    # V = valor da variável
    
    df_pam['cod_municipio'] = df_pam['D3C'].astype(int)
    df_pam['produto'] = df_pam['D2N'].str.lower().str.strip()
    df_pam['variavel'] = df_pam['D1N'].str.lower()
    df_pam['valor'] = pd.to_numeric(df_pam['V'].str.replace(',', ''), errors='coerce')
    
    # Pivotar para ter culturas em colunas
    result = {}
    
    for cod in municipios['cod_municipio'].unique():
        df_mun = df_pam[df_pam['cod_municipio'] == cod]
        
        mun_data = {'cod_municipio': cod}
        
        # Área plantada por cultura
        for cultura in ['soja', 'milho', 'arroz', 'maçã']:
            area = df_mun[
                (df_mun['produto'].str.contains(cultura, case=False, na=False)) &
                (df_mun['variavel'].str.contains('área plantada', case=False))
            ]['valor'].sum()
            
            mun_data[f'area_{cultura.replace("ç", "c").replace("ã", "a")}_ha'] = area
        
        # Área total = soma de todas culturas
        mun_data['area_total_ha'] = sum([
            mun_data[f'area_{c}_ha'] 
            for c in ['soja', 'milho', 'arroz', 'maca']
        ])
        
        # Valor da produção total
        valor_producao = df_mun[
            df_mun['variavel'].str.contains('valor da produção', case=False)
        ]['valor'].sum()
        
        mun_data['valor_producao_mil_reais'] = valor_producao
        
        result[cod] = mun_data
    
    df_result = pd.DataFrame(list(result.values()))
    print(f"   ✓ {len(df_result)} municípios processados")
    
    return df_result


def process_ppm_data(df_ppm):
    """
    Processa dados da PPM (pecuária)
    """
    if df_ppm is None or len(df_ppm) == 0:
        return None
    
    print("\n[PROCESSANDO] PPM - Pecuária...")
    
    df_ppm['cod_municipio'] = df_ppm['D3C'].astype(int)
    df_ppm['tipo_rebanho'] = df_ppm['D1N'].str.lower().str.strip()
    df_ppm['valor'] = pd.to_numeric(df_ppm['V'], errors='coerce')
    
    # Agrupar por município e tipo de rebanho
    result = {}
    
    for cod in df_ppm['cod_municipio'].unique():
        df_mun = df_ppm[df_ppm['cod_municipio'] == cod]
        
        mun_data = {'cod_municipio': cod}
        
        # Extrair rebanhos principais
        for tipo in ['bovino', 'suíno', 'galinhas']:
            qtd = df_mun[
                df_mun['tipo_rebanho'].str.contains(tipo, case=False, na=False)
            ]['valor'].sum()
            
            coluna = f'rebanho_{tipo}s' if tipo != 'galinhas' else 'rebanho_aves'
            mun_data[coluna] = qtd
        
        result[cod] = mun_data
    
    df_result = pd.DataFrame(list(result.values()))
    print(f"   ✓ {len(df_result)} municípios processados")
    
    return df_result


def process_censo_agro_data(df_censo):
    """
    Processa dados do Censo Agropecuário
    """
    if df_censo is None or len(df_censo) == 0:
        return None
    
    print("\n[PROCESSANDO] Censo Agropecuário...")
    
    df_censo['cod_municipio'] = df_censo['D3C'].astype(int)
    df_censo['grupo_area'] = df_censo['D1N'].str.lower().str.strip()
    df_censo['valor'] = pd.to_numeric(df_censo['V'], errors='coerce')
    
    # Agrupar por município
    result = {}
    
    for cod in df_censo['cod_municipio'].unique():
        df_mun = df_censo[df_censo['cod_municipio'] == cod]
        
        # Total de estabelecimentos
        total = df_mun['valor'].sum()
        
        # Grandes estabelecimentos (>100 ha)
        # Grupos: "De 100 a menos de 200", "De 200 a menos de 500", "De 500 a menos de 1000", "De 1000 ha e mais"
        grandes = df_mun[
            df_mun['grupo_area'].str.contains('100|200|500|1000', case=False, na=False)
        ]['valor'].sum()
        
        result[cod] = {
            'cod_municipio': cod,
            'estabelecimentos_total': total,
            'estabelecimentos_grandes_100ha_plus': grandes
        }
    
    df_result = pd.DataFrame(list(result.values()))
    print(f"   ✓ {len(df_result)} municípios processados")
    
    return df_result


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print("\n" + "=" * 80)
    print("INICIANDO COLETA DE DADOS")
    print("=" * 80)
    
    # 1. Buscar lista de municípios
    municipios = fetch_municipios_sc()
    if municipios is None:
        print("\n❌ ERRO: Não foi possível buscar lista de municípios")
        return
    
    # 2. Buscar dados das fontes
    df_pam = fetch_sidra_pam()
    df_ppm = fetch_sidra_ppm()
    df_censo = fetch_sidra_censo_agro()
    
    # 3. Processar dados
    df_pam_proc = process_pam_data(df_pam, municipios) if df_pam is not None else None
    df_ppm_proc = process_ppm_data(df_ppm) if df_ppm is not None else None
    df_censo_proc = process_censo_agro_data(df_censo) if df_censo is not None else None
    
    # 4. Consolidar tudo
    print("\n" + "=" * 80)
    print("CONSOLIDANDO DADOS")
    print("=" * 80)
    
    # Começar com lista de municípios
    df_final = municipios.copy()
    
    # Merge com PAM (produção agrícola)
    if df_pam_proc is not None:
        df_final = df_final.merge(df_pam_proc, on='cod_municipio', how='left')
        print(f"✓ PAM mesclado: {len(df_pam_proc)} registros")
    
    # Merge com PPM (pecuária)
    if df_ppm_proc is not None:
        df_final = df_final.merge(df_ppm_proc, on='cod_municipio', how='left')
        print(f"✓ PPM mesclado: {len(df_ppm_proc)} registros")
    
    # Merge com Censo Agro
    if df_censo_proc is not None:
        df_final = df_final.merge(df_censo_proc, on='cod_municipio', how='left')
        print(f"✓ Censo Agro mesclado: {len(df_censo_proc)} registros")
    
    # Preencher NaN com 0
    numeric_cols = df_final.select_dtypes(include=['float64', 'int64']).columns
    df_final[numeric_cols] = df_final[numeric_cols].fillna(0)
    
    # Mapear região estimada (baseado em mesorregião)
    def mapear_regiao(mesorregiao):
        mesorregiao_lower = str(mesorregiao).lower()
        if 'oeste' in mesorregiao_lower:
            return 'Oeste'
        elif 'sul' in mesorregiao_lower:
            return 'Sul'
        elif 'serrana' in mesorregiao_lower or 'norte' in mesorregiao_lower:
            return 'Serrana'
        elif 'vale' in mesorregiao_lower or 'itajaí' in mesorregiao_lower:
            return 'Vale'
        else:
            return 'Outras'
    
    df_final['regiao_estimada'] = df_final['mesorregiao'].apply(mapear_regiao)
    
    # 5. Salvar resultados
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS")
    print("=" * 80)
    
    output_csv = OUTPUT_DIR / "dados_agro_sc_real.csv"
    output_json = OUTPUT_DIR / "dados_agro_sc_real.json"
    
    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    df_final.to_json(output_json, orient='records', indent=2, force_ascii=False)
    
    print(f"\n✓ CSV salvo: {output_csv}")
    print(f"✓ JSON salvo: {output_json}")
    
    # 6. Estatísticas finais
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS FINAIS")
    print("=" * 80)
    
    print(f"\nTotal de municípios: {len(df_final)}")
    print(f"\nÁrea agrícola total (SC): {df_final['area_total_ha'].sum():,.0f} ha")
    print(f"Valor de produção total: R$ {df_final['valor_producao_mil_reais'].sum():,.0f} mil")
    
    if 'estabelecimentos_total' in df_final.columns:
        print(f"Total estabelecimentos: {df_final['estabelecimentos_total'].sum():,.0f}")
        print(f"Estabelecimentos grandes (>100 ha): {df_final['estabelecimentos_grandes_100ha_plus'].sum():,.0f}")
    
    print("\nDistribuição por região:")
    print(df_final.groupby('regiao_estimada')['area_total_ha'].sum().sort_values(ascending=False))
    
    print("\nTop 10 municípios por área agrícola:")
    top10 = df_final.nlargest(10, 'area_total_ha')[['nome_municipio', 'regiao_estimada', 'area_total_ha']]
    print(top10.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("✅ COLETA CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print(f"\n📂 Próximo passo: Execute 'calculate_agro_indicators_ranking.py'")
    print(f"   para recalcular o ranking com os dados REAIS")


if __name__ == "__main__":
    main()
