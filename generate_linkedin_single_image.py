"""
Gera imagem única condensada do carrossel (1200x1500px)
Versão alternativa quando o carrossel não funciona no LinkedIn
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

# Figura vertical longa (melhor para LinkedIn feed)
fig = plt.figure(figsize=(12, 15), dpi=100, facecolor='white')
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Gradiente de fundo
gradient = np.linspace(0, 1, 256).reshape(1, -1)
gradient = np.vstack((gradient, gradient))
ax.imshow(gradient, extent=[0, 100, 0, 100], aspect='auto', 
          cmap='Blues', alpha=0.08, origin='lower')

# ============================================
# HEADER
# ============================================
header = Rectangle((0, 94), 100, 6, facecolor='#2C5F8D', edgecolor='none')
ax.add_patch(header)

ax.text(50, 97, '🚁 ESTRATÉGIA COLD SPOTS', 
        fontsize=22, weight='bold', ha='center', va='center', color='white')

# ============================================
# SEÇÃO 1: VISÃO GERAL
# ============================================
ax.text(50, 90, 'Como cobrir 700 mil hectares com custo 40% menor', 
        fontsize=14, ha='center', va='center', color='#4a5568', style='italic')

# Mapa simplificado com 3 pontos
map_box = FancyBboxPatch((15, 68), 70, 18,
                         boxstyle="round,pad=1",
                         facecolor='#ebf8ff',
                         edgecolor='#2C5F8D',
                         linewidth=2)
ax.add_patch(map_box)

# 3 cidades
cities = [
    {'name': 'Curitibanos', 'x': 35, 'y': 77, 'color': '#48bb78'},
    {'name': 'Chapecó', 'x': 50, 'y': 75, 'color': '#4299e1'},
    {'name': 'Mafra', 'x': 65, 'y': 79, 'color': '#ed8936'}
]

for city in cities:
    point = Circle((city['x'], city['y']), 2, 
                   color=city['color'], edgecolor='white', linewidth=2)
    ax.add_patch(point)
    ax.text(city['x'], city['y'] - 4, city['name'], 
            fontsize=10, weight='bold', ha='center', color=city['color'])

# Métricas resumo
metrics_y = 70
ax.text(30, metrics_y, '700k ha', fontsize=14, weight='bold', color='#2C5F8D', ha='center')
ax.text(30, metrics_y-2, 'Cobertura', fontsize=8, color='#4a5568', ha='center')

ax.text(50, metrics_y, '42%', fontsize=14, weight='bold', color='#2C5F8D', ha='center')
ax.text(50, metrics_y-2, 'do Estado', fontsize=8, color='#4a5568', ha='center')

ax.text(70, metrics_y, '-40%', fontsize=14, weight='bold', color='#48bb78', ha='center')
ax.text(70, metrics_y-2, 'Custo OPEX', fontsize=8, color='#4a5568', ha='center')

# ============================================
# SEÇÃO 2: 3 BASES
# ============================================
bases = [
    {
        'name': 'CURITIBANOS', 'phase': 'Fase 1 (0-12m)', 'color': '#48bb78', 'bg': '#f0fff4',
        'metrics': [
            ('240k ha', 'Cobertura 60km'),
            ('4 cidades', 'Hot Spots'),
            ('-40%', 'Custo vs Hot'),
            ('UFSC', 'Campus + Talentos')
        ],
        'y': 63
    },
    {
        'name': 'CHAPECÓ', 'phase': 'Fase 2 (12-24m)', 'color': '#4299e1', 'bg': '#ebf8ff',
        'metrics': [
            ('280k ha', 'Cobertura Oeste'),
            ('Aurora', 'Cooperativa'),
            ('Copérdia', 'Parceria'),
            ('Milho', 'Cultura Principal')
        ],
        'y': 44
    },
    {
        'name': 'MAFRA', 'phase': 'Fase 3 (24-36m)', 'color': '#ed8936', 'bg': '#fffaf0',
        'metrics': [
            ('180k ha', 'Cobertura Norte'),
            ('Fronteira', 'Divisa PR'),
            ('+TAM', 'Expansão PR'),
            ('Madeira', 'Complementar')
        ],
        'y': 25
    }
]

for base in bases:
    # Card
    card = FancyBboxPatch((10, base['y']-15), 80, 16,
                          boxstyle="round,pad=1",
                          facecolor=base['bg'],
                          edgecolor=base['color'],
                          linewidth=3)
    ax.add_patch(card)
    
    # Nome
    ax.text(50, base['y']+0.5, base['name'], 
            fontsize=16, weight='bold', ha='center', color=base['color'])
    ax.text(50, base['y']-2, base['phase'], 
            fontsize=9, ha='center', color='#4a5568', style='italic')
    
    # 4 métricas em grid 2x2
    positions = [(25, base['y']-7), (75, base['y']-7), 
                 (25, base['y']-12), (75, base['y']-12)]
    
    for (x, y), (value, label) in zip(positions, base['metrics']):
        ax.text(x, y+1, value, 
                fontsize=11, weight='bold', ha='center', color=base['color'])
        ax.text(x, y-1, label, 
                fontsize=7, ha='center', color='#4a5568')

# ============================================
# SEÇÃO 3: VIABILIDADE FINANCEIRA
# ============================================
result_box = FancyBboxPatch((10, 6), 80, 8,
                           boxstyle="round,pad=1",
                           facecolor='#f0fff4',
                           edgecolor='#48bb78',
                           linewidth=3)
ax.add_patch(result_box)

ax.text(50, 12, '💰 VIABILIDADE FINANCEIRA', 
        fontsize=13, weight='bold', ha='center', color='#22543d')

financial = ['TIR: 180%', 'Payback: 14m', 'VPL: R$ 4,2M']
for i, metric in enumerate(financial):
    x = 23 + i * 27
    ax.text(x, 8.5, metric, fontsize=10, weight='bold',
           ha='center', color='#22543d')

# ============================================
# FOOTER / CTA
# ============================================
footer = Rectangle((0, 0), 100, 4, facecolor='#2C5F8D', edgecolor='none')
ax.add_patch(footer)

ax.text(50, 2.5, '🔗 Análise completa: Link nos comentários!', 
        fontsize=11, weight='bold', ha='center', color='white')
ax.text(50, 0.8, 'Ronan Caetano • IFSC Geoprocessamento + UFSC Ciências Biológicas', 
        fontsize=7, ha='center', color='#bee3f8')

plt.tight_layout(pad=0)
plt.savefig('data/outputs/linkedin_post_unico_cold_spots.png', 
            dpi=100, bbox_inches='tight', pad_inches=0.1,
            facecolor='white')
plt.close()

print("✅ Imagem única criada: data/outputs/linkedin_post_unico_cold_spots.png")
print("📐 Dimensões: 1200x1500px (formato vertical otimizado para LinkedIn feed)")
print("\n📤 Como usar:")
print("1. Criar post no LinkedIn")
print("2. Adicionar esta ÚNICA imagem")
print("3. Colar o texto da Versão 2")
print("4. Publicar! Muito mais simples que carrossel 🚀")
