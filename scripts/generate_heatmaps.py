"""
Geração de Mapas de Calor (Heatmaps) - Drones Agrícolas SC
Autor: Ronan Armando Caetano
"""

import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import json
from pathlib import Path

print("=" * 60)
print("🔥 GERAÇÃO DE MAPAS DE CALOR - DRONES AGRÍCOLAS SC")
print("=" * 60)

# Caminhos
base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"
output_dir = data_dir / "outputs" / "maps"
output_dir.mkdir(parents=True, exist_ok=True)

# [1] Carregar dados
print("\n[1/5] Carregando dados...")
malha_path = data_dir / "SC_Municipios_2024" / "SC_Municipios_2024.shp"
ranking_path = data_dir / "outputs" / "ranking_municipal_drones_agro_REAL.csv"

gdf = gpd.read_file(malha_path)
df_ranking = pd.read_csv(ranking_path)

# Limpar nomes dos municípios no ranking (remover " (SC)")
df_ranking['nome_municipio_clean'] = df_ranking['nome_municipio'].str.replace(' (SC)', '', regex=False)

# Merge dados
gdf = gdf.merge(df_ranking, left_on='NM_MUN', right_on='nome_municipio_clean', how='left')
gdf = gdf.to_crs(epsg=4326)  # WGS84

# Calcular centroides
gdf['lat'] = gdf.geometry.centroid.y
gdf['lon'] = gdf.geometry.centroid.x

print(f"✓ {len(gdf)} municípios carregados")

# [2] Preparar dados para heatmaps
print("\n[2/5] Preparando dados para heatmaps...")

# Remover NaN
gdf_valid = gdf[gdf['score_composto'].notna()].copy()

# Normalizar scores para intensidade do heatmap (0-1)
def normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

# Criar diferentes datasets de heatmap
heatmap_data = {
    'score_composto': [],
    'area_agricola': [],
    'densidade_agricola': [],
    'area_soja': [],
    'estabelecimentos': []
}

for idx, row in gdf_valid.iterrows():
    lat, lon = row['lat'], row['lon']
    
    # Score composto (normalizado para 0-1)
    score_norm = normalize(gdf_valid['score_composto']).loc[idx]
    heatmap_data['score_composto'].append([lat, lon, score_norm])
    
    # Área agrícola (peso baseado em hectares)
    area_weight = min(row['area_total_ha'] / 100000, 1.0)  # Max 100k ha = peso 1.0
    heatmap_data['area_agricola'].append([lat, lon, area_weight])
    
    # Densidade agrícola (usar ind_area_total normalizado)
    dens_norm = row['ind_area_total'] / 100.0  # já está em 0-100, normalizar para 0-1
    heatmap_data['densidade_agricola'].append([lat, lon, dens_norm])
    
    # Área de soja
    soja_weight = min(row['area_soja_ha'] / 50000, 1.0)  # Max 50k ha = peso 1.0
    heatmap_data['area_soja'].append([lat, lon, soja_weight])
    
    # Estabelecimentos grandes
    estab_weight = min(row['estabelecimentos_grandes_100ha_plus'] / 200, 1.0)  # Max 200 = peso 1.0
    heatmap_data['estabelecimentos'].append([lat, lon, estab_weight])

print("✓ Dados preparados para 5 tipos de heatmap")

# [3] Criar mapas de calor individuais
print("\n[3/5] Gerando mapas de calor individuais...")

# Centro de SC
center_lat = gdf['lat'].mean()
center_lon = gdf['lon'].mean()

heatmap_configs = {
    'score_composto': {
        'title': 'Mapa de Calor - Score Composto (Potencial Geral)',
        'gradient': {0.0: 'blue', 0.3: 'cyan', 0.5: 'lime', 0.7: 'yellow', 1.0: 'red'},
        'file': 'heatmap_score_composto.html'
    },
    'area_agricola': {
        'title': 'Mapa de Calor - Área Agrícola Total',
        'gradient': {0.0: 'navy', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1.0: 'darkred'},
        'file': 'heatmap_area_agricola.html'
    },
    'densidade_agricola': {
        'title': 'Mapa de Calor - Densidade Agrícola (ha/km²)',
        'gradient': {0.0: 'purple', 0.3: 'blue', 0.5: 'green', 0.7: 'yellow', 1.0: 'red'},
        'file': 'heatmap_densidade.html'
    },
    'area_soja': {
        'title': 'Mapa de Calor - Área de Soja',
        'gradient': {0.0: 'lightgreen', 0.3: 'green', 0.6: 'gold', 0.8: 'orange', 1.0: 'red'},
        'file': 'heatmap_soja.html'
    },
    'estabelecimentos': {
        'title': 'Mapa de Calor - Estabelecimentos Grandes (>100 ha)',
        'gradient': {0.0: 'lightblue', 0.3: 'blue', 0.5: 'purple', 0.7: 'red', 1.0: 'darkred'},
        'file': 'heatmap_estabelecimentos.html'
    }
}

