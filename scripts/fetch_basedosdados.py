"""
Script DEFINITIVO - Busca dados REAIS do IBGE via Base dos Dados
Método: SQL queries diretas no BigQuery (dados já limpos!)
Fonte: https://basedosdados.org
"""

import basedosdados as bd
import pandas as pd
from pathlib import Path

# Configurações
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("BUSCA AUTOMATIZADA - BASE DOS DADOS (basedosdados.org)")
print("=" * 80)
print("\n🎯 Método: SQL queries no BigQuery (dados limpos do IBGE)")
print("✓ Vantagem: Dados padronizados, sem parsing complicado")
print("⚡ Velocidade: Download direto, sem necessidade de API instável\n")

print("=" * 80)
print("CONFIGURAÇÃO NECESSÁRIA")
print("=" * 80)

print("\n📝 Este script usa a Base dos Dados (basedosdados.org)")
print("   que conecta no Google BigQuery (gratuito até 1TB/mês)")
print("\n🔧 PRIMEIRA VEZ? Você precisa:")
print("   1. Ter uma conta Google (Gmail)")
print("   2. Criar projeto no Google Cloud (gratuito)")
print("   3. Autenticar uma vez")
print("\n📚 Tutorial completo: https://basedosdados.org/docs/")

# Modo alternativo: download de CSVs públicos
print("\n" + "=" * 80)
print("MODO ALTERNATIVO: DOWNLOAD DIRETO (SEM AUTENTICAÇÃO)")
print("=" * 80)

print("\nA Base dos Dados também disponibiliza CSVs públicos!")
print("Vou tentar baixar diretamente (mais simples):\n")

import requests
import json

