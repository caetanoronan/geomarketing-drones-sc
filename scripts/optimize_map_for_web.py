"""
Otimizador de Mapa Interativo para GitHub Pages
Reduz tamanho do arquivo simplificando geometrias
Mantém qualidade visual e dados do ranking
"""

import pandas as pd
import geopandas as gpd
import folium
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "data" / "outputs" / "maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("OTIMIZANDO MAPA PARA GITHUB PAGES")
print("=" * 80)

# Carregar dados
print("\n[1/5] Carregando dados...")
df_ranking = pd.read_csv(BASE_DIR / "data" / "outputs" / "ranking_municipal_drones_agro_REAL.csv")
print(f"✓ Ranking: {len(df_ranking)} municípios")

# Carregar GeoJSON municipal
geojson_path = DATA_DIR / "bc25_geojson" / "lml_municipio_a.geojson"
print(f"✓ Carregando geometrias: {geojson_path.name}")
gdf = gpd.read_file(geojson_path)
original_size_mb = geojson_path.stat().st_size / 1024 / 1024
print(f"✓ Tamanho original GeoJSON: {original_size_mb:.1f} MB")

# Detectar coluna de código
print("\n[2/5] Preparando dados...")
if 'CD_MUN' in gdf.columns:
    gdf['cod_municipio'] = gdf['CD_MUN'].astype(int)
elif 'geocodigo' in gdf.columns:
    gdf['cod_municipio'] = gdf['geocodigo'].astype(int)
elif 'cod_mun' in gdf.columns:
    gdf['cod_municipio'] = gdf['cod_mun'].astype(int)
elif 'GEOCODIGO' in gdf.columns:
    gdf['cod_municipio'] = gdf['GEOCODIGO'].astype(str).str[:7].astype(int)
else:
    for col in gdf.columns:
        if 'cod' in col.lower() or 'geo' in col.lower():
            gdf['cod_municipio'] = gdf[col].astype(str).str[:7].astype(int)
            break

# Merge com ranking
gdf_merged = gdf.merge(df_ranking, on='cod_municipio', how='left')

# Filtrar apenas SC
gdf_sc = gdf_merged[gdf_merged['cod_municipio'].astype(str).str.startswith('42')].copy()
print(f"✓ {len(gdf_sc)} municípios de SC")

# Preencher NaN
gdf_sc['score_composto'] = gdf_sc['score_composto'].fillna(0)
gdf_sc['area_total_ha'] = gdf_sc['area_total_ha'].fillna(0)

# Converter para WGS84
if gdf_sc.crs != 'EPSG:4326':
    gdf_sc = gdf_sc.to_crs('EPSG:4326')

# ==============================================
# SIMPLIFICAÇÃO DE GEOMETRIAS
# ==============================================

print("\n[3/5] Simplificando geometrias...")
print("   Testando níveis de tolerância...")

# Testar diferentes níveis de simplificação
tolerances = [0.001, 0.005, 0.01, 0.02]
best_tolerance = 0.005  # Valor padrão

for tol in tolerances:
    gdf_test = gdf_sc.copy()
    gdf_test['geometry'] = gdf_test['geometry'].simplify(tolerance=tol, preserve_topology=True)
    
    # Salvar temporário para medir tamanho
    temp_file = OUTPUT_DIR / "temp_test.geojson"
    gdf_test[['cod_municipio', 'geometry']].to_file(temp_file, driver='GeoJSON')
    test_size_mb = temp_file.stat().st_size / 1024 / 1024
    reduction = (1 - test_size_mb / original_size_mb) * 100
    
    print(f"   Tolerância {tol}: {test_size_mb:.1f} MB (-{reduction:.0f}%)")
    
    # Escolher tolerância que resulta em ~5-10 MB
    if test_size_mb < 10 and test_size_mb > 3:
        best_tolerance = tol
        break
    
    temp_file.unlink()

print(f"✓ Tolerância escolhida: {best_tolerance}")

# Aplicar simplificação final
gdf_sc_simplified = gdf_sc.copy()
gdf_sc_simplified['geometry'] = gdf_sc_simplified['geometry'].simplify(
    tolerance=best_tolerance, 
    preserve_topology=True
)

print(f"✓ Geometrias simplificadas")

# ==============================================
# GERAR MAPA LEVE
# ==============================================

print("\n[4/5] Gerando mapa otimizado...")

# Centro de SC
center_lat = -27.5
center_lon = -50.5

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    min_zoom=6,
    max_zoom=12,
    tiles='OpenStreetMap',
    max_bounds=True
)

# Limites geográficos de SC
south_west = [-29.5, -54.0]
north_east = [-25.8, -48.0]
m.fit_bounds([south_west, north_east])