for key, config in heatmap_configs.items():
    # Calcular bounds de SC
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles='CartoDB positron',
        min_zoom=6,
        max_zoom=13,
        max_bounds=True
    )
    
    # Definir limites da visualização para SC
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    # Adicionar limites dos municípios
    folium.GeoJson(
        gdf[['geometry', 'NM_MUN']],
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#999999',
            'weight': 0.5,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(fields=['NM_MUN'], aliases=['Município:'])
    ).add_to(m)
    
    # Adicionar limite de SC
    sc_boundary = gdf.dissolve()
    folium.GeoJson(
        sc_boundary,
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#FF0000',
            'weight': 2.5,
            'fillOpacity': 0,
            'dashArray': '5, 5'
        }
    ).add_to(m)
    
    # Adicionar camada de heatmap
    HeatMap(
        heatmap_data[key],
        min_opacity=0.3,
        max_zoom=13,
        radius=25,
        blur=35,
        gradient=config['gradient']
    ).add_to(m)
    
    # Adicionar título
    title_html = f'''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 600px; height: 60px; 
                background-color: white; border: 2px solid grey;
                z-index: 9999; font-size: 16px; padding: 10px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
                border-radius: 5px;">
        <h4 style="margin: 0; color: #333;">{config['title']}</h4>
        <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
            Cores mais quentes = maior concentração/potencial
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Salvar
    output_path = output_dir / config['file']
    m.save(str(output_path))
    print(f"✓ {config['file']}")

# [4] Criar mapa de calor COMBINADO com camadas
print("\n[4/5] Gerando mapa de calor combinado (multicamadas)...")

# Calcular bounds de SC
bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

m_combined = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    tiles='CartoDB positron',
    min_zoom=6,
    max_zoom=13,
    max_bounds=True
)

# Definir limites da visualização para SC
m_combined.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

# Adicionar camada de limites municipais
municipios_layer = folium.FeatureGroup(name='🗺️ Limites Municipais', show=True)
folium.GeoJson(
    gdf[['geometry', 'NM_MUN']],
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': '#666666',
        'weight': 1,
        'fillOpacity': 0
    },
    tooltip=folium.GeoJsonTooltip(fields=['NM_MUN'], aliases=['Município:'])
).add_to(municipios_layer)
municipios_layer.add_to(m_combined)

# Adicionar camada do contorno de SC (dissolver todos os municípios)
sc_boundary = gdf.dissolve()
sc_layer = folium.FeatureGroup(name='📍 Limite de Santa Catarina', show=True)
folium.GeoJson(
    sc_boundary,
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': '#FF0000',
        'weight': 3,
        'fillOpacity': 0,
        'dashArray': '5, 5'
    }
).add_to(sc_layer)
sc_layer.add_to(m_combined)

# Adicionar múltiplas camadas de heatmap
for key, config in heatmap_configs.items():
    heat_layer = folium.FeatureGroup(name=config['title'], show=(key == 'score_composto'))
    HeatMap(
        heatmap_data[key],
        min_opacity=0.3,
        max_zoom=13,
        radius=25,
        blur=35,
        gradient=config['gradient']
    ).add_to(heat_layer)
    heat_layer.add_to(m_combined)

# Adicionar controle de camadas
folium.LayerControl(position='topright', collapsed=False).add_to(m_combined)

# Título
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 650px; height: 80px; 
            background-color: white; border: 2px solid grey;
            z-index: 9999; font-size: 16px; padding: 10px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
            border-radius: 5px;">
    <h4 style="margin: 0; color: #333;">🔥 Mapas de Calor Combinados - Drones Agrícolas SC</h4>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
        Use o controle de camadas (canto superior direito) para alternar entre diferentes indicadores
    </p>
</div>
'''
m_combined.get_root().html.add_child(folium.Element(title_html))

# Adicionar legenda
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: auto; 
            background-color: white; border: 2px solid grey;
            z-index: 9999; font-size: 12px; padding: 10px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
            border-radius: 5px;">
    <h5 style="margin: 0 0 10px 0;">Interpretação das Cores</h5>
    <div style="background: linear-gradient(to right, blue, cyan, lime, yellow, red); 
                height: 20px; border-radius: 3px; margin-bottom: 5px;"></div>
    <div style="display: flex; justify-content: space-between; font-size: 10px;">
        <span>Baixo</span>
        <span>Médio</span>
        <span>Alto</span>
    </div>