def download_basedosdados_public():
    """
    Tenta baixar dados públicos da Base dos Dados via API deles
    """
    print("[1/3] Tentando baixar PAM (Produção Agrícola Municipal)...")
    
    # URL da API pública da Base dos Dados
    # Nota: A API pública tem limits, mas para SC deve funcionar
    
    base_url = "https://api.basedosdados.org/api/v1/graphql"
    
    # Query GraphQL para buscar dados
    query = """
    query {
      allDataset(filter: {slug: "br-ibge-pam"}) {
        edges {
          node {
            name
            description
            tables {
              edges {
                node {
                  name
                  description
                }
              }
            }
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            base_url,
            json={'query': query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ API respondeu: {len(str(data))} bytes")
            return data
        else:
            print(f"   ✗ API retornou status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        return None


# Alternativa: usar modo download direto do projeto público
def download_from_public_bucket():
    """
    Base dos Dados tem bucket público no Google Cloud Storage
    """
    print("\n[ALTERNATIVA] Tentando acesso ao bucket público...\n")
    
    # URLs públicas conhecidas da Base dos Dados
    public_urls = {
        'pam': 'https://storage.googleapis.com/basedosdados-public/one-click-download/br_ibge_pam/municipio/municipio.csv',
        'ppm': 'https://storage.googleapis.com/basedosdados-public/one-click-download/br_ibge_ppm/municipio/municipio.csv',
    }
    
    datasets = {}
    
    for dataset_name, url in public_urls.items():
        print(f"[{dataset_name.upper()}] Baixando de {url[:60]}...")
        
        try:
            response = requests.get(url, timeout=120, stream=True)
            
            if response.status_code == 200:
                # Salvar arquivo temporário
                temp_file = OUTPUT_DIR / f"{dataset_name}_basedosdados.csv"
                
                with open(temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"   ✓ Baixado: {temp_file.stat().st_size / 1024 / 1024:.1f} MB")
                
                # Ler e filtrar SC
                df = pd.read_csv(temp_file)
                print(f"   ℹ️  Total de registros: {len(df)}")
                
                # Filtrar Santa Catarina (sigla_uf == 'SC')
                if 'sigla_uf' in df.columns:
                    df_sc = df[df['sigla_uf'] == 'SC'].copy()
                    print(f"   ✓ Registros SC: {len(df_sc)}")
                    datasets[dataset_name] = df_sc
                else:
                    print(f"   ⚠️  Coluna 'sigla_uf' não encontrada. Colunas: {df.columns.tolist()[:10]}")
                    datasets[dataset_name] = df
                    
            elif response.status_code == 404:
                print(f"   ✗ Dataset não encontrado (404)")
            else:
                print(f"   ✗ Status {response.status_code}")
                
        except Exception as e:
            print(f"   ✗ Erro: {e}")
    
    return datasets


# Executar download
result_api = download_basedosdados_public()
datasets = download_from_public_bucket()

if len(datasets) == 0:
    print("\n" + "=" * 80)
    print("❌ DOWNLOAD AUTOMÁTICO FALHOU")
    print("=" * 80)
    print("\n📖 SOLUÇÃO: Configurar acesso ao BigQuery (1 vez só)")
    print("\n📋 PASSO A PASSO:")
    print("\n1. Acesse: https://console.cloud.google.com")
    print("2. Crie um projeto (ex: 'geomarketing-drones')")
    print("3. No terminal, execute:")
    print("     import basedosdados as bd")
    print("     bd.download(savepath='data/pam_sc.csv',")
    print("                 query='SELECT * FROM `basedosdados.br_ibge_pam.municipio` WHERE sigla_uf=\"SC\" AND ano=2022',")
    print("                 billing_project_id='SEU_PROJETO_ID')")
    print("\n4. Na primeira vez, vai abrir navegador para autenticar")
    print("\n📚 Tutorial: https://basedosdados.org/docs/access-data/")
    
    print("\n" + "="  * 80)
    print("OU USE O DOWNLOAD MANUAL (5 min, garantido):")
    print("=" * 80)
    print("\n1. Acesse: https://basedosdados.org/dataset/br-ibge-pam")
    print("2. Clique em 'Download dos Dados'")
    print("3. Selecione: estado='SC', ano=2022")
    print("4. Baixe o CSV")
    print(f"5. Salve em: {OUTPUT_DIR / 'pam_sc_manual.csv'}")
    print("\nRepita para:")
    print("   - PPM (Pecuária): https://basedosdados.org/dataset/br-ibge-ppm")
    print("   - Censo Agro: https://basedosdados.org/dataset/br-ibge-censo-agropecuario")
    
else:
    print("\n" + "=" * 80)
    print("✅ DATASETS BAIXADOS COM SUCESSO!")
    print("=" * 80)
    
    # Processar dados baixados
    if 'pam' in datasets:
        df_pam = datasets['pam']
        print(f"\n[PAM] Processando {len(df_pam)} registros...")
        print(f"Colunas disponíveis: {df_pam.columns.tolist()[:10]}...")
        
        # Agrupar por município
        if 'id_municipio' in df_pam.columns and 'quantidade' in df_pam.columns:
            # Pivotar culturas
            culturas_interesse = ['Soja', 'Milho', 'Arroz', 'Maçã']
            
            df_pam_pivot = df_pam.pivot_table(
                index='id_municipio',
                columns='produto',
                values='quantidade',
                aggfunc='sum',
                fill_value=0
            ).reset_index()
            
            print(f"   ✓ Dados pivotados: {len(df_pam_pivot)} municípios")
            
            # Salvar
            output_file = OUTPUT_DIR / "pam_sc_processado.csv"
            df_pam_pivot.to_csv(output_file, index=False)
            print(f"   ✓ Salvo: {output_file}")
    
    if 'ppm' in datasets:
        df_ppm = datasets['ppm']
        print(f"\n[PPM] Processando {len(df_ppm)} registros...")
        print(f"Colunas: {df_ppm.columns.tolist()[:10]}...")
        
        output_file = OUTPUT_DIR / "ppm_sc_processado.csv"
        df_ppm.to_csv(output_file, index=False)
        print(f"   ✓ Salvo: {output_file}")
    
    print("\n" + "=" * 80)
    print("PRÓXIMOS PASSOS")
    print("=" * 80)
    print("\n✓ Dados baixados e salvos!")
    print("\n📧 Me avise se os dados parecem corretos.")
    print("   Posso criar um script de transformação para o formato final.")

print("\n" + "=" * 80)
