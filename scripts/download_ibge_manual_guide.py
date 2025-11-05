"""
Script ALTERNATIVO para buscar dados reais do IBGE
Método: Download direto de arquivos CSV do SIDRA (interface web)
Sem necessidade de API - mais estável!
"""

import pandas as pd
import requests
from pathlib import Path
import time

# Configurações
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "ibge_agro"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("DOWNLOAD DIRETO DE DADOS IBGE - AGRICULTURA SC")
print("=" * 80)
print("\nMétodo: Download de CSVs pré-configurados do SIDRA")
print("Vantagem: Não depende de API instável\n")

# ============================================================================
# URLs PRÉ-CONFIGURADAS DO SIDRA (formato de download direto)
# ============================================================================

# Estas URLs foram construídas usando a interface web do SIDRA e capturando
# o link de download. Elas apontam para CSVs prontos.

URLS = {
    'pam_2022': {
        'url': 'https://sidra.ibge.gov.br/geratabela?format=us.csv&name=tabela5457.csv&terr=NC&rank=-&query=t/5457/n6/4200051,4200101,4200159,4200200,4200309,4200408,4200507,4200556,4200606,4200705,4200754,4200804,4200903,4201000,4201109,4201208,4201257,4201273,4201307,4201406,4201505,4201604,4201653,4201703,4201802,4201901,4202008,4202057,4202073,4202081,4202099,4202107,4202131,4202156,4202206,4202305,4202404,4202438,4202453,4202503,4202537,4202578,4202602,4202701,4202800,4202859,4202875,4202909,4203004,4203103,4203152,4203202,4203301,4203400,4203509,4203558,4203608,4203707,4203806,4203905,4203954,4204002,4204101,4204152,4204178,4204194,4204202,4204251,4204301,4204350,4204400,4204509,4204558,4204608,4204707,4204756,4204806,4204905,4205001,4205100,4205159,4205175,4205191,4205209,4205308,4205357,4205407,4205431,4205456,4205506,4205555,4205605,4205704,4205803,4205902,4206009,4206108,4206207,4206306,4206405,4206504,4206603,4206652,4206702,4206751,4206801,4206900,4207007,4207106,4207205,4207304,4207403,4207502,4207577,4207601,4207650,4207684,4207700,4207759,4207809,4207858,4207908,4208005,4208104,4208203,4208302,4208401,4208450,4208500,4208609,4208708,4208807,4208906,4208955,4209003,4209102,4209151,4209177,4209201,4209300,4209409,4209458,4209508,4209607,4209706,4209805,4209854,4209904,4210001,4210035,4210050,4210100,4210209,4210308,4210407,4210506,4210555,4210605,4210704,4210803,4210852,4210902,4211009,4211058,4211108,4211207,4211256,4211306,4211405,4211454,4211504,4211603,4211652,4211702,4211751,4211801,4211850,4211876,4211892,4211900,4212007,4212056,4212106,4212205,4212239,4212254,4212270,4212304,4212403,4212502,4212601,4212650,4212700,4212809,4212908,4213005,4213104,4213153,4213203,4213302,4213351,4213401,4213500,4213609,4213708,4213807,4213906,4214003,4214102,4214151,4214201,4214300,4214409,4214508,4214607,4214706,4214805,4214904,4215000,4215059,4215075,4215091,4215109,4215208,4215307,4215356,4215406,4215455,4215505,4215554,4215604,4215653,4215679,4215687,4215695,4215703,4215752,4215802,4215901,4216008,4216057,4216107,4216206,4216255,4216305,4216354,4216404,4216503,4216602,4216701,4216800,4216909,4217006,4217105,4217154,4217204,4217253,4217303,4217402,4217501,4217550,4217600,4217709,4217758,4217808,4217907,4217956,4218004,4218103,4218202,4218251,4218301,4218350,4218400,4218509,4218608,4218707,4218756,4218806,4218855,4218905,4218954,4219002,4219101,4219150,4219176,4219200,4219309,4219358,4219408,4219507,4219606,4219705,4219853,4219903,4220000/v/109,214,215/p/2022/c81/2692,2693,2694,2695,2696,2697,2698,2699,2700,2701,2702,2703,2704,2705,2706,2707,2708,2709,2710,2711,2712,2713,2714,2715,2716,2717,2718,2719,2720,2721,2722,2723,2724,2726,2727,2728,2729,2730,2731,2732,2733,2734,2735,2736,2737,2738,2739,2740,2741,2742,2743,2744,2745,2746,2747,2748,2749,2750,2751,2752,2753,2754,2755,2756,2757,2758,2759,2760,2761,2762,2763,2764,2765,2766,2767,2768,2769,2770,2771,2772,2773,2774,2775,2776,2777,2778,2779,2780,2781,2782,2783,2784,2785,2786,2787,2788,2789,2790,2791,2792,2793,2794,2795,2796',
        'desc': 'PAM - Produção Agrícola Municipal 2022 (área plantada, colhida, valor)'
    }
}

print("⚠️  A API SIDRA está instável. Vou te guiar para download MANUAL dos dados.\n")
print("É rápido (5 minutos) e garante dados completos!\n")

print("=" * 80)
print("GUIA DE DOWNLOAD MANUAL - SIGA OS PASSOS:")
print("=" * 80)

