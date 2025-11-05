"""Generate choropleth maps for agricultural drone market potential in SC.
Creates:
1. Static PNG maps (matplotlib) - score composto, área agrícola
2. Interactive HTML map (folium) - score composto with municipality tooltips
"""
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

DATA_DIR = 'data'
OUT_DIR = 'data/outputs/maps'
os.makedirs(OUT_DIR, exist_ok=True)

# Load ranking data
df_ranking = pd.read_csv(os.path.join(DATA_DIR, 'outputs', 'ranking_municipal_drones_agro.csv'))
print(f"Loaded ranking for {len(df_ranking)} municipalities\n")

# Load municipal polygons
gdf_muni = gpd.read_file(os.path.join(DATA_DIR, 'bc25_geojson', 'lml_municipio_a.geojson'))
print(f"Loaded {len(gdf_muni)} municipal polygons")
print(f"Columns: {list(gdf_muni.columns)[:10]}")

# Try to identify the municipality code column in the shapefile
# Common names: CD_GEOCMU, GEOCODIGO, CD_MUN, etc.
code_col_candidates = ['CD_GEOCMU', 'CD_MUN', 'GEOCODIGO', 'geocodigo', 'cd_geocmu']
code_col = None
for col in code_col_candidates:
    if col in gdf_muni.columns:
        code_col = col
        break

if not code_col:
    print(f"\nWARNING: Could not find municipality code column in shapefile. Available columns: {list(gdf_muni.columns)}")
    print("Will try first column that looks like a code...")
    # Fallback: use first column with numeric codes
    for col in gdf_muni.columns:
        if gdf_muni[col].dtype in ['int64', 'object'] and gdf_muni[col].astype(str).str.isdigit().sum() > len(gdf_muni) * 0.8:
            code_col = col
            break

print(f"\nUsing code column: {code_col}")

# Ensure both are string for merge
gdf_muni[code_col] = gdf_muni[code_col].astype(str)
df_ranking['cod_municipio'] = df_ranking['cod_municipio'].astype(str)

# Merge ranking data with geometries
gdf_merged = gdf_muni.merge(df_ranking, left_on=code_col, right_on='cod_municipio', how='left')
print(f"Merged GeoDataFrame has {len(gdf_merged)} rows, {gdf_merged['score_composto'].notna().sum()} with ranking data\n")

# 1) Choropleth: Score Composto
print("Creating choropleth map: Score Composto...")
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
gdf_merged.plot(
    column='score_composto',
    ax=ax,
    legend=True,
    cmap='YlOrRd',
    edgecolor='black',
    linewidth=0.3,
    missing_kwds={'color': 'lightgrey', 'label': 'Sem dados'},
    legend_kwds={'label': 'Score Composto (Potencial Drones Agro)', 'shrink': 0.6}
)
ax.set_title('Potencial de Mercado para Drones Agrícolas - Santa Catarina\n(Score Composto: Área + Culturas + Grandes Produtores + Infraestrutura)', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
map1_path = os.path.join(OUT_DIR, 'mapa_score_composto_drones_agro_sc.png')
plt.savefig(map1_path, dpi=300, bbox_inches='tight')
print(f"Saved: {map1_path}\n")
plt.close()

# 2) Choropleth: Área Agrícola Total
print("Creating choropleth map: Área Agrícola Total...")
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
gdf_merged.plot(
    column='area_total_ha',
    ax=ax,
    legend=True,
    cmap='Greens',
    edgecolor='black',
    linewidth=0.3,
    missing_kwds={'color': 'lightgrey'},
    legend_kwds={'label': 'Área Agrícola Total (ha)', 'shrink': 0.6}
)
ax.set_title('Área Agrícola Total por Município - Santa Catarina', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
map2_path = os.path.join(OUT_DIR, 'mapa_area_agricola_sc.png')
plt.savefig(map2_path, dpi=300, bbox_inches='tight')
print(f"Saved: {map2_path}\n")
plt.close()

# 3) Interactive HTML map with Folium
print("Creating interactive HTML map with Folium...")
try:
    import folium
    from folium import plugins
    
    # Reproject to WGS84 for Folium
    gdf_map = gdf_merged.to_crs(epsg=4326)
    
    # Create base map centered on SC
    m = folium.Map(location=[-27.5, -50.5], zoom_start=7, tiles='OpenStreetMap')
    
    # Add choropleth layer
    folium.Choropleth(
        geo_data=gdf_map,
        data=df_ranking,
        columns=['cod_municipio', 'score_composto'],
        key_on='feature.properties.' + code_col,
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name='Score Composto (Potencial Drones Agro)',
        nan_fill_color='lightgrey'
    ).add_to(m)
    
    # Add tooltips with municipality info
    style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity': 0.1, 'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.50, 'weight': 0.1}
    
    tooltip_fields = ['nome_municipio', 'ranking', 'score_composto', 'area_total_ha', 'estabelecimentos_grandes_100ha_plus']
    tooltip_aliases = ['Município:', 'Ranking:', 'Score:', 'Área Agrícola (ha):', 'Grandes Produtores:']
    
    tooltip = folium.features.GeoJsonTooltip(
        fields=tooltip_fields,
        aliases=tooltip_aliases,
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )
    
    folium.GeoJson(
        gdf_map,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=tooltip
    ).add_to(m)
    
    # Add title
    title_html = '''
             <div style="position: fixed; 
                         top: 10px; left: 50px; width: 500px; height: 80px; 
                         background-color:white; border:2px solid grey; z-index:9999; font-size:14px;
                         padding: 10px">
                         <b>Potencial de Mercado para Drones Agrícolas - SC</b><br>
                         Score Composto: Área Agrícola + Culturas-Alvo + Grandes Produtores + Infraestrutura B2B
                         </div>
             '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    map3_path = os.path.join(OUT_DIR, 'mapa_interativo_drones_agro_sc.html')
    m.save(map3_path)
    print(f"Saved: {map3_path}\n")
    
except ImportError:
    print("Folium not installed. Skipping interactive map. Install with: pip install folium\n")

print("="*60)
print("All maps generated successfully!")
print(f"Files saved to: {OUT_DIR}/")
print("="*60)