# Adicionar camada choropleth
folium.Choropleth(
    geo_data=gdf_sc_simplified,
    name='Score Composto',
    data=gdf_sc_simplified,
    columns=['cod_municipio', 'score_composto'],
    key_on='feature.properties.cod_municipio',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Potencial de Mercado (Score)',
    highlight=True
).add_to(m)

# Adicionar tooltip
folium.GeoJson(
    gdf_sc_simplified,
    name='Informações',
    tooltip=folium.GeoJsonTooltip(
        fields=['nome_municipio', 'ranking', 'score_composto', 'area_total_ha', 
                'area_soja_ha', 'area_milho_ha', 'area_arroz_ha', 
                'estabelecimentos_grandes_100ha_plus'],
        aliases=['Município:', 'Ranking:', 'Score:', 'Área Total (ha):', 
                 'Soja (ha):', 'Milho (ha):', 'Arroz (ha):', 
                 'Grandes Produtores:'],
        localize=True,
        style="font-size: 12px;"
    ),
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': 'transparent',
        'weight': 0
    }
).add_to(m)

# Controle de camadas
folium.LayerControl().add_to(m)

# Título
title_html = '''
<div style="position: fixed; 
     top: 10px; left: 50px; width: 450px; height: 110px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:16px; padding: 10px">
     <b>Geomarketing: Drones Agrícolas em SC</b><br>
     Dados REAIS IBGE (PAM 2024)<br>
     <small>Passe o mouse sobre os municípios para ver detalhes</small><br>
     <small style="color: #666;">⚡ Versão Web Otimizada - Geometrias simplificadas para carregamento rápido</small>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Rodapé com créditos
footer_html = '''
<div style="position: fixed; 
     bottom: 10px; left: 10px; width: 500px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:12px; padding: 8px; opacity: 0.9;">
     <b>Autor:</b> Ronan Armando Caetano<br>
     <small>📚 Graduando em Ciências Biológicas - UFSC | 🗺️ Técnico em Geoprocessamento - IFSC</small><br>
     <hr style="margin: 5px 0; border: 0; border-top: 1px solid #ccc;">
     <small><b>Fonte dos Dados:</b> IBGE/SIDRA - Tabela 5457 (PAM 2024) · Base Cartográfica 2025 · OpenStreetMap</small><br>
     <small><b>Tecnologias:</b> Python 3.13 · GeoPandas · Folium · Matplotlib · Shapely</small><br>
     <small style="color: #666;">⚡ Versão otimizada para web - Para versão HD completa, baixe o arquivo original</small>
