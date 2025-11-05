"""
Gera carrossel de infográficos para LinkedIn (1080x1080px cada slide)
5 slides explicando a estratégia de Cold Spots para drones agrícolas em SC
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np

# Configurações globais
SLIDE_SIZE = (10.8, 10.8)  # 1080x1080px a 100 DPI
DPI = 100

def create_slide_base(title, subtitle="", slide_number=1, total_slides=5):
    """Cria base padrão para cada slide"""
    fig = plt.figure(figsize=SLIDE_SIZE, dpi=DPI, facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Gradiente de fundo sutil
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    ax.imshow(gradient, extent=[0, 100, 0, 100], aspect='auto', 
              cmap='Blues', alpha=0.08, origin='lower')
    
    # Barra superior com marca
    header = Rectangle((0, 92), 100, 8, facecolor='#2C5F8D', edgecolor='none')
    ax.add_patch(header)
    
    ax.text(5, 96, '🚁 GEOMARKETING DRONES AGRO SC', 
            fontsize=11, weight='bold', color='white', va='center')
    
    # Contador de slides
    ax.text(95, 96, f'{slide_number}/{total_slides}', 
            fontsize=10, weight='bold', color='white', va='center', ha='right')
    
    # Título do slide
    ax.text(50, 84, title, 
            fontsize=28, weight='bold', ha='center', va='center',
            color='#1a365d', wrap=True)
    
    if subtitle:
        ax.text(50, 78, subtitle, 
                fontsize=14, ha='center', va='center',
                color='#4a5568', style='italic')
    
    # Rodapé
    footer = Rectangle((0, 0), 100, 4, facecolor='#f7fafc', edgecolor='#e2e8f0', linewidth=1)
    ax.add_patch(footer)
    
    ax.text(50, 2, 'Ronan Caetano • IFSC Geoprocessamento + UFSC Ciências Biológicas', 
            fontsize=8, ha='center', va='center', color='#718096')
    
    return fig, ax


# ============================================
# SLIDE 1: CAPA
# ============================================
def create_slide_1():
    fig, ax = create_slide_base(
        "Estratégia Cold Spots",
        "Como cobrir 700 mil hectares com custo 40% menor",
        slide_number=1
    )
    
    # Mapa estilizado de SC com 3 pontos
    # Contorno SC simplificado
    sc_outline = FancyBboxPatch((20, 25), 60, 45,
                                boxstyle="round,pad=2",
                                edgecolor='#2C5F8D',
                                facecolor='#ebf8ff',
                                linewidth=3)
    ax.add_patch(sc_outline)
    
    # Pontos das 3 cidades
    cities = [
        {'name': 'Curitibanos', 'x': 50, 'y': 50, 'color': '#48bb78', 'phase': 'FASE 1'},
        {'name': 'Chapecó', 'x': 35, 'y': 45, 'color': '#4299e1', 'phase': 'FASE 2'},
        {'name': 'Mafra', 'x': 58, 'y': 60, 'color': '#ed8936', 'phase': 'FASE 3'}
    ]
    
    for city in cities:
        # Círculo de cobertura
        coverage = Circle((city['x'], city['y']), 8, 
                         color=city['color'], alpha=0.2, linewidth=0)
        ax.add_patch(coverage)
        
        # Ponto central
        point = Circle((city['x'], city['y']), 2.5, 
                      color=city['color'], edgecolor='white', linewidth=2)
        ax.add_patch(point)
        
        # Label
        ax.text(city['x'], city['y'] - 12, city['name'], 
                fontsize=11, weight='bold', ha='center',
                color=city['color'])
        ax.text(city['x'], city['y'] - 15, city['phase'], 
                fontsize=8, ha='center', color='#4a5568')
    
    # Métricas resumo
    metrics_box = FancyBboxPatch((15, 8), 70, 12,
                                 boxstyle="round,pad=1",
                                 facecolor='white',
                                 edgecolor='#e2e8f0',
                                 linewidth=2)
    ax.add_patch(metrics_box)
    
    ax.text(25, 16, '700k ha', fontsize=16, weight='bold', color='#2C5F8D', ha='center')
    ax.text(25, 11, 'Cobertura Total', fontsize=9, color='#4a5568', ha='center')
    
    ax.text(50, 16, '42%', fontsize=16, weight='bold', color='#2C5F8D', ha='center')
    ax.text(50, 11, 'do Estado', fontsize=9, color='#4a5568', ha='center')
    
    ax.text(75, 16, '-40%', fontsize=16, weight='bold', color='#48bb78', ha='center')
    ax.text(75, 11, 'Custo OPEX', fontsize=9, color='#4a5568', ha='center')
    
    plt.tight_layout(pad=0)
    plt.savefig('data/outputs/linkedin_carousel_slide_1.png', 
                dpi=DPI, bbox_inches='tight', pad_inches=0,
                facecolor='white')
    plt.close()
    print("✅ Slide 1 criado: Capa")


# ============================================
# SLIDE 2: CURITIBANOS
# ============================================
def create_slide_2():
    fig, ax = create_slide_base(
        "Base Principal",
        "Curitibanos • Fase 1 (0-12 meses)",
        slide_number=2
    )
    
    # Card principal
    card = FancyBboxPatch((10, 20), 80, 50,
                          boxstyle="round,pad=2",
                          facecolor='#f0fff4',
                          edgecolor='#48bb78',
                          linewidth=4)
    ax.add_patch(card)
    
    # Nome da cidade
    ax.text(50, 63, 'CURITIBANOS', 
            fontsize=26, weight='bold', ha='center',
            color='#22543d')
    
    # Métricas principais em grid 2x2
    metrics = [
        {'icon': '📍', 'value': '240k ha', 'label': 'Cobertura no raio 60km'},
        {'icon': '🎯', 'value': '4 cidades', 'label': 'Hot Spots atendidos'},
        {'icon': '💰', 'value': '-40%', 'label': 'Custo vs Hot Spots'},
        {'icon': '🎓', 'value': 'UFSC', 'label': 'Campus + Talentos'}
    ]
    
    positions = [(25, 48), (75, 48), (25, 33), (75, 33)]
    
    for metric, (x, y) in zip(metrics, positions):
        # Box individual
        box = FancyBboxPatch((x-10, y-5), 20, 10,
                            boxstyle="round,pad=0.5",
                            facecolor='white',
                            edgecolor='#c6f6d5',
                            linewidth=2)
        ax.add_patch(box)
        
        ax.text(x, y+2, metric['icon'], fontsize=20, ha='center')
        ax.text(x, y-1, metric['value'], 
                fontsize=14, weight='bold', ha='center', color='#22543d')
        ax.text(x, y-4, metric['label'], 
                fontsize=8, ha='center', color='#4a5568')
    
    # Hot Spots atendidos
    ax.text(50, 22, '🌾 Municípios Atendidos:', 
            fontsize=12, weight='bold', ha='center', color='#2d3748')
    
    cities = ['Campos Novos (90k ha)', 'Ponte Alta', 'Lebon Régis', 'São José do Cerrito']
    for i, city in enumerate(cities):
        ax.text(50, 18 - i*3, f'• {city}', 
                fontsize=10, ha='center', color='#4a5568')
    
    plt.tight_layout(pad=0)
    plt.savefig('data/outputs/linkedin_carousel_slide_2.png', 
                dpi=DPI, bbox_inches='tight', pad_inches=0,
                facecolor='white')
    plt.close()
    print("✅ Slide 2 criado: Curitibanos")


# ============================================
# SLIDE 3: CHAPECÓ
# ============================================
def create_slide_3():
    fig, ax = create_slide_base(
        "Expansão Oeste",
        "Chapecó • Fase 2 (12-24 meses)",
        slide_number=3
    )
    
    # Card principal
    card = FancyBboxPatch((10, 20), 80, 50,
                          boxstyle="round,pad=2",
                          facecolor='#ebf8ff',
                          edgecolor='#4299e1',
                          linewidth=4)
    ax.add_patch(card)
    
    # Nome da cidade
    ax.text(50, 63, 'CHAPECÓ', 
            fontsize=26, weight='bold', ha='center',
            color='#1e4e8c')
    
    # Métricas principais
    metrics = [
        {'icon': '📍', 'value': '280k ha', 'label': 'Cobertura Oeste SC'},
        {'icon': '🏭', 'value': 'Aurora', 'label': 'Cooperativa Integrada'},
        {'icon': '🤝', 'value': 'Copérdia', 'label': 'Parceria Regional'},
        {'icon': '🌽', 'value': 'Milho', 'label': 'Cultura Dominante'}
    ]
    
    positions = [(25, 48), (75, 48), (25, 33), (75, 33)]
    
    for metric, (x, y) in zip(metrics, positions):
        box = FancyBboxPatch((x-10, y-5), 20, 10,
                            boxstyle="round,pad=0.5",
                            facecolor='white',
                            edgecolor='#bee3f8',
                            linewidth=2)
        ax.add_patch(box)
        
        ax.text(x, y+2, metric['icon'], fontsize=20, ha='center')
        ax.text(x, y-1, metric['value'], 
                fontsize=14, weight='bold', ha='center', color='#1e4e8c')
        ax.text(x, y-4, metric['label'], 
                fontsize=8, ha='center', color='#4a5568')
    
    # Vantagem competitiva
    advantage_box = FancyBboxPatch((15, 10), 70, 8,
                                   boxstyle="round,pad=1",
                                   facecolor='#2C5F8D',
                                   edgecolor='#1a365d',
                                   linewidth=2)
    ax.add_patch(advantage_box)
    
    ax.text(50, 15, '✅ Região com maior densidade de cooperativas', 
            fontsize=11, weight='bold', ha='center', color='white')
    ax.text(50, 12, 'Suinocultura + Avicultura = demanda constante', 
            fontsize=9, ha='center', color='#bee3f8', style='italic')
    
    plt.tight_layout(pad=0)
    plt.savefig('data/outputs/linkedin_carousel_slide_3.png', 
                dpi=DPI, bbox_inches='tight', pad_inches=0,
                facecolor='white')
    plt.close()
    print("✅ Slide 3 criado: Chapecó")


# ============================================
# SLIDE 4: MAFRA
# ============================================
def create_slide_4():
    fig, ax = create_slide_base(
        "Expansão Norte",
        "Mafra • Fase 3 (24-36 meses)",
        slide_number=4
    )
    
    # Card principal
    card = FancyBboxPatch((10, 20), 80, 50,
                          boxstyle="round,pad=2",
                          facecolor='#fffaf0',
                          edgecolor='#ed8936',
                          linewidth=4)
    ax.add_patch(card)
    
    # Nome da cidade
    ax.text(50, 63, 'MAFRA', 
            fontsize=26, weight='bold', ha='center',
            color='#7c2d12')
    
    # Métricas principais
    metrics = [
        {'icon': '📍', 'value': '180k ha', 'label': 'Cobertura Norte SC'},
        {'icon': '🚪', 'value': 'Fronteira', 'label': 'Divisa com Paraná'},
        {'icon': '📈', 'value': '+TAM', 'label': 'Expansão PR'},
        {'icon': '🌲', 'value': 'Madeira', 'label': 'Setor Complementar'}
    ]
    
    positions = [(25, 48), (75, 48), (25, 33), (75, 33)]
    
    for metric, (x, y) in zip(metrics, positions):
        box = FancyBboxPatch((x-10, y-5), 20, 10,
                            boxstyle="round,pad=0.5",
                            facecolor='white',
                            edgecolor='#fed7aa',
                            linewidth=2)
        ax.add_patch(box)
        
        ax.text(x, y+2, metric['icon'], fontsize=20, ha='center')
        ax.text(x, y-1, metric['value'], 
                fontsize=14, weight='bold', ha='center', color='#7c2d12')
        ax.text(x, y-4, metric['label'], 
                fontsize=8, ha='center', color='#4a5568')
    
    # Oportunidade estratégica
    opportunity_box = FancyBboxPatch((15, 10), 70, 8,
                                     boxstyle="round,pad=1",
                                     facecolor='#ed8936',
                                     edgecolor='#7c2d12',
                                     linewidth=2)
    ax.add_patch(opportunity_box)
    
    ax.text(50, 15, '🎯 Porta de entrada para o mercado paranaense', 
            fontsize=11, weight='bold', ha='center', color='white')
    ax.text(50, 12, 'Potencial de duplicar TAM com expansão PR', 
            fontsize=9, ha='center', color='#fed7aa', style='italic')
    
    plt.tight_layout(pad=0)
    plt.savefig('data/outputs/linkedin_carousel_slide_4.png', 
                dpi=DPI, bbox_inches='tight', pad_inches=0,
                facecolor='white')
    plt.close()
    print("✅ Slide 4 criado: Mafra")


# ============================================
# SLIDE 5: COMPARATIVO + CTA
# ============================================
def create_slide_5():
    fig, ax = create_slide_base(
        "Comparativo Final",
        "Por que Cold Spots funcionam?",
        slide_number=5
    )
    
    # Tabela comparativa
    table_data = [
        ['', 'Curitibanos', 'Chapecó', 'Mafra'],
        ['Cobertura', '240k ha', '280k ha', '180k ha'],
        ['Municípios', '4', '6+', '5+'],
        ['OPEX', '-40%', '-30%', '-35%'],
        ['Score', '8.5/10', '8.0/10', '7.5/10']
    ]
    
    # Desenhar tabela manualmente
    colors = ['#48bb78', '#4299e1', '#ed8936']
    
    y_start = 62
    row_height = 6
    
    # Header
    for i, col in enumerate(table_data[0]):
        x = 20 + i * 20
        if i > 0:
            ax.add_patch(Rectangle((x-8, y_start-2), 16, row_height-1,
                                   facecolor=colors[i-1], alpha=0.2,
                                   edgecolor=colors[i-1], linewidth=2))
        ax.text(x, y_start, col, fontsize=11, weight='bold', 
                ha='center', va='center', color='#1a365d')
    
    # Linhas de dados
    for row_idx, row in enumerate(table_data[1:], 1):
        y = y_start - row_idx * row_height
        for col_idx, cell in enumerate(row):
            x = 20 + col_idx * 20
            if col_idx == 0:
                ax.text(x, y, cell, fontsize=10, weight='bold',
                       ha='center', va='center', color='#4a5568')
            else:
                ax.text(x, y, cell, fontsize=10,
                       ha='center', va='center', color='#2d3748')
    
    # Resultado financeiro
    result_box = FancyBboxPatch((12, 28), 76, 10,
                                boxstyle="round,pad=1",
                                facecolor='#f0fff4',
                                edgecolor='#48bb78',
                                linewidth=3)
    ax.add_patch(result_box)
    
    ax.text(50, 35, '💰 VIABILIDADE FINANCEIRA', 
            fontsize=14, weight='bold', ha='center', color='#22543d')
    
    financial = [
        '📈 TIR: 180%',
        '⏱️ Payback: 14 meses',
        '💵 VPL: R$ 4,2M'
    ]
    
    for i, metric in enumerate(financial):
        x = 23 + i * 27
        ax.text(x, 30, metric, fontsize=11, weight='bold',
               ha='center', color='#22543d')
    
    # CTA Principal
    cta_box = FancyBboxPatch((12, 10), 76, 14,
                            boxstyle="round,pad=1.5",
                            facecolor='#2C5F8D',
                            edgecolor='#1a365d',
                            linewidth=3)
    ax.add_patch(cta_box)
    
    ax.text(50, 20, '🔗 Acesse a análise completa', 
            fontsize=16, weight='bold', ha='center', color='white')
    
    ax.text(50, 16, 'Dashboard Interativo + Business Plan', 
            fontsize=11, ha='center', color='#bee3f8')
    
    ax.text(50, 12, 'Link nos comentários do post! 👇', 
            fontsize=12, weight='bold', ha='center', color='#fbd38d')
    
    plt.tight_layout(pad=0)
    plt.savefig('data/outputs/linkedin_carousel_slide_5.png', 
                dpi=DPI, bbox_inches='tight', pad_inches=0,
                facecolor='white')
    plt.close()
    print("✅ Slide 5 criado: Comparativo + CTA")


# ============================================
# EXECUTAR TUDO
# ============================================
if __name__ == "__main__":
    print("🎨 Gerando carrossel LinkedIn (5 slides)...\n")
    
    create_slide_1()
    create_slide_2()
    create_slide_3()
    create_slide_4()
    create_slide_5()
    
    print("\n✅ CARROSSEL COMPLETO!")
    print("\n📁 Arquivos gerados:")
    print("   • linkedin_carousel_slide_1.png (Capa)")
    print("   • linkedin_carousel_slide_2.png (Curitibanos)")
    print("   • linkedin_carousel_slide_3.png (Chapecó)")
    print("   • linkedin_carousel_slide_4.png (Mafra)")
    print("   • linkedin_carousel_slide_5.png (Comparativo + CTA)")
    print("\n📐 Dimensões: 1080x1080px cada (formato quadrado LinkedIn)")
    print("\n📤 Como usar no LinkedIn:")
    print("1. Criar post → 'Adicionar mídia' → 'Adicionar documento'")
    print("2. Selecionar os 5 arquivos PNG na ordem")
    print("3. LinkedIn vai criar um carrossel interativo automaticamente")
    print("4. Adicionar o texto do post (Versão 2 do posts_linkedin.md)")
    print("5. Publicar! 🚀")
