"""
Script para gerar mapa de Cold Spots estratégicos para base operacional de drones agrícolas
Autor: Ronan Armando Caetano
Data: 05/11/2025
"""

import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

print("🗺️ Gerando Mapa de Cold Spots Estratégicos...")

# Carregar dados
print("\n📂 Carregando dados...")
gdf_sc = gpd.read_file('data/SC_Municipios_2024/SC_Municipios_2024.shp')
df_ranking = pd.read_csv('data/outputs/ranking_municipal_drones_agro_REAL.csv')

# Limpar nome do município
df_ranking['nome_municipio_clean'] = df_ranking['nome_municipio'].str.replace(' (SC)', '', regex=False)

# Merge para ter ranking nos municípios
gdf_merged = gdf_sc.merge(
    df_ranking[['nome_municipio_clean', 'score_composto', 'area_total_ha', 'ranking']],
    left_on='NM_MUN',
    right_on='nome_municipio_clean',
    how='left'
)

# Simplificar geometria para web
print("🔧 Simplificando geometria para web...")
gdf_merged['geometry'] = gdf_merged['geometry'].simplify(tolerance=0.01)

# Definir Cold Spots estratégicos
cold_spots = [
    {
        'nome': 'Curitibanos',
        'score_operacional': 95,
        'classificacao': 'Warm Spot (#4)',
        'lat': -27.283,
        'lon': -50.583,
        'area_cobertura': 240712,  # ha
        'municipios_atendidos': 5,
        'opex_mensal': 25000,
        'vantagens': [
            'UFSC Campus',
            '25 km de Campos Novos',
            'BR-116 + BR-282',
            'Custo 35% menor'
        ],
        'raio_km': 60,
        'cor': '#2ecc71',
        'prioridade': '🥇 PRINCIPAL'
    },
    {
        'nome': 'Caçador',
        'score_operacional': 90,
        'classificacao': 'Cold Spot',
        'lat': -26.775,
        'lon': -51.015,
        'area_cobertura': 380000,
        'municipios_atendidos': 8,
        'opex_mensal': 30000,
        'vantagens': [
            'Maior cidade Planalto (78k hab)',
            'Aeródromo',
            'BR-470 + BR-153',
            'Ponte Oeste-Serrano'
        ],
        'raio_km': 100,
        'cor': '#3498db',
        'prioridade': '🥈 SECUNDÁRIA'
    },
    {
        'nome': 'Mafra',
        'score_operacional': 85,
        'classificacao': 'Warm Spot (#3)',
        'lat': -26.117,
        'lon': -49.817,
        'area_cobertura': 180000,
        'municipios_atendidos': 4,
        'opex_mensal': 28000,
        'vantagens': [
            'Fronteira PR-SC',
            'BR-116',
            'Mercado duplo',
            'Polo madeireiro'
        ],
        'raio_km': 60,
        'cor': '#9b59b6',
        'prioridade': '🥉 TERCIÁRIA'
    },
    {
        'nome': 'Chapecó',
        'score_operacional': 88,
        'classificacao': 'Cold Spot',
        'lat': -27.097,
        'lon': -52.617,
        'area_cobertura': 280000,
        'municipios_atendidos': 6,
        'opex_mensal': 35000,
        'vantagens': [
            'Capital Oeste (224k hab)',
            'Aeroporto regional',
            'Sede cooperativas',
            'UFFS + Unochapecó'
        ],
        'raio_km': 100,
        'cor': '#e67e22',
        'prioridade': 'FASE 2'
    },
    {
        'nome': 'Lages',
        'score_operacional': 70,
        'classificacao': 'Cold Spot',
        'lat': -27.816,
        'lon': -50.325,
        'area_cobertura': 120000,
        'municipios_atendidos': 2,
        'opex_mensal': 22000,
        'vantagens': [
            'Maior cidade Planalto (158k)',
            'Aeroporto',
            'UDESC Campus',
            'Custo baixo'
        ],
        'raio_km': 80,
        'cor': '#95a5a6',
        'prioridade': 'OPCIONAL'
    }
]