</div>
'''
m_combined.get_root().html.add_child(folium.Element(legend_html))

# Footer com créditos
footer_html = '''
<div style="position: fixed; 
            bottom: 10px; right: 10px; width: 300px; height: auto; 
            background-color: rgba(255,255,255,0.9); border: 1px solid grey;
            z-index: 9999; font-size: 10px; padding: 8px;
            border-radius: 5px;">
    <strong>Autor:</strong> Ronan Armando Caetano (UFSC/IFSC)<br>
    <strong>Dados:</strong> IBGE/SIDRA - PAM 2024<br>
    <strong>Tecnologia:</strong> Python, GeoPandas, Folium
</div>
'''
m_combined.get_root().html.add_child(folium.Element(footer_html))

# Salvar
combined_path = output_dir / "heatmap_combinado.html"
m_combined.save(str(combined_path))
print(f"✓ heatmap_combinado.html")

# [5] Criar mapa de calor OTIMIZADO para web
print("\n[5/5] Gerando versão otimizada para web...")

# Usar apenas TOP 50 municípios para reduzir tamanho
top50 = gdf_valid.nlargest(50, 'score_composto')

heatmap_top50 = []
for _, row in top50.iterrows():
    score_norm = (row['score_composto'] - gdf_valid['score_composto'].min()) / \
                 (gdf_valid['score_composto'].max() - gdf_valid['score_composto'].min())
    heatmap_top50.append([row['lat'], row['lon'], score_norm])

# Calcular bounds de SC
bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

m_web = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    tiles='CartoDB positron',
    max_bounds=True,
    min_zoom=6,
    max_zoom=13
)

# Definir limites da visualização para SC
m_web.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

# Adicionar limites dos municípios
folium.GeoJson(
    gdf[['geometry', 'NM_MUN']],
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': '#888888',
        'weight': 0.8,
        'fillOpacity': 0
    },
    tooltip=folium.GeoJsonTooltip(fields=['NM_MUN'], aliases=['Município:'])
).add_to(m_web)

# Adicionar limite de SC
sc_boundary = gdf.dissolve()
folium.GeoJson(
    sc_boundary,
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': '#FF0000',
        'weight': 3,
        'fillOpacity': 0,
        'dashArray': '5, 5'
    }
).add_to(m_web)

HeatMap(
    heatmap_top50,
    min_opacity=0.4,
    max_zoom=13,
    radius=30,
    blur=40,
    gradient={0.0: 'blue', 0.3: 'cyan', 0.5: 'lime', 0.7: 'yellow', 1.0: 'red'}
).add_to(m_web)

# Adicionar marcadores nos TOP 5
top5 = top50.nlargest(5, 'score_composto')
for idx, row in top5.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"<b>{row['nome_municipio']}</b><br>Score: {row['score_composto']:.1f}<br>Área: {row['area_total_ha']:,.0f} ha",
        color='darkred',
        fill=True,
        fillColor='red',
        fillOpacity=0.7,
        weight=2
    ).add_to(m_web)

# Título
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 600px; height: 80px; 
            background-color: white; border: 2px solid grey;
            z-index: 9999; font-size: 16px; padding: 10px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
            border-radius: 5px;">
    <h4 style="margin: 0; color: #333;">🔥 Mapa de Calor - TOP 50 Municípios</h4>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
        Potencial para drones agrícolas em Santa Catarina<br>
        <span style="color: red;">● Marcadores vermelhos = TOP 5 municípios</span>
    </p>
</div>
'''
m_web.get_root().html.add_child(folium.Element(title_html))

# Footer
footer_html = '''
<div style="position: fixed; 
            bottom: 10px; right: 10px; width: 300px; height: auto; 
            background-color: rgba(255,255,255,0.9); border: 1px solid grey;
            z-index: 9999; font-size: 10px; padding: 8px;
            border-radius: 5px;">
    <strong>Autor:</strong> Ronan Armando Caetano (UFSC/IFSC)<br>
    <strong>Dados:</strong> IBGE/SIDRA - PAM 2024<br>
    <strong>Versão:</strong> Web Otimizada (TOP 50)
</div>
'''
m_web.get_root().html.add_child(folium.Element(footer_html))

web_path = output_dir / "heatmap_top50_WEB.html"
m_web.save(str(web_path))
print(f"✓ heatmap_top50_WEB.html")

# [6] Resumo
print("\n" + "=" * 60)
print("✅ MAPAS DE CALOR GERADOS COM SUCESSO!")
print("=" * 60)
print("\n📂 Arquivos salvos em:", output_dir)
print("\n🔥 Mapas Individuais:")
for config in heatmap_configs.values():
    print(f"   • {config['file']}")
print("\n🔥 Mapas Especiais:")
print("   • heatmap_combinado.html (todas as camadas em um só mapa)")
print("   • heatmap_top50_WEB.html (versão otimizada com TOP 50)")
print("\n💡 Dica: Abra o 'heatmap_combinado.html' para visualizar todos os indicadores!")
print("=" * 60)