</div>
'''
m.get_root().html.add_child(folium.Element(footer_html))

# Salvar versão otimizada
output_file = OUTPUT_DIR / "mapa_interativo_WEB.html"
m.save(str(output_file))
optimized_size_mb = output_file.stat().st_size / 1024 / 1024
print(f"✓ Mapa web salvo: {output_file.name} ({optimized_size_mb:.1f} MB)")

# Comparar tamanhos
original_map = OUTPUT_DIR / "mapa_interativo_REAL.html"
if original_map.exists():
    original_map_size_mb = original_map.stat().st_size / 1024 / 1024
    reduction_percent = (1 - optimized_size_mb / original_map_size_mb) * 100
    print(f"✓ Redução de tamanho: {reduction_percent:.1f}% (de {original_map_size_mb:.1f} MB para {optimized_size_mb:.1f} MB)")

# ==============================================
# CRIAR README PARA GITHUB PAGES
# ==============================================

print("\n[5/5] Criando documentação...")

readme_content = f"""# 🚁 Análise de Geomarketing: Drones Agrícolas em Santa Catarina

## 📊 Sobre o Projeto

Análise completa do potencial de mercado para operações de **aluguel e venda de drones agrícolas** em Santa Catarina, utilizando dados oficiais do IBGE (PAM 2024).

## 🗺️ Mapas Disponíveis

### 📱 Versão Web (Recomendada)
- **Arquivo:** `mapa_interativo_WEB.html` ({optimized_size_mb:.1f} MB)
- **Carregamento:** Rápido (2-5 segundos)
- **Ideal para:** Navegação online, celulares, tablets
- [🌐 Abrir Mapa Interativo Web](maps/mapa_interativo_WEB.html)

### 💾 Versão HD Completa
- **Arquivo:** `mapa_interativo_REAL.html` ({original_map_size_mb:.1f} MB)
- **Carregamento:** Lento (10-60 segundos)
- **Ideal para:** Análise detalhada offline, máxima precisão
- [⬇️ Download Versão HD](maps/mapa_interativo_REAL.html) (clique direito → salvar)

### 🖼️ Mapas Estáticos
- [Score Composto](maps/mapa_score_composto_REAL.png)
- [Área Agrícola](maps/mapa_area_agricola_REAL.png)

## 🏆 Principais Descobertas

### TOP 5 Municípios
1. **Campos Novos** (Serrana) - Score 69.1, 90.879 ha
2. **Abelardo Luz** (Norte) - Score 50.8, 69.401 ha
3. **Mafra** (Norte) - Score 40.6, 52.534 ha
4. **Curitibanos** (Serrana) - Score 40.3, 28.708 ha
5. **Canoinhas** (Norte) - Score 34.4, 48.596 ha

### Estatísticas SC
- 📍 **295 municípios** analisados
- 🌾 **1,68 milhões de hectares** agrícolas
- 🌱 **814 mil ha de soja** (48,3% do total)
- 🏭 **28.599 estabelecimentos** >100 ha

## 📂 Arquivos do Projeto

### Dados
- `ranking_municipal_drones_agro_REAL.csv` - Ranking completo 295 municípios
- `pam_area_plantada_sc_2024.csv` - Dados brutos IBGE

### Relatórios
- `apresentacao_drones_agro_sc.html` - Dashboard interativo 7 abas
- `ENTREGA_FINAL_ANALISE_REAL.md` - Relatório executivo completo

### Scripts Python
- `process_pam_corrected.py` - Processamento dados SIDRA
- `consolidate_real_data.py` - Consolidação ranking
- `generate_maps_REAL.py` - Geração de mapas
- `optimize_map_for_web.py` - Otimização para web

## 👨‍💻 Autor

**Ronan Armando Caetano**
- 📚 Graduando em Ciências Biológicas - UFSC
- 🗺️ Técnico em Geoprocessamento - IFSC
- 📧 [Email](mailto:seu-email@exemplo.com) · [GitHub](https://github.com/seu-usuario) · [LinkedIn](https://linkedin.com/in/seu-perfil)

## 🛠️ Tecnologias

**Python & Bibliotecas:** pandas · geopandas · folium · matplotlib · shapely · fiona · pyshp

**Dados:** IBGE SIDRA (PAM 2024) · Base Cartográfica 2025 · OpenStreetMap

**Desenvolvimento:** VS Code · Python 3.13 · PowerShell · GitHub Copilot

## 📜 Licença

© 2025 Ronan Armando Caetano | IFSC Geoprocessamento

Desenvolvido com assistência de 🤖 GitHub Copilot

---

**Última atualização:** Novembro 2025
"""

readme_file = BASE_DIR / "README.md"
with open(readme_file, 'w', encoding='utf-8') as f:
    f.write(readme_content)
print(f"✓ README.md criado")

# Criar .gitignore
gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data (arquivos muito grandes)
data/bc25_geojson/*.geojson
*.gpkg

# Mapa original pesado (opcional - descomente se quiser incluir no git)
# data/outputs/maps/mapa_interativo_REAL.html

# Temporários
*.tmp
*.bak
temp_*
"""

gitignore_file = BASE_DIR / ".gitignore"
with open(gitignore_file, 'w', encoding='utf-8') as f:
    f.write(gitignore_content)
print(f"✓ .gitignore criado")

print("\n" + "=" * 80)
print("✅ OTIMIZAÇÃO CONCLUÍDA!")
print("=" * 80)

print(f"""
📊 RESULTADOS:

📁 Arquivos Gerados:
  ✓ mapa_interativo_WEB.html ({optimized_size_mb:.1f} MB) - VERSÃO OTIMIZADA
  ✓ mapa_interativo_REAL.html ({original_map_size_mb:.1f} MB) - VERSÃO ORIGINAL
  ✓ README.md - Documentação do projeto
  ✓ .gitignore - Configuração Git

📉 Redução de Tamanho:
  • Tamanho original: {original_map_size_mb:.1f} MB
  • Tamanho otimizado: {optimized_size_mb:.1f} MB
  • Redução: {reduction_percent:.1f}%

🚀 Próximos Passos para GitHub Pages:

1. Inicializar Git (se ainda não fez):
   git init
   git add .
   git commit -m "Análise Geomarketing Drones Agrícolas SC"

2. Criar repositório no GitHub e enviar:
   git remote add origin https://github.com/seu-usuario/seu-repositorio.git
   git branch -M main
   git push -u origin main

3. Ativar GitHub Pages:
   • Ir em Settings → Pages
   • Source: Deploy from a branch
   • Branch: main / (root)
   • Save

4. Seu site estará em:
   https://seu-usuario.github.io/seu-repositorio/

📌 IMPORTANTE:
  • Use mapa_interativo_WEB.html na apresentação (versão leve)
  • Mantenha mapa_interativo_REAL.html para download opcional
  • Edite README.md com seus links pessoais
""")

print("🎯 Tudo pronto para publicar no GitHub Pages!")
