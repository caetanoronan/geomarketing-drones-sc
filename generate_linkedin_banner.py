"""
Gera banner otimizado para LinkedIn (1200x627px)
Banner profissional para divulgação do projeto de Geomarketing de Drones Agrícolas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# Configurar figura com dimensões LinkedIn (1200x627px, 96 DPI)
fig = plt.figure(figsize=(12.5, 6.53), dpi=96, facecolor='white')
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# FUNDO COM GRADIENTE
from matplotlib.patches import Rectangle
gradient = np.linspace(0, 1, 256).reshape(1, -1)
gradient = np.vstack((gradient, gradient))

# Gradiente azul profissional
ax.imshow(gradient, extent=[0, 100, 0, 100], aspect='auto', 
          cmap='Blues', alpha=0.15, origin='lower')

# RETÂNGULO DE FUNDO COM BORDA
background = FancyBboxPatch((2, 2), 96, 96, 
                           boxstyle="round,pad=1", 
                           edgecolor='#2C5F8D', 
                           facecolor='white', 
                           linewidth=3,
                           alpha=0.95)
ax.add_patch(background)

# TÍTULO PRINCIPAL
ax.text(50, 88, '🚁 GEOMARKETING', 
        fontsize=32, weight='bold', 
        ha='center', va='top',
        color='#1a365d',
        family='sans-serif')

ax.text(50, 80, 'Drones Agrícolas em Santa Catarina', 
        fontsize=18, weight='normal',
        ha='center', va='top',
        color='#2d3748',
        family='sans-serif')

# LINHA SEPARADORA
ax.plot([15, 85], [75, 75], color='#4299e1', linewidth=2, alpha=0.6)

# MÉTRICAS PRINCIPAIS (3 colunas)
metrics = [
    {'icon': '📊', 'value': '295', 'label': 'Municípios\nAnalisados'},
    {'icon': '🌾', 'value': '1,68M ha', 'label': 'Área\nAgrícola'},
    {'icon': '💰', 'value': 'R$ 4,2M', 'label': 'VPL\nProjetado'}
]

x_positions = [25, 50, 75]
for i, (x, metric) in enumerate(zip(x_positions, metrics)):
    # Círculo de fundo
    circle = Circle((x, 55), 8, color='#ebf8ff', ec='#4299e1', linewidth=2)
    ax.add_patch(circle)
    
    # Ícone
    ax.text(x, 58, metric['icon'], fontsize=28, ha='center', va='center')
    
    # Valor
    ax.text(x, 43, metric['value'], 
            fontsize=18, weight='bold', ha='center', va='top',
            color='#1a365d')
    
    # Label
    ax.text(x, 38, metric['label'], 
            fontsize=10, ha='center', va='top',
            color='#4a5568',
            linespacing=1.3)

# DESTAQUE: COLD SPOTS STRATEGY
strategy_box = FancyBboxPatch((10, 15), 80, 15,
                              boxstyle="round,pad=0.5",
                              facecolor='#2C5F8D',
                              edgecolor='#1a365d',
                              linewidth=2)
ax.add_patch(strategy_box)

ax.text(50, 25, '🧊 ESTRATÉGIA COLD SPOTS', 
        fontsize=14, weight='bold', ha='center', va='center',
        color='white')

ax.text(50, 20, 'Curitibanos → Chapecó → Mafra  •  700 mil ha  •  Custo 40% menor', 
        fontsize=10, ha='center', va='center',
        color='#e0f2fe',
        style='italic')

# FOOTER COM DADOS REAIS
ax.text(10, 8, '✅ Dados Reais IBGE PAM 2024 + Censo Agro 2017', 
        fontsize=9, ha='left', va='center',
        color='#2d3748',
        weight='normal')

ax.text(90, 8, 'TIR 180% • Payback 14m', 
        fontsize=9, ha='right', va='center',
        color='#22543d',
        weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#c6f6d5', 
                  edgecolor='#48bb78', linewidth=1.5))

# AUTOR
ax.text(50, 3, 'Ronan Armando Caetano  •  IFSC Geoprocessamento + UFSC Ciências Biológicas', 
        fontsize=8, ha='center', va='center',
        color='#718096',
        style='italic')

# Salvar em alta qualidade
plt.tight_layout(pad=0)
plt.savefig('data/outputs/linkedin_banner_drones_agro.png', 
            dpi=96, bbox_inches='tight', pad_inches=0.1,
            facecolor='white', edgecolor='none')

print("✅ Banner LinkedIn criado: data/outputs/linkedin_banner_drones_agro.png")
print("📐 Dimensões: 1200x627px (otimizado para LinkedIn)")
print("🎨 Formato: PNG de alta qualidade")
print("\n📤 Próximos passos:")
print("1. Abra o arquivo gerado")
print("2. No LinkedIn, clique em 'Adicionar mídia' ao criar o post")
print("3. Faça upload do banner PNG")
print("4. Ajuste o enquadramento se necessário")

# Fechar a figura sem mostrar (evita travamento)
plt.close()