# Hot Spots TOP 5 para referência
hot_spots_top5 = [
    {'nome': 'Campos Novos', 'lat': -27.400, 'lon': -51.217, 'score': 69.1, 'area': 90879, 'ranking': 1},
    {'nome': 'Abelardo Luz', 'lat': -26.567, 'lon': -52.333, 'score': 49.2, 'area': 69423, 'ranking': 2},
    {'nome': 'Mafra', 'lat': -26.117, 'lon': -49.817, 'score': 48.2, 'area': 52163, 'ranking': 3},
    {'nome': 'Curitibanos', 'lat': -27.283, 'lon': -50.583, 'score': 47.8, 'area': 47062, 'ranking': 4},
    {'nome': 'Ponte Alta', 'lat': -27.483, 'lon': -50.383, 'score': 46.1, 'area': 39756, 'ranking': 5}
]

# ========================================
# MAPA 1: MAPA INTERATIVO COLD SPOTS
# ========================================
print("\n🗺️ Criando mapa interativo de Cold Spots...")

# Criar mapa base
m = folium.Map(
    location=[-27.2, -50.8],
    zoom_start=7,
    tiles='CartoDB positron',
    min_zoom=6,
    max_zoom=13
)

# Adicionar TÍTULO ao mapa
title_html = '''
<div style="position: fixed; 
     top: 10px; left: 50%; transform: translateX(-50%);
     width: 700px; height: 90px;
     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
     z-index: 9999; 
     padding: 15px;
     border-radius: 15px;
     box-shadow: 0 4px 15px rgba(0,0,0,0.3);
     border: 3px solid white;">
    <h2 style="color: white; margin: 0; text-align: center; font-family: Arial, sans-serif; font-size: 24px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        🧊 MAPA DE COLD SPOTS ESTRATÉGICOS
    </h2>
    <p style="color: white; margin: 8px 0 0 0; text-align: center; font-family: Arial, sans-serif; font-size: 14px; opacity: 0.95;">
        Localização ideal para bases operacionais de drones agrícolas em Santa Catarina
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Adicionar limites MUNICIPAIS de SC
print("🗺️ Adicionando limites municipais...")
folium.GeoJson(
    gdf_merged,
    style_function=lambda x: {
        'fillColor': '#f8f9fa' if x['properties'].get('ranking') is None else '#e8f5e9',
        'color': '#90a4ae',
        'weight': 0.8,
        'fillOpacity': 0.4
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', 'ranking', 'score_composto'],
        aliases=['Município:', 'Ranking:', 'Score:'],
        localize=True
    ),
    name='Limites Municipais'
).add_to(m)

# Adicionar limite ESTADUAL de SC (contorno destacado)
print("🗺️ Adicionando limite estadual...")
gdf_sc_union = gdf_sc.dissolve()  # Unir todos os municípios = contorno do estado
folium.GeoJson(
    gdf_sc_union,
    style_function=lambda x: {
        'fillColor': 'none',
        'color': '#1a237e',
        'weight': 4,
        'fillOpacity': 0
    },
    name='Limite Estadual SC'
).add_to(m)

# Camada de Hot Spots (TOP 5)
hot_spots_layer = folium.FeatureGroup(name='🔥 Hot Spots (TOP 5)', show=True)

for hs in hot_spots_top5:
    folium.CircleMarker(
        location=[hs['lat'], hs['lon']],
        radius=15 + (hs['score'] / 10),
        popup=folium.Popup(f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="color: #e74c3c; margin: 0;">🔥 {hs['nome']}</h4>
                <hr style="margin: 5px 0;">
                <p style="margin: 5px 0;"><b>Ranking:</b> #{hs['ranking']}</p>
                <p style="margin: 5px 0;"><b>Score:</b> {hs['score']}</p>
                <p style="margin: 5px 0;"><b>Área Agrícola:</b> {hs['area']:,.0f} ha</p>
                <p style="margin: 8px 0; padding: 8px; background: #ffe6e6; border-left: 3px solid #e74c3c;">
                    <b>Mercado prioritário</b> para serviços de drones agrícolas
                </p>
            </div>
        """, max_width=300),
        tooltip=f"#{hs['ranking']} {hs['nome']} - {hs['score']} pts",
        color='#e74c3c',
        fill=True,
        fillColor='#ff6b6b',
        fillOpacity=0.7,
        weight=3
    ).add_to(hot_spots_layer)

hot_spots_layer.add_to(m)

# Camada de Cold Spots com raios de cobertura
cold_spots_layer = folium.FeatureGroup(name='🧊 Cold Spots Estratégicos', show=True)

for cs in cold_spots:
    # Raio de cobertura
    folium.Circle(
        location=[cs['lat'], cs['lon']],
        radius=cs['raio_km'] * 1000,  # converter km para metros
        popup=f"Raio de cobertura: {cs['raio_km']} km",
        color=cs['cor'],
        fill=True,
        fillColor=cs['cor'],
        fillOpacity=0.1,
        weight=2,
        dashArray='5, 5'
    ).add_to(cold_spots_layer)
    
    # Marcador do Cold Spot
    vantagens_html = ''.join([f'<li style="margin: 3px 0;">{v}</li>' for v in cs['vantagens']])
    
    folium.Marker(
        location=[cs['lat'], cs['lon']],
        popup=folium.Popup(f"""
            <div style="font-family: Arial; width: 300px;">
                <h3 style="color: {cs['cor']}; margin: 0; padding: 10px; background: {cs['cor']}20; border-radius: 5px;">
                    🧊 {cs['nome']}
                </h3>
                <p style="margin: 8px 0; font-size: 0.9em; color: #666;"><b>{cs['classificacao']}</b></p>
                
                <table style="width: 100%; font-size: 0.85em; margin: 10px 0;">
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 5px;"><b>Score Operacional:</b></td>
                        <td style="padding: 5px; text-align: right;"><b style="color: {cs['cor']};">{cs['score_operacional']}/100</b></td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Prioridade:</b></td>
                        <td style="padding: 5px; text-align: right;">{cs['prioridade']}</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 5px;"><b>Área Atendível:</b></td>
                        <td style="padding: 5px; text-align: right;">{cs['area_cobertura']:,.0f} ha</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Municípios TOP 15:</b></td>
                        <td style="padding: 5px; text-align: right;">{cs['municipios_atendidos']}</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 5px;"><b>Raio Cobertura:</b></td>
                        <td style="padding: 5px; text-align: right;">{cs['raio_km']} km</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>OPEX Mensal:</b></td>
                        <td style="padding: 5px; text-align: right;">R$ {cs['opex_mensal']:,.0f}</td>
                    </tr>
                </table>
                
                <div style="margin: 10px 0; padding: 10px; background: {cs['cor']}15; border-left: 3px solid {cs['cor']};">
                    <p style="margin: 0 0 5px 0; font-weight: bold; color: {cs['cor']};">✅ Vantagens Competitivas:</p>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        {vantagens_html}
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 10px; padding: 8px; background: linear-gradient(135deg, {cs['cor']}40, {cs['cor']}20); border-radius: 5px;">
                    <b style="color: {cs['cor']};">BASE OPERACIONAL ESTRATÉGICA</b>
                </div>
            </div>
        """, max_width=350),
        tooltip=f"{cs['prioridade']} {cs['nome']} - Score: {cs['score_operacional']}",
        icon=folium.Icon(color='blue', icon='home', prefix='fa')
    ).add_to(cold_spots_layer)

cold_spots_layer.add_to(m)

# Linhas conectando Cold Spots aos Hot Spots dentro do raio
connections_layer = folium.FeatureGroup(name='🔗 Conexões Estratégicas', show=False)

for cs in cold_spots:
    cs_location = [cs['lat'], cs['lon']]
    for hs in hot_spots_top5:
        hs_location = [hs['lat'], hs['lon']]
        # Calcular distância aproximada
        dist_km = ((cs['lat'] - hs['lat'])**2 + (cs['lon'] - hs['lon'])**2)**0.5 * 111  # aprox km
        
        if dist_km <= cs['raio_km']:
            folium.PolyLine(
                locations=[cs_location, hs_location],
                color=cs['cor'],
                weight=2,
                opacity=0.4,
                dash_array='5, 10',
                popup=f"{cs['nome']} → {hs['nome']}: ~{dist_km:.0f} km"
            ).add_to(connections_layer)

connections_layer.add_to(m)

# Adicionar controle de camadas
folium.LayerControl(position='topright', collapsed=False).add_to(m)

# Adicionar legenda ATUALIZADA
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 300px; background: white; 
     border: 3px solid #667eea; z-index: 9999; padding: 15px; border-radius: 10px; 
     box-shadow: 0 4px 10px rgba(0,0,0,0.2); font-family: Arial;">
    <h4 style="margin: 0 0 12px 0; color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 8px;">📍 Legenda</h4>
    
    <div style="margin: 8px 0;">
        <span style="border: 3px solid #1a237e; width: 20px; height: 3px; 
                     display: inline-block; margin-right: 8px;"></span>
        <b style="color: #1a237e;">Limite Estadual SC</b>
    </div>
    
    <div style="margin: 8px 0;">
        <span style="border: 1px solid #90a4ae; background: #f8f9fa; width: 20px; height: 15px; 
                     display: inline-block; margin-right: 8px;"></span>
        <b style="color: #546e7a;">Limites Municipais</b>
    </div>
    
    <div style="margin: 8px 0;">
        <span style="background: #ff6b6b; width: 20px; height: 20px; border-radius: 50%; 
                     display: inline-block; margin-right: 8px; border: 2px solid #e74c3c;"></span>
        <b style="color: #e74c3c;">🔥 Hot Spots</b> - TOP 5 municípios (alta atividade agrícola)
    </div>
    
    <div style="margin: 8px 0;">
        <span style="background: #3498db; width: 20px; height: 20px; border-radius: 5px; 
                     display: inline-block; margin-right: 8px; border: 2px solid #2980b9;"></span>
        <b style="color: #3498db;">🧊 Cold Spots</b> - Bases operacionais estratégicas
    </div>
    
    <div style="margin: 8px 0;">
        <span style="border: 2px dashed #3498db; width: 25px; height: 2px; 
                     display: inline-block; margin-right: 8px;"></span>
        Raio de cobertura (60-100 km)
    </div>
    
    <div style="margin: 8px 0;">
        <span style="border: 1px dotted #95a5a6; width: 25px; height: 2px; 
                     display: inline-block; margin-right: 8px;"></span>
        Conexões estratégicas
    </div>
    
    <hr style="margin: 10px 0; border: 1px solid #ecf0f1;">
    
    <div style="background: #ecf8ff; padding: 10px; border-radius: 5px; border-left: 3px solid #3498db;">
        <p style="margin: 0; font-size: 0.85em; color: #2c3e50; line-height: 1.5;">
            <b>💡 Estratégia:</b> Localizar base em <b>Cold Spot</b> para atender múltiplos <b>Hot Spots</b> 
            com custo operacional <b>30-50% menor</b>.
        </p>
    </div>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Salvar mapa
output_map = 'data/outputs/maps/mapa_cold_spots_estrategicos.html'
m.save(output_map)
print(f"✅ Mapa salvo: {output_map}")

# ========================================
# INFOGRÁFICO: COMPARATIVO COLD SPOTS
# ========================================
print("\n📊 Gerando infográfico comparativo...")

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('🧊 ANÁLISE DE COLD SPOTS ESTRATÉGICOS - BASES OPERACIONAIS\nDrones Agrícolas em Santa Catarina', 
             fontsize=20, fontweight='bold', y=0.98)

# Subplot 1: Score Operacional
ax1 = axes[0, 0]
cold_spots_sorted = sorted(cold_spots, key=lambda x: x['score_operacional'], reverse=True)
nomes = [cs['nome'] for cs in cold_spots_sorted]
scores = [cs['score_operacional'] for cs in cold_spots_sorted]
cores = [cs['cor'] for cs in cold_spots_sorted]

bars1 = ax1.barh(nomes, scores, color=cores, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Score Operacional (0-100)', fontsize=12, fontweight='bold')
ax1.set_title('📈 Score Operacional (Custo x Cobertura x Infraestrutura)', fontsize=14, fontweight='bold')
ax1.set_xlim(0, 100)
ax1.grid(axis='x', alpha=0.3, linestyle='--')

# Adicionar valores
for i, (bar, score, cs) in enumerate(zip(bars1, scores, cold_spots_sorted)):
    ax1.text(score + 2, i, f'{score}', va='center', fontsize=11, fontweight='bold')
    ax1.text(5, i, cs['prioridade'], va='center', fontsize=9, color='white', fontweight='bold')

# Subplot 2: Área de Cobertura
ax2 = axes[0, 1]
areas = [cs['area_cobertura'] / 1000 for cs in cold_spots_sorted]  # converter para mil ha
bars2 = ax2.barh(nomes, areas, color=cores, edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Área Atendível (mil hectares)', fontsize=12, fontweight='bold')
ax2.set_title('🌾 Potencial de Mercado (Área Agrícola Atendível)', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3, linestyle='--')

for i, (bar, area, cs) in enumerate(zip(bars2, areas, cold_spots_sorted)):
    ax2.text(area + 10, i, f'{area:.0f}k ha', va='center', fontsize=11, fontweight='bold')
    ax2.text(10, i, f'{cs["municipios_atendidos"]} municípios', va='center', fontsize=9, color='white', fontweight='bold')

# Subplot 3: OPEX Mensal
ax3 = axes[1, 0]
opex = [cs['opex_mensal'] / 1000 for cs in cold_spots_sorted]  # converter para mil reais
bars3 = ax3.barh(nomes, opex, color=cores, edgecolor='black', linewidth=1.5)
ax3.set_xlabel('OPEX Mensal (R$ mil)', fontsize=12, fontweight='bold')
ax3.set_title('💰 Custo Operacional (Menor = Melhor)', fontsize=14, fontweight='bold')
ax3.grid(axis='x', alpha=0.3, linestyle='--')

for i, (bar, cost, cs) in enumerate(zip(bars3, opex, cold_spots_sorted)):
    ax3.text(cost + 1, i, f'R$ {cost:.0f}k', va='center', fontsize=11, fontweight='bold')
    # Calcular custo/área
    custo_ha = (cs['opex_mensal'] / cs['area_cobertura']) if cs['area_cobertura'] > 0 else 0
    ax3.text(2, i, f'R$ {custo_ha:.2f}/ha', va='center', fontsize=9, color='white', fontweight='bold')

# Subplot 4: Matriz Score x Área (Scatter com bolhas)
ax4 = axes[1, 1]
scores_x = [cs['score_operacional'] for cs in cold_spots]
areas_y = [cs['area_cobertura'] / 1000 for cs in cold_spots]
municipios_size = [cs['municipios_atendidos'] * 100 for cs in cold_spots]

for cs, score, area, size in zip(cold_spots, scores_x, areas_y, municipios_size):
    ax4.scatter(score, area, s=size * 15, color=cs['cor'], alpha=0.6, edgecolor='black', linewidth=2)
    ax4.annotate(cs['nome'], (score, area), fontsize=10, fontweight='bold', 
                ha='center', va='bottom', xytext=(0, 10), textcoords='offset points')

ax4.set_xlabel('Score Operacional', fontsize=12, fontweight='bold')
ax4.set_ylabel('Área Atendível (mil ha)', fontsize=12, fontweight='bold')
ax4.set_title('🎯 Matriz Estratégica (tamanho = municípios atendidos)', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, linestyle='--')

# Adicionar quadrantes
ax4.axvline(x=85, color='red', linestyle='--', alpha=0.5)
ax4.axhline(y=250, color='red', linestyle='--', alpha=0.5)
ax4.text(95, 360, 'IDEAL\n(alto score,\nalto mercado)', ha='center', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout()
output_infographic = 'data/outputs/maps/infografico_cold_spots.png'
plt.savefig(output_infographic, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Infográfico salvo: {output_infographic}")
plt.close()

# ========================================
# INFOGRÁFICO 2: ESTRATÉGIA 3 FASES
# ========================================
print("\n📊 Gerando infográfico da estratégia de expansão...")

fig, ax = plt.subplots(figsize=(18, 10), facecolor='white')

# Título
fig.text(0.5, 0.96, '🚀 ESTRATÉGIA DE EXPANSÃO - 3 FASES (36 MESES)', 
         ha='center', fontsize=22, fontweight='bold')
fig.text(0.5, 0.92, 'Plano de abertura de bases operacionais para dominar 42% do mercado de SC (700k ha)', 
         ha='center', fontsize=14, color='#666')

# Fase 1
fase1_box = FancyBboxPatch((0.05, 0.60), 0.25, 0.22, boxstyle="round,pad=0.02", 
                           edgecolor='#2ecc71', facecolor='#d5f4e6', linewidth=3)
ax.add_patch(fase1_box)
ax.text(0.175, 0.78, '🥇 FASE 1: PLANALTO SERRANO', ha='center', fontsize=16, fontweight='bold', color='#27ae60')
ax.text(0.175, 0.74, 'Meses 0-12', ha='center', fontsize=12, color='#666', style='italic')
ax.text(0.08, 0.70, '📍 Base: CURITIBANOS', fontsize=11, fontweight='bold')
ax.text(0.08, 0.67, '🎯 Target: Campos Novos (#1)', fontsize=10)
ax.text(0.08, 0.64, '🌾 Área: 240k ha (5 municípios)', fontsize=10)
ax.text(0.08, 0.61, '💰 Receita Ano 1: R$ 2,15M', fontsize=10, fontweight='bold', color='#27ae60')

# Fase 2
fase2_box = FancyBboxPatch((0.375, 0.60), 0.25, 0.22, boxstyle="round,pad=0.02", 
                           edgecolor='#e67e22', facecolor='#fdebd0', linewidth=3)
ax.add_patch(fase2_box)
ax.text(0.5, 0.78, '🥈 FASE 2: OESTE', ha='center', fontsize=16, fontweight='bold', color='#d35400')
ax.text(0.5, 0.74, 'Meses 12-24', ha='center', fontsize=12, color='#666', style='italic')
ax.text(0.405, 0.70, '📍 Base: CHAPECÓ', fontsize=11, fontweight='bold')
ax.text(0.405, 0.67, '🎯 Target: Abelardo Luz (#2) + cluster', fontsize=10)
ax.text(0.405, 0.64, '🌾 Área: 280k ha (6 municípios)', fontsize=10)
ax.text(0.405, 0.61, '💰 Receita Ano 2: R$ 5,60M', fontsize=10, fontweight='bold', color='#d35400')

# Fase 3
fase3_box = FancyBboxPatch((0.70, 0.60), 0.25, 0.22, boxstyle="round,pad=0.02", 
                           edgecolor='#9b59b6', facecolor='#ebdef0', linewidth=3)
ax.add_patch(fase3_box)
ax.text(0.825, 0.78, '🥉 FASE 3: NORTE + PR', ha='center', fontsize=16, fontweight='bold', color='#8e44ad')
ax.text(0.825, 0.74, 'Meses 24-36', ha='center', fontsize=12, color='#666', style='italic')
ax.text(0.73, 0.70, '📍 Base: MAFRA', fontsize=11, fontweight='bold')
ax.text(0.73, 0.67, '🎯 Target: Porto União + Paraná', fontsize=10)
ax.text(0.73, 0.64, '🌾 Área: 280k ha (mercado duplo)', fontsize=10)
ax.text(0.73, 0.61, '💰 Receita Ano 3: R$ 10,44M', fontsize=10, fontweight='bold', color='#8e44ad')

# Setas de progressão
ax.annotate('', xy=(0.36, 0.71), xytext=(0.31, 0.71), 
            arrowprops=dict(arrowstyle='->', lw=3, color='#34495e'))
ax.annotate('', xy=(0.685, 0.71), xytext=(0.635, 0.71), 
            arrowprops=dict(arrowstyle='->', lw=3, color='#34495e'))

# Métricas consolidadas
metrics_box = FancyBboxPatch((0.05, 0.35), 0.9, 0.20, boxstyle="round,pad=0.02", 
                             edgecolor='#3498db', facecolor='#ebf5fb', linewidth=3)
ax.add_patch(metrics_box)
ax.text(0.5, 0.52, '📊 RESULTADOS CONSOLIDADOS (36 MESES)', ha='center', fontsize=16, fontweight='bold', color='#2c3e50')

# Métricas em colunas
col1_x = 0.15
col2_x = 0.4
col3_x = 0.65
col4_x = 0.85
row_y = 0.46

ax.text(col1_x, row_y, '🏢 BASES', ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(col1_x, row_y - 0.04, '3', ha='center', fontsize=20, fontweight='bold', color='#3498db')
ax.text(col1_x, row_y - 0.08, 'Curitibanos\nChapecó\nMafra', ha='center', fontsize=9)

ax.text(col2_x, row_y, '🌾 ÁREA TOTAL', ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(col2_x, row_y - 0.04, '700k ha', ha='center', fontsize=20, fontweight='bold', color='#27ae60')
ax.text(col2_x, row_y - 0.08, '42% mercado SC\n(de 1,68M ha)', ha='center', fontsize=9)

ax.text(col3_x, row_y, '💰 RECEITA ANO 3', ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(col3_x, row_y - 0.04, 'R$ 10,44M', ha='center', fontsize=20, fontweight='bold', color='#e67e22')
ax.text(col3_x, row_y - 0.08, 'Margem: 58,4%\nLucro: R$ 6,10M', ha='center', fontsize=9)

ax.text(col4_x, row_y, '📈 TIR', ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(col4_x, row_y - 0.04, '180%', ha='center', fontsize=20, fontweight='bold', color='#c0392b')
ax.text(col4_x, row_y - 0.08, 'Payback:\n14 meses', ha='center', fontsize=9)

# Timeline visual
timeline_y = 0.25
ax.plot([0.05, 0.95], [timeline_y, timeline_y], 'k-', linewidth=2)

# Marcos de tempo
for month, x_pos, label in [(0, 0.05, 'Mês 0\nINÍCIO'), 
                             (12, 0.375, 'Mês 12\nFASE 2'), 
                             (24, 0.70, 'Mês 24\nFASE 3'),
                             (36, 0.95, 'Mês 36\nCONSOLIDADO')]:
    ax.plot(x_pos, timeline_y, 'o', markersize=15, color='#34495e')
    ax.text(x_pos, timeline_y - 0.05, label, ha='center', fontsize=9, fontweight='bold')

# Vantagens da estratégia
advantages_box = FancyBboxPatch((0.05, 0.05), 0.9, 0.12, boxstyle="round,pad=0.02", 
                                edgecolor='#16a085', facecolor='#d1f2eb', linewidth=2)
ax.add_patch(advantages_box)
ax.text(0.5, 0.145, '✅ VANTAGENS DA ESTRATÉGIA COLD SPOTS', ha='center', fontsize=14, fontweight='bold', color='#0e6655')

advantages = [
    '💰 Custo 30-50% menor vs. hot spots',
    '🎯 Atende múltiplos municípios',
    '🛡️ Resiliência (diversificação geográfica)',
    '🧑‍🎓 Acesso a universidades (UFSC, UFFS)',
    '🚀 Infraestrutura superior (aeroportos, rodovias)'
]

x_start = 0.10
x_step = 0.18
for i, adv in enumerate(advantages):
    ax.text(x_start + (i * x_step), 0.09, adv, fontsize=9, va='center')

# Remover eixos
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

output_strategy = 'data/outputs/maps/infografico_estrategia_3_fases.png'
plt.savefig(output_strategy, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Infográfico estratégia salvo: {output_strategy}")
plt.close()

print("\n🎉 CONCLUÍDO!")
print(f"\n📁 Arquivos gerados:")
print(f"   1. {output_map}")
print(f"   2. {output_infographic}")
print(f"   3. {output_strategy}")
print("\n✨ Visualizações prontas para apresentação!")