print("\n📋 PASSO 1: PAM - Produção Agrícola Municipal")
print("-" * 80)
print("1. Acesse: https://sidra.ibge.gov.br/tabela/5457")
print("2. Configure:")
print("   - Unidade Territorial: Santa Catarina → Município → TODOS")
print("   - Produto: Soja, Milho, Arroz, Maçã")
print("   - Variável: TODAS (área plantada, colhida, valor)")
print("   - Ano: 2022")
print("3. Clique em 'Download' (canto superior direito)")
print("4. Escolha formato: CSV")
print(f"5. Salve como: {OUTPUT_DIR / 'pam_2022_manual.csv'}")
print("\n✅ Depois de salvar, pressione ENTER para continuar...")
input()

print("\n📋 PASSO 2: PPM - Pecuária Municipal")
print("-" * 80)
print("1. Acesse: https://sidra.ibge.gov.br/tabela/3939")
print("2. Configure:")
print("   - Unidade Territorial: Santa Catarina → Município → TODOS")
print("   - Tipo de rebanho: Bovinos, Suínos, Galinhas")
print("   - Variável: Número de cabeças")
print("   - Ano: 2022")
print("3. Clique em 'Download' → CSV")
print(f"4. Salve como: {OUTPUT_DIR / 'ppm_2022_manual.csv'}")
print("\n✅ Depois de salvar, pressione ENTER para continuar...")
input()

print("\n📋 PASSO 3: Censo Agropecuário 2017")
print("-" * 80)
print("1. Acesse: https://sidra.ibge.gov.br/tabela/6727")
print("2. Configure:")
print("   - Unidade Territorial: Santa Catarina → Município → TODOS")
print("   - Grupos de área total: TODOS")
print("   - Variável: Número de estabelecimentos")
print("   - Ano: 2017")
print("3. Clique em 'Download' → CSV")
print(f"4. Salve como: {OUTPUT_DIR / 'censo_agro_2017_manual.csv'}")
print("\n✅ Depois de salvar, pressione ENTER para continuar...")
input()

print("\n" + "=" * 80)
print("PROCESSANDO ARQUIVOS BAIXADOS")
print("=" * 80)

# Verificar se arquivos existem
files_to_check = [
    ('pam_2022_manual.csv', 'PAM'),
    ('ppm_2022_manual.csv', 'PPM'),
    ('censo_agro_2017_manual.csv', 'Censo Agro')
]

files_found = {}
for filename, label in files_to_check:
    filepath = OUTPUT_DIR / filename
    if filepath.exists():
        print(f"✓ {label}: arquivo encontrado")
        files_found[label] = filepath
    else:
        print(f"✗ {label}: arquivo NÃO encontrado em {filepath}")

if len(files_found) == 0:
    print("\n❌ Nenhum arquivo encontrado. Execute novamente e siga os passos.")
    exit(1)

print("\n" + "=" * 80)
print("PROCESSAMENTO DOS DADOS")
print("=" * 80)

# Processar arquivos encontrados
dados_processados = {}

if 'PAM' in files_found:
    print("\n[1/3] Processando PAM...")
    try:
        df_pam = pd.read_csv(files_found['PAM'], sep=';', encoding='latin1', skiprows=0)
        print(f"   Linhas: {len(df_pam)}, Colunas: {len(df_pam.columns)}")
        print(f"   Colunas detectadas: {list(df_pam.columns[:5])}...")
        dados_processados['pam'] = df_pam
    except Exception as e:
        print(f"   ✗ Erro ao processar: {e}")

if 'PPM' in files_found:
    print("\n[2/3] Processando PPM...")
    try:
        df_ppm = pd.read_csv(files_found['PPM'], sep=';', encoding='latin1', skiprows=0)
        print(f"   Linhas: {len(df_ppm)}, Colunas: {len(df_ppm.columns)}")
        dados_processados['ppm'] = df_ppm
    except Exception as e:
        print(f"   ✗ Erro ao processar: {e}")

if 'Censo Agro' in files_found:
    print("\n[3/3] Processando Censo Agropecuário...")
    try:
        df_censo = pd.read_csv(files_found['Censo Agro'], sep=';', encoding='latin1', skiprows=0)
        print(f"   Linhas: {len(df_censo)}, Colunas: {len(df_censo.columns)}")
        dados_processados['censo'] = df_censo
    except Exception as e:
        print(f"   ✗ Erro ao processar: {e}")

print("\n" + "=" * 80)
print("INSTRUÇÕES PARA PRÓXIMOS PASSOS")
print("=" * 80)

if len(dados_processados) > 0:
    print("\n✅ Arquivos processados com sucesso!")
    print("\nOs dados estão prontos, mas precisam ser TRANSFORMADOS para o formato esperado.")
    print("\n📧 Me mostre a estrutura dos arquivos executando:")
    print(f"   python -c \"import pandas as pd; df = pd.read_csv(r'{list(files_found.values())[0]}', sep=';', encoding='latin1'); print(df.head()); print('\\nColunas:', df.columns.tolist())\"")
    print("\nDepois, posso criar um script de transformação personalizado!")
else:
    print("\n❌ Nenhum arquivo foi processado com sucesso.")
    print("Verifique se os arquivos foram salvos corretamente.")

print("\n" + "=" * 80)
