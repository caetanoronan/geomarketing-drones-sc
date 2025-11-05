# 🚁 Análise de Geomarketing: Drones Agrícolas em Santa Catarina

## 🌐 Acesso Rápido

**🎯 Dashboard Interativo Principal:** [https://caetanoronan.github.io/geomarketing-drones-sc/](https://caetanoronan.github.io/geomarketing-drones-sc/)

## 📊 Sobre o Projeto

Análise completa do potencial de mercado para operações de **aluguel e venda de drones agrícolas** em Santa Catarina, utilizando dados oficiais do IBGE (PAM 2024).

## 🗺️ Mapas Disponíveis

### 📱 Versão Web (Recomendada)
- **Arquivo:** `mapa_interativo_WEB.html` (1.6 MB)
- **Carregamento:** Rápido (2-5 segundos)
- **Ideal para:** Navegação online, celulares, tablets
- [🌐 Abrir Mapa Interativo Web](maps/mapa_interativo_WEB.html)

### 💾 Versão HD Completa
- **Arquivo:** `mapa_interativo_REAL.html` (222.7 MB)
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
