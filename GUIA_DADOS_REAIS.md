# GUIA COMPLETO: ONDE BUSCAR DADOS REAIS IBGE

## 🎯 RESUMO: 3 Opções (da mais fácil para a mais completa)

---

## ✅ **OPÇÃO 1: DOWNLOAD MANUAL SIDRA (5 minutos - RECOMENDADO)**

### Vantagens:
- ✓ Não precisa de conta/autenticação
- ✓ Interface amigável
- ✓ Dados oficiais e atualizados
- ✓ Formato CSV pronto para usar

### Passo a passo:

#### 1️⃣ **PAM - Produção Agrícola Municipal (área plantada)**

```
URL: https://sidra.ibge.gov.br/tabela/5457

Configuração:
- Variável: "Área plantada (Hectares)"
- Unidade Territorial: Santa Catarina > Município > TODOS
- Produto: Soja (em grão), Milho (em grão), Arroz (em casca), Maçã
- Ano: 2022 (ou último disponível)

Salvar como: data/ibge_agro/pam_area_plantada_sc_2022.csv
```

#### 2️⃣ **PAM - Valor da Produção**

```
URL: https://sidra.ibge.gov.br/tabela/5457

Configuração:
- Variável: "Valor da produção (Mil Reais)"
- [Mesma configuração acima]

Salvar como: data/ibge_agro/pam_valor_producao_sc_2022.csv
```

#### 3️⃣ **PPM - Pecuária Municipal**

```
URL: https://sidra.ibge.gov.br/tabela/3939

Configuração:
- Variável: "Número de cabeças"
- Unidade Territorial: Santa Catarina > Município > TODOS
- Tipo de rebanho: Bovinos, Suínos, Galinhas
- Ano: 2022

Salvar como: data/ibge_agro/ppm_rebanhos_sc_2022.csv
```

#### 4️⃣ **Censo Agropecuário - Estabelecimentos**

```
URL: https://sidra.ibge.gov.br/tabela/6727

Configuração:
- Variável: "Número de estabelecimentos agropecuários"
- Unidade Territorial: Santa Catarina > Município > TODOS
- Grupos de área total: TODOS
- Ano: 2017 (último Censo)

Salvar como: data/ibge_agro/censo_agro_estabelecimentos_sc_2017.csv
```

---

## ✅ **OPÇÃO 2: BASE DOS DADOS (Configuração única, depois é automático)**

### Vantagens:
- ✓ Dados limpos e padronizados
- ✓ SQL queries simples
- ✓ Atualização automática

### Configuração (1 vez só):

1. **Criar projeto no Google Cloud:**
   - Acesse: https://console.cloud.google.com
   - Crie um projeto (ex: "geomarketing-sc")
   - Anote o PROJECT_ID

2. **Instalar e autenticar:**
   ```bash
   pip install basedosdados
   ```

3. **Primeiro uso (abre navegador para autenticar):**
   ```python
   import basedosdados as bd
   
   # PAM - Produção Agrícola
   bd.download(
       savepath='data/ibge_agro/pam_sc_2022.csv',
       query='''
           SELECT * 
           FROM `basedosdados.br_ibge_pam.municipio` 
           WHERE sigla_uf = "SC" 
             AND ano = 2022
             AND produto IN ("Soja (em grão)", "Milho (em grão)", 
                            "Arroz (em casca)", "Maçã")
       ''',
       billing_project_id='SEU_PROJECT_ID'  # Substitua!
   )
   ```

### Depois de configurado, queries automáticas:

```python
import basedosdados as bd

# PAM
df_pam = bd.read_table(
    dataset_id='br_ibge_pam',
    table_id='municipio',
    billing_project_id='SEU_PROJECT_ID'
)
df_pam_sc = df_pam[df_pam['sigla_uf'] == 'SC']

# PPM
df_ppm = bd.read_table(
    dataset_id='br_ibge_ppm',
    table_id='municipio',
    billing_project_id='SEU_PROJECT_ID'
)
df_ppm_sc = df_ppm[df_ppm['sigla_uf'] == 'SC']
```

📚 **Tutorial completo:** https://basedosdados.org/docs/

---

## ✅ **OPÇÃO 3: WEB SCRAPING (Automático, mas pode quebrar)**

### Usar biblioteca sidrapy com sintaxe corrigida:

```python
import sidrapy

# PAM - Produção Agrícola
pam = sidrapy.get_table(
    table_code='5457',
    territorial_level='6',  # município
    ibge_territorial_code='all',  # todos
    variable='109',  # área plantada
    classifications={'81': 'all'},  # produtos
    period='2022'
)

# Filtrar SC
pam_sc = pam[pam['D3C'].str.startswith('42')]
```

⚠️ **Problema:** Sintaxe da API muda frequentemente.

---

## 📊 **DADOS QUE VOCÊ PRECISA**

### Para refazer o ranking com dados reais:

| Dataset | Tabela SIDRA | Variáveis | Ano |
|---------|--------------|-----------|-----|
| Área plantada | 5457 (PAM) | Soja, Milho, Arroz, Maçã | 2022 |
| Valor produção | 5457 (PAM) | Valor total | 2022 |
| Rebanhos | 3939 (PPM) | Bovinos, Suínos, Aves | 2022 |
| Estabelecimentos | 6727 (Censo) | Por grupo de área | 2017 |

### Formato final esperado (CSV):

```
cod_municipio,nome_municipio,regiao_estimada,
area_total_ha,area_soja_ha,area_milho_ha,area_arroz_ha,area_maca_ha,
valor_producao_mil_reais,
rebanho_bovinos,rebanho_suinos,rebanho_aves,
estabelecimentos_total,estabelecimentos_grandes_100ha_plus
```

---

## 🚀 **DEPOIS DE BAIXAR OS DADOS**

### Execute o processador automático:

```bash
python scripts/process_real_ibge_data.py
```

Esse script vai:
1. Ler os CSVs baixados
2. Limpar e padronizar
3. Gerar o formato esperado
4. Salvar como `dados_agro_sc_real.csv`

Depois, recalcule o ranking:
```bash
python scripts/calculate_agro_indicators_ranking.py
```

---

## 💡 **MINHA RECOMENDAÇÃO**

**Use OPÇÃO 1 (download manual SIDRA)** porque:
- ✓ Funciona 100%
- ✓ Não precisa configurar nada
- ✓ Leva 5 minutos
- ✓ Dados oficiais garantidos

Depois que tiver os CSVs, posso criar um script de processamento personalizado!

---

## 📧 **PRÓXIMO PASSO**

Me avise quando tiver baixado os arquivos ou me diga qual opção prefere que eu te ajude a configurar! 🎯
