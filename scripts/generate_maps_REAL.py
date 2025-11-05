"""
Gerador de Mapas - VERSÃO ATUALIZADA com dados REAIS
Gera choropleths e mapa interativo com ranking atualizado
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "data" / "outputs" / "maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GERANDO MAPAS COM DADOS REAIS")
print("=" * 80)

# Carregar dados
print("\n[1/3] Carregando dados...")
df_ranking = pd.read_csv(BASE_DIR / "data" / "outputs" / "ranking_municipal_drones_agro_REAL.csv")
print(f"✓ Ranking: {len(df_ranking)} municípios")

# Carregar GeoJSON municipal
geojson_path = DATA_DIR / "bc25_geojson" / "lml_municipio_a.geojson"
print(f"✓ Carregando geometrias: {geojson_path}")
gdf = gpd.read_file(geojson_path)
print(f"✓ GeoDataFrame: {len(gdf)} features")

# Merge ranking + geometrias
print("\n[2/3] Mesclando dados espaciais...")

# Detectar coluna de código de município (pode ser CD_MUN, geocodigo, ou cod_mun)
print(f"   Colunas disponíveis: {gdf.columns.tolist()[:10]}...")

if 'CD_MUN' in gdf.columns:
    gdf['cod_municipio'] = gdf['CD_MUN'].astype(int)
elif 'geocodigo' in gdf.columns:
    gdf['cod_municipio'] = gdf['geocodigo'].astype(int)
elif 'cod_mun' in gdf.columns:
    gdf['cod_municipio'] = gdf['cod_mun'].astype(int)
elif 'GEOCODIGO' in gdf.columns:
    gdf['cod_municipio'] = gdf['GEOCODIGO'].astype(str).str[:7].astype(int)
else:
    # Tentar encontrar coluna com código IBGE
    for col in gdf.columns:
        if 'cod' in col.lower() or 'geo' in col.lower():
            print(f"   Usando coluna: {col}")
            gdf['cod_municipio'] = gdf[col].astype(str).str[:7].astype(int)
            break

gdf_merged = gdf.merge(df_ranking, on='cod_municipio', how='left')

# Filtrar apenas SC
gdf_sc = gdf_merged[gdf_merged['cod_municipio'].astype(str).str.startswith('42')].copy()
print(f"✓ {len(gdf_sc)} municípios de SC com dados")

# Preencher NaN
gdf_sc['score_composto'] = gdf_sc['score_composto'].fillna(0)
gdf_sc['area_total_ha'] = gdf_sc['area_total_ha'].fillna(0)

# ==============================================
# MAPA 1: Score Composto
# ==============================================

print("\n[3/3] Gerando mapas...")
print("  [1/3] Choropleth - Score Composto...")

fig, ax = plt.subplots(1, 1, figsize=(16, 12))

gdf_sc.plot(
    column='score_composto',
    cmap='YlOrRd',
    linewidth=0.3,
    edgecolor='0.2',
    legend=True,
    ax=ax,
    missing_kwds={'color': 'lightgrey'}
)

ax.set_title('Potencial de Mercado para Drones Agrícolas em SC\n(Score Composto - Dados REAIS IBGE 2024)', 
             fontsize=18, fontweight='bold', pad=20)
ax.axis('off')

# Adicionar top 5 como anotações
top5 = gdf_sc.nlargest(5, 'score_composto')
for idx, row in top5.iterrows():
    if row.geometry and row.geometry.centroid:
        x = row.geometry.centroid.x
        y = row.geometry.centroid.y
        ax.annotate(
            f"{row['ranking']}. {row['nome_municipio'].replace(' (SC)', '')}",
            xy=(x, y),
            fontsize=9,
            fontweight='bold',
            color='darkred',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
        )

plt.tight_layout()
output_file = OUTPUT_DIR / "mapa_score_composto_REAL.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"    ✓ Salvo: {output_file}")

# ==============================================
# MAPA 2: Área Agrícola Total
# ==============================================

print("  [2/3] Choropleth - Área Agrícola...")

fig, ax = plt.subplots(1, 1, figsize=(16, 12))

gdf_sc.plot(
    column='area_total_ha',
    cmap='Greens',
    linewidth=0.3,
    edgecolor='0.2',
    legend=True,
    ax=ax,
    missing_kwds={'color': 'lightgrey'}
)

ax.set_title('Área Agrícola Total por Município em SC\n(Dados REAIS IBGE - PAM 2024)', 
             fontsize=18, fontweight='bold', pad=20)
ax.axis('off')

# Adicionar top 5 por área
top5_area = gdf_sc.nlargest(5, 'area_total_ha')
for idx, row in top5_area.iterrows():
    if row.geometry and row.geometry.centroid:
        x = row.geometry.centroid.x
        y = row.geometry.centroid.y
        ax.annotate(
            f"{row['nome_municipio'].replace(' (SC)', '')}\n{row['area_total_ha']:,.0f} ha",
            xy=(x, y),
            fontsize=8,
            fontweight='bold',
            color='darkgreen',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
        )

plt.tight_layout()
output_file = OUTPUT_DIR / "mapa_area_agricola_REAL.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"    ✓ Salvo: {output_file}")

# ==============================================
# MAPA 3: Interativo (Folium)
# ==============================================

print("  [3/3] Mapa Interativo...")

# Converter para WGS84 se necessário
if gdf_sc.crs != 'EPSG:4326':
    gdf_sc = gdf_sc.to_crs('EPSG:4326')

# Centro de SC
center_lat = -27.5
center_lon = -50.5

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    min_zoom=6,      # Limite de zoom afastado (visão geral SC)
    max_zoom=12,     # Limite de zoom aproximado (nível municipal)
    tiles='OpenStreetMap',
    max_bounds=True  # Restringe navegação aos limites
)

# Definir limites geográficos de SC (bounding box)
# SC: aproximadamente lat -29.4 a -25.9, lon -53.8 a -48.3
south_west = [-29.5, -54.0]  # Canto sudoeste
north_east = [-25.8, -48.0]  # Canto nordeste
m.fit_bounds([south_west, north_east])

# Adicionar camada choropleth
folium.Choropleth(
    geo_data=gdf_sc,
    name='Score Composto',
    data=gdf_sc,
    columns=['cod_municipio', 'score_composto'],
    key_on='feature.properties.cod_municipio',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Potencial de Mercado (Score)',
    highlight=True
).add_to(m)

# Adicionar tooltip com informações
folium.GeoJson(
    gdf_sc,
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

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Adicionar título
title_html = '''
<div style="position: fixed; 
     top: 10px; left: 50px; width: 400px; height: 90px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:16px; padding: 10px">
     <b>Geomarketing: Drones Agrícolas em SC</b><br>
     Dados REAIS IBGE (PAM 2024)<br>
     <small>Passe o mouse sobre os municípios para ver detalhes</small>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Adicionar rodapé com créditos
footer_html = '''
<div style="position: fixed; 
     bottom: 10px; left: 10px; width: 450px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:12px; padding: 8px; opacity: 0.9;">
     <b>Autor:</b> Ronan Armando Caetano<br>
     <small>📚 Graduando em Ciências Biológicas - UFSC | 🗺️ Técnico em Geoprocessamento - IFSC</small><br>
     <hr style="margin: 5px 0; border: 0; border-top: 1px solid #ccc;">
     <small><b>Fonte dos Dados:</b> IBGE/SIDRA - Tabela 5457 (PAM 2024) · Base Cartográfica 2025 · OpenStreetMap</small><br>
     <small><b>Tecnologias:</b> Python 3.13 · GeoPandas · Folium · Matplotlib · Shapely</small>
</div>
'''
m.get_root().html.add_child(folium.Element(footer_html))

# Salvar
output_file = OUTPUT_DIR / "mapa_interativo_REAL.html"
m.save(str(output_file))
print(f"    ✓ Salvo: {output_file} ({output_file.stat().st_size / 1024 / 1024:.1f} MB)")

print("\n" + "=" * 80)
print("✅ MAPAS GERADOS COM SUCESSO!")
print("=" * 80)

print("\n📂 Arquivos gerados em data/outputs/maps/:")
print("  - mapa_score_composto_REAL.png")
print("  - mapa_area_agricola_REAL.png")
print("  - mapa_interativo_REAL.html")

print("\n🎯 Principais destaques visuais:")
print(f"  1. {gdf_sc.nlargest(1, 'score_composto')['nome_municipio'].values[0]} - Score {gdf_sc['score_composto'].max():.1f}")
print(f"  2. {gdf_sc.nlargest(1, 'area_total_ha')['nome_municipio'].values[0]} - {gdf_sc['area_total_ha'].max():,.0f} ha")
print(f"  3. Região com maior concentração: Planalto Serrano + Norte")
