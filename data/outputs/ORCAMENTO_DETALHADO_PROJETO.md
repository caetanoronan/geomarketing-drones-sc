# ORÇAMENTO DETALHADO - PROJETO GEOMARKETING DRONES AGRÍCOLAS SC

**Projeto:** Análise Geoespacial para Localização Estratégica de Operações com Drones Agrícolas em Santa Catarina  
**Responsável:** Ronan Armando Caetano | UFSC/IFSC  
**Data:** Novembro 2025  
**Versão:** 1.0

---

## 📋 SUMÁRIO EXECUTIVO

Este documento apresenta o orçamento completo do projeto de geomarketing, dividido em:
- **Fase 1 (CONCLUÍDA):** Pesquisa, análise de dados e desenvolvimento de plataformas interativas
- **Fase 2 (PROPOSTA):** Validação em campo e ajustes baseados em feedback real
- **Fase 3 (PROPOSTA):** Expansão da metodologia para outros estados e culturas

**Investimento Fase 1 (realizado):** R$ 47.800,00  
**Investimento Fase 2 (proposto):** R$ 82.500,00  
**Investimento Fase 3 (proposto):** R$ 156.000,00  
**TOTAL PROJETO COMPLETO:** R$ 286.300,00

---

## 💰 FASE 1: DESENVOLVIMENTO INICIAL (CONCLUÍDA)

### 1.1 PESQUISA E COLETA DE DADOS (120 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Levantamento bibliográfico** | Revisão literatura sobre drones agrícolas, geomarketing e AgTech | 20h | R$ 80 | R$ 1.600 |
| **Coleta dados IBGE** | Download, limpeza e estruturação PAM 2024, Censo Agro 2017, Base Cartográfica | 30h | R$ 80 | R$ 2.400 |
| **Pesquisa de mercado** | Análise concorrência, precificação, modelos de negócio em drones agrícolas | 25h | R$ 80 | R$ 2.000 |
| **Validação de fontes** | Cross-check dados, identificação inconsistências, correções | 15h | R$ 80 | R$ 1.200 |
| **Documentação metodológica** | Elaboração protocolo de análise, critérios de scoring | 10h | R$ 80 | R$ 800 |
| **Pesquisa infraestrutura** | Mapeamento cooperativas, revendas, universidades via OSM | 20h | R$ 80 | R$ 1.600 |
| **SUBTOTAL PESQUISA** | | **120h** | | **R$ 9.600** |

---

### 1.2 ANÁLISE GEOESPACIAL E DESENVOLVIMENTO (180 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Setup ambiente Python** | Instalação bibliotecas (geopandas, folium, pandas, matplotlib), configuração IDE | 8h | R$ 100 | R$ 800 |
| **ETL e processamento dados** | Scripts de extração, transformação e carga de dados IBGE | 35h | R$ 100 | R$ 3.500 |
| **Algoritmo de scoring** | Desenvolvimento modelo ponderado 5 indicadores + normalização | 25h | R$ 120 | R$ 3.000 |
| **Análise espacial** | Cálculo clusters, densidade, áreas de influência (buffers, isócronas) | 30h | R$ 120 | R$ 3.600 |
| **Identificação Cold Spots** | Metodologia proprietária de localização estratégica | 20h | R$ 120 | R$ 2.400 |
| **Geração mapas interativos** | Folium: heatmaps, choropleth, markers, popups personalizados | 40h | R$ 100 | R$ 4.000 |
| **Visualizações gráficas** | Matplotlib/Plotly: rankings, barras, linhas, scatter plots | 15h | R$ 100 | R$ 1.500 |
| **Testes e validação** | Debugging, validação cruzada resultados, ajustes fine-tuning | 7h | R$ 100 | R$ 700 |
| **SUBTOTAL ANÁLISE** | | **180h** | | **R$ 19.500** |

---

### 1.3 DESENVOLVIMENTO WEB E UX/UI (95 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Dashboard interativo (9 abas)** | HTML/CSS/JS: estrutura, navegação por abas, layout responsivo | 30h | R$ 90 | R$ 2.700 |
| **Business Plan HTML** | Documento interativo com 8 seções, métricas, tabelas dinâmicas | 20h | R$ 90 | R$ 1.800 |
| **Pitch Deck HTML** | Apresentação executiva em slides com transições | 12h | R$ 90 | R$ 1.080 |
| **Modo escuro/claro** | Implementação toggle tema, persistência localStorage, paleta cores | 10h | R$ 90 | R$ 900 |
| **Otimização UX** | Navegação sticky, contraste, acessibilidade WCAG 2.1 | 8h | R$ 90 | R$ 720 |
| **Integração mapas** | Embed Folium maps, sincronização dados dashboard | 6h | R$ 90 | R$ 540 |
| **Gráficos Chart.js** | Implementação gráficos financeiros interativos | 5h | R$ 90 | R$ 450 |
| **Testes cross-browser** | Validação Chrome, Firefox, Safari, Edge + mobile | 4h | R$ 90 | R$ 360 |
| **SUBTOTAL WEB** | | **95h** | | **R$ 8.550** |

---

### 1.4 DOCUMENTAÇÃO E RELATÓRIOS (45 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Relatório final técnico** | Documento 50+ páginas com metodologia completa, resultados, recomendações | 20h | R$ 80 | R$ 1.600 |
| **Documentação código** | Comentários inline, README.md, guia de instalação | 10h | R$ 80 | R$ 800 |
| **Posts LinkedIn** | 4 versões otimizadas para diferentes públicos (técnico, storytelling, acadêmico) | 5h | R$ 80 | R$ 400 |
| **Apresentação investidores** | Slides executivos com highlights financeiros | 6h | R$ 80 | R$ 480 |
| **Material de divulgação** | Infográficos, capturas de tela, assets para redes sociais | 4h | R$ 80 | R$ 320 |
| **SUBTOTAL DOCUMENTAÇÃO** | | **45h** | | **R$ 3.600** |

---

### 1.5 INFRAESTRUTURA E FERRAMENTAS

| Item | Descrição | Quantidade | Valor Unit. | Subtotal |
|------|-----------|------------|-------------|----------|
| **GitHub Pro** | Repositório privado, GitHub Pages, Actions (6 meses) | 6 meses | R$ 25 | R$ 150 |
| **Domínio personalizado** | .com.br para GitHub Pages (opcional) | 1 ano | R$ 40 | R$ 40 |
| **Licença software GIS** | QGIS (gratuito) + plugins premium | - | R$ 0 | R$ 0 |
| **API OpenStreetMap** | Nominatim para geocoding (uso gratuito) | - | R$ 0 | R$ 0 |
| **Hospedagem dados** | GitHub LFS para arquivos pesados (5GB free) | - | R$ 0 | R$ 0 |
| **Ferramentas design** | Canva Pro para infográficos (3 meses) | 3 meses | R$ 45 | R$ 135 |
| **Energia elétrica** | Consumo adicional workstation (estimado) | 4 meses | R$ 80 | R$ 320 |
| **Internet dedicada** | Upload mapas pesados, versionamento Git | 4 meses | R$ 150 | R$ 600 |
| **SUBTOTAL INFRAESTRUTURA** | | | | **R$ 1.245** |

---

### 1.6 GESTÃO E COORDENAÇÃO (35 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Planejamento projeto** | Cronograma, milestones, definição escopo | 8h | R$ 100 | R$ 800 |
| **Reuniões coordenação** | Alinhamentos semanais, ajustes de rota | 12h | R$ 100 | R$ 1.200 |
| **Gestão Git/GitHub** | Commits, versionamento, documentação técnica | 10h | R$ 100 | R$ 1.000 |
| **Controle qualidade** | Revisões, testes, validações finais | 5h | R$ 100 | R$ 500 |
| **SUBTOTAL GESTÃO** | | **35h** | | **R$ 3.500** |

---

### 1.7 CUSTOS INDIRETOS E IMPOSTOS

| Item | Descrição | Base cálculo | Percentual | Subtotal |
|------|-----------|--------------|------------|----------|
| **Impostos (MEI/Simples)** | Tributação sobre serviços prestados | R$ 46.000 | 6% | R$ 2.760 |
| **Reserva contingência** | Imprevistos, ajustes não planejados | R$ 46.000 | 5% | R$ 2.300 |
| **SUBTOTAL INDIRETOS** | | | | **R$ 5.060** |

---

## 📊 RESUMO FASE 1 (CONCLUÍDA)

| Categoria | Valor | % Total |
|-----------|-------|---------|
| Pesquisa e Coleta de Dados | R$ 9.600 | 20,1% |
| Análise Geoespacial | R$ 19.500 | 40,8% |
| Desenvolvimento Web | R$ 8.550 | 17,9% |
| Documentação | R$ 3.600 | 7,5% |
| Infraestrutura | R$ 1.245 | 2,6% |
| Gestão | R$ 3.500 | 7,3% |
| Impostos e Contingência | R$ 5.060 | 10,6% |
| **TOTAL FASE 1** | **R$ 51.055** | **100%** |

**Total de horas trabalhadas:** 475 horas (≈ 3 meses em tempo integral)  
**Valor médio hora:** R$ 96,65

---

## 🚀 FASE 2: VALIDAÇÃO EM CAMPO (PROPOSTA)

### 2.1 PESQUISA QUALITATIVA (80 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Entrevistas produtores** | 20 entrevistas semiestruturadas em Campos Novos, Curitibanos, Mafra | 40h | R$ 100 | R$ 4.000 |
| **Visitas cooperativas** | Meetings com Aurora, Copérdia, Coopercampos (validação B2B) | 20h | R$ 100 | R$ 2.000 |
| **Análise qualitativa** | Transcrição, codificação, identificação padrões (NVivo/Atlas.ti) | 15h | R$ 100 | R$ 1.500 |
| **Relatório insights** | Documento com descobertas, ajustes modelo de negócio | 5h | R$ 100 | R$ 500 |
| **SUBTOTAL PESQUISA CAMPO** | | **80h** | | **R$ 8.000** |

---

### 2.2 DESENVOLVIMENTO MÓDULOS ADICIONAIS (120 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Calculadora ROI interativa** | Ferramenta web para produtor calcular retorno investimento drones | 25h | R$ 110 | R$ 2.750 |
| **Simulador de rotas** | Algoritmo de otimização de trajetos para pulverização | 30h | R$ 120 | R$ 3.600 |
| **Dashboard financeiro avançado** | Projeções personalizáveis, análise sensibilidade | 25h | R$ 110 | R$ 2.750 |
| **Integração API climática** | INMET/CPTEC para janelas operacionais ideais | 15h | R$ 110 | R$ 1.650 |
| **Módulo comparativo PR/RS** | Expansão análise para estados vizinhos | 20h | R$ 110 | R$ 2.200 |
| **Testes e deploy** | QA, ajustes, publicação features | 5h | R$ 110 | R$ 550 |
| **SUBTOTAL DESENVOLVIMENTO** | | **120h** | | **R$ 13.500** |

---

### 2.3 MARKETING E DIVULGAÇÃO (60 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Conteúdo técnico (blogs)** | 10 artigos para Medium/LinkedIn sobre AgTech e geomarketing | 30h | R$ 80 | R$ 2.400 |
| **Vídeos demonstrativos** | 3 vídeos curtos (1-2 min) mostrando plataforma | 15h | R$ 100 | R$ 1.500 |
| **Webinar para cooperativas** | Apresentação online + Q&A (preparação + execução) | 10h | R$ 100 | R$ 1.000 |
| **Press kit** | Material para imprensa, jornalistas especializados agro | 5h | R$ 80 | R$ 400 |
| **SUBTOTAL MARKETING** | | **60h** | | **R$ 5.300** |

---

### 2.4 DESPESAS OPERACIONAIS CAMPO

| Item | Descrição | Quantidade | Valor Unit. | Subtotal |
|------|-----------|------------|-------------|----------|
| **Viagens Campos Novos** | Combustível + pedágio (3 viagens, 800 km ida/volta) | 3 viagens | R$ 350 | R$ 1.050 |
| **Hospedagem** | Hotel/Airbnb (6 diárias totais) | 6 diárias | R$ 150 | R$ 900 |
| **Alimentação campo** | Refeições durante pesquisa | 6 dias | R$ 120 | R$ 720 |
| **Gravador + transcrição** | Equipamento entrevistas + serviço transcrição | 1 conjunto | R$ 800 | R$ 800 |
| **Material impressão** | Folders, cartões visita, brochuras | 1 lote | R$ 450 | R$ 450 |
| **Brindes corporativos** | Pen drives personalizados para cooperativas (50 un) | 50 un | R$ 25 | R$ 1.250 |
| **SUBTOTAL DESPESAS CAMPO** | | | | **R$ 5.170** |

---

### 2.5 CONSULTORIA ESPECIALIZADA

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Agrônomo consultor** | Revisão técnica aplicações, culturas, defensivos | 20h | R$ 150 | R$ 3.000 |
| **Piloto RPAS certificado** | Consultoria operacional drones, viabilidade rotas | 15h | R$ 180 | R$ 2.700 |
| **Advogado agro/regulação** | Assessment ANAC, MAPA, licenças estaduais | 10h | R$ 250 | R$ 2.500 |
| **Contador especializado** | Modelagem tributária, estrutura societária ideal | 8h | R$ 200 | R$ 1.600 |
| **SUBTOTAL CONSULTORIA** | | **53h** | | **R$ 9.800** |

---

### 2.6 FERRAMENTAS E SOFTWARE PREMIUM

| Item | Descrição | Período | Valor | Subtotal |
|------|-----------|---------|-------|----------|
| **Pix4D Mapper** | Software fotogrametria/NDVI profissional | 3 meses | R$ 1.200 | R$ 3.600 |
| **Tableau Desktop** | Visualizações avançadas, dashboards executivos | 6 meses | R$ 450 | R$ 2.700 |
| **NVivo/Atlas.ti** | Software análise qualitativa entrevistas | 3 meses | R$ 800 | R$ 2.400 |
| **ArcGIS Online** | Camadas adicionais, geocoding premium | 6 meses | R$ 350 | R$ 2.100 |
| **SUBTOTAL SOFTWARE** | | | | **R$ 10.800** |

---

### 2.7 CUSTOS INDIRETOS FASE 2

| Item | Base cálculo | Percentual | Subtotal |
|------|--------------|------------|----------|
| **Impostos** | R$ 52.570 | 6% | R$ 3.154 |
| **Contingência** | R$ 52.570 | 5% | R$ 2.629 |
| **SUBTOTAL INDIRETOS** | | | **R$ 5.783** |

---

## 📊 RESUMO FASE 2 (PROPOSTA)

| Categoria | Valor | % Total |
|-----------|-------|---------|
| Pesquisa Qualitativa | R$ 8.000 | 13,5% |
| Desenvolvimento Módulos | R$ 13.500 | 22,8% |
| Marketing | R$ 5.300 | 8,9% |
| Despesas Campo | R$ 5.170 | 8,7% |
| Consultoria | R$ 9.800 | 16,5% |
| Software Premium | R$ 10.800 | 18,2% |
| Impostos e Contingência | R$ 5.783 | 9,7% |
| **TOTAL FASE 2** | **R$ 58.353** | **100%** |

**Total de horas adicionais:** 313 horas (≈ 2 meses)  
**Duração estimada Fase 2:** 3-4 meses (incluindo field work)

---

## 🌎 FASE 3: EXPANSÃO REGIONAL (PROPOSTA)

### 3.1 EXPANSÃO GEOGRÁFICA (200 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Análise Paraná** | Replicação metodologia para 399 municípios PR | 60h | R$ 110 | R$ 6.600 |
| **Análise Rio Grande do Sul** | Replicação para 497 municípios RS | 70h | R$ 110 | R$ 7.700 |
| **Análise comparativa Sul** | Cross-state analysis, identificação padrões regionais | 25h | R$ 120 | R$ 3.000 |
| **Mapa interativo 3 estados** | Dashboard unificado SC-PR-RS | 30h | R$ 110 | R$ 3.300 |
| **Relatório técnico regional** | Documento 80+ páginas com metodologia expandida | 15h | R$ 100 | R$ 1.500 |
| **SUBTOTAL EXPANSÃO** | | **200h** | | **R$ 22.100** |

---

### 3.2 DIVERSIFICAÇÃO DE CULTURAS (150 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Módulo Horticultura** | Análise Vale do Itajaí (cebola, alho, tomate) | 40h | R$ 110 | R$ 4.400 |
| **Módulo Fruticultura** | Maçã (SC), uva (RS), análise viabilidade drones | 35h | R$ 110 | R$ 3.850 |
| **Módulo Pecuária** | Monitoramento rebanhos, pastagens (Lages, Campos Gerais) | 30h | R$ 110 | R$ 3.300 |
| **Módulo Florestal** | Inventário florestal, reflorestamento (Pinus, Eucalipto) | 25h | R$ 110 | R$ 2.750 |
| **Dashboard multi-culturas** | Interface seleção cultura + recomendações personalizadas | 20h | R$ 110 | R$ 2.200 |
| **SUBTOTAL CULTURAS** | | **150h** | | **R$ 16.500** |

---

### 3.3 INTELIGÊNCIA ARTIFICIAL E MACHINE LEARNING (180 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Modelo preditivo demanda** | ML para prever demanda sazonal por município | 50h | R$ 150 | R$ 7.500 |
| **Classificação imagens satélite** | CNN para detecção automática áreas agricultáveis | 60h | R$ 150 | R$ 9.000 |
| **Otimização rotas IA** | Algoritmo genético para maximizar cobertura/minimizar custo | 40h | R$ 150 | R$ 6.000 |
| **Chatbot consultivo** | IA conversacional para produtores (recomendações personalizadas) | 25h | R$ 140 | R$ 3.500 |
| **Deploy modelos cloud** | AWS SageMaker ou Google AI Platform | 5h | R$ 140 | R$ 700 |
| **SUBTOTAL IA/ML** | | **180h** | | **R$ 26.700** |

---

### 3.4 PLATAFORMA SaaS COMPLETA (250 horas)

| Item | Descrição | Horas | Valor/hora | Subtotal |
|------|-----------|-------|------------|----------|
| **Backend (Node.js/Python)** | API RESTful, autenticação, CRUD completo | 80h | R$ 130 | R$ 10.400 |
| **Frontend (React/Vue)** | Interface responsiva, painéis personalizáveis | 70h | R$ 120 | R$ 8.400 |
| **Banco de dados** | PostgreSQL + PostGIS para dados espaciais | 25h | R$ 120 | R$ 3.000 |
| **Integração pagamentos** | Stripe/PagSeguro para assinaturas SaaS | 15h | R$ 120 | R$ 1.800 |
| **Sistema multi-tenant** | Isolamento dados por cliente, planos (básico/pro/enterprise) | 30h | R$ 130 | R$ 3.900 |
| **Testes automatizados** | Jest, Pytest, Selenium (cobertura >80%) | 20h | R$ 120 | R$ 2.400 |
| **DevOps e CI/CD** | Docker, Kubernetes, GitHub Actions | 10h | R$ 130 | R$ 1.300 |
| **SUBTOTAL SaaS** | | **250h** | | **R$ 31.200** |

---

### 3.5 INFRAESTRUTURA CLOUD E ESCALABILIDADE

| Item | Descrição | Período | Valor/mês | Subtotal |
|------|-----------|---------|-----------|----------|
| **AWS/Google Cloud** | Compute (EC2/Compute Engine), Storage (S3/Cloud Storage) | 12 meses | R$ 800 | R$ 9.600 |
| **CDN Cloudflare Pro** | Performance global, DDoS protection | 12 meses | R$ 100 | R$ 1.200 |
| **Banco dados gerenciado** | RDS PostgreSQL ou Cloud SQL | 12 meses | R$ 350 | R$ 4.200 |
| **Monitoramento (Datadog)** | APM, logs, alertas | 12 meses | R$ 250 | R$ 3.000 |
| **SUBTOTAL CLOUD** | | | | **R$ 18.000** |

---

### 3.6 MARKETING E GO-TO-MARKET FASE 3

| Item | Descrição | Quantidade | Valor | Subtotal |
|------|-----------|------------|-------|----------|
| **Landing page SaaS** | Design profissional, copywriting, SEO | 1 projeto | R$ 4.500 | R$ 4.500 |
| **Campanha Google Ads** | 3 meses anúncios segmentados (agro, drones) | 3 meses | R$ 2.000 | R$ 6.000 |
| **Marketing conteúdo** | 20 artigos SEO + 10 estudos de caso | 30 artigos | R$ 200 | R$ 6.000 |
| **Presença eventos** | AgroBrasília, Agrishow, DroneShow (stands + materiais) | 3 eventos | R$ 3.500 | R$ 10.500 |
| **Vídeo institucional** | Produção profissional 3-5 min | 1 vídeo | R$ 8.000 | R$ 8.000 |
| **SUBTOTAL MARKETING** | | | | **R$ 35.000** |

---

### 3.7 EQUIPE E GESTÃO FASE 3

| Item | Descrição | Período | Valor/mês | Subtotal |
|------|-----------|---------|-----------|----------|
| **Product Manager** | Gestão roadmap, priorização features | 6 meses | R$ 8.000 | R$ 48.000 |
| **Designer UI/UX** | Interfaces, experiência usuário (part-time) | 6 meses | R$ 4.500 | R$ 27.000 |
| **DevOps Engineer** | Manutenção infra, performance (part-time) | 6 meses | R$ 5.000 | R$ 30.000 |
| **Coordenação geral** | Alinhamentos, reports, gestão stakeholders | 6 meses | R$ 3.500 | R$ 21.000 |
| **SUBTOTAL EQUIPE** | | | | **R$ 126.000** |

---

### 3.8 CUSTOS INDIRETOS FASE 3

| Item | Base cálculo | Percentual | Subtotal |
|------|--------------|------------|----------|
| **Impostos** | R$ 275.500 | 6% | R$ 16.530 |
| **Contingência** | R$ 275.500 | 5% | R$ 13.775 |
| **SUBTOTAL INDIRETOS** | | | **R$ 30.305** |

---

## 📊 RESUMO FASE 3 (PROPOSTA)

| Categoria | Valor | % Total |
|-----------|-------|---------|
| Expansão Geográfica | R$ 22.100 | 7,2% |
| Diversificação Culturas | R$ 16.500 | 5,4% |
| IA e Machine Learning | R$ 26.700 | 8,7% |
| Plataforma SaaS | R$ 31.200 | 10,2% |
| Infraestrutura Cloud | R$ 18.000 | 5,9% |
| Marketing Go-to-Market | R$ 35.000 | 11,4% |
| Equipe (6 meses) | R$ 126.000 | 41,2% |
| Impostos e Contingência | R$ 30.305 | 9,9% |
| **TOTAL FASE 3** | **R$ 305.805** | **100%** |

**Total de horas desenvolvimento:** 780 horas  
**Duração estimada Fase 3:** 6-8 meses  
**Tamanho equipe:** 4 pessoas (PM, Designer, DevOps, Coordenador)

---

## 💼 CONSOLIDADO GERAL DO PROJETO

| Fase | Descrição | Status | Valor | Prazo |
|------|-----------|--------|-------|-------|
| **Fase 1** | Pesquisa, análise, plataformas interativas | ✅ **CONCLUÍDA** | R$ 51.055 | 3-4 meses |
| **Fase 2** | Validação campo, módulos avançados | 🟡 **PROPOSTA** | R$ 58.353 | 3-4 meses |
| **Fase 3** | Expansão regional, SaaS, IA | 🟡 **PROPOSTA** | R$ 305.805 | 6-8 meses |
| | | | | |
| **SUBTOTAL TÉCNICO** | | | **R$ 415.213** | **12-16 meses** |
| **Desconto investidor (15%)** | Redução para captação única 3 fases | | **-R$ 62.282** | |
| **VALOR INVESTIMENTO** | | | **R$ 352.931** | |

---

## 📈 PROJEÇÃO DE RECEITA (CASO EVOLUA PARA PRODUTO)

### Cenário: Plataforma SaaS para Operadores de Drones Agrícolas

| Métrica | Ano 1 | Ano 2 | Ano 3 |
|---------|-------|-------|-------|
| **Clientes ativos (operadores)** | 15 | 45 | 120 |
| **Ticket médio mensal** | R$ 800 | R$ 1.200 | R$ 1.500 |
| **MRR (Receita Recorrente Mensal)** | R$ 12.000 | R$ 54.000 | R$ 180.000 |
| **ARR (Receita Recorrente Anual)** | R$ 144.000 | R$ 648.000 | R$ 2.160.000 |
| **Receita consultoria/personalização** | R$ 80.000 | R$ 150.000 | R$ 300.000 |
| **RECEITA TOTAL** | R$ 224.000 | R$ 798.000 | R$ 2.460.000 |
| **Custo operacional** | R$ 120.000 | R$ 280.000 | R$ 650.000 |
| **EBITDA** | R$ 104.000 | R$ 518.000 | R$ 1.810.000 |
| **Margem EBITDA** | 46,4% | 64,9% | 73,6% |

**Valuation estimado (Ano 3):** R$ 18-25M (10-12x ARR padrão SaaS B2B)

---

## 🎯 FORMAS DE CONTRATAÇÃO

### Opção A: INVESTIMENTO EQUITY (RECOMENDADO)

**Investidor aporta:** R$ 352.931 (3 fases completas)  
**Contrapartida:** 20-35% equity da futura empresa + direitos sobre IP  
**Modelo:** Seed Investment via SAFE ou Convertible Note  
**Vesting:** 4 anos com cliff de 1 ano  
**Target exit:** Aquisição por player AgTech (Solinftec, Aegro, Climate FieldView) ou IPO Ano 5

**Vantagens investidor:**
- Potencial retorno 10-20x em 5 anos
- Participação em mercado AgTech (CAGR 15% a.a. no Brasil)
- Produto com tração comprovada (dados reais IBGE)

---

### Opção B: CONTRATAÇÃO POR ETAPAS

**Fase 2 isolada:** R$ 58.353 (consultoria + validação)  
**Fase 3 isolada:** R$ 305.805 (desenvolvimento SaaS completo)  

**Modelo:** Prestação de serviços com milestones  
**Pagamento:** 30% início / 40% meio / 30% entrega  
**Propriedade IP:** Negociável (licença exclusiva vs. compartilhada)

---

### Opção C: LICENCIAMENTO DE METODOLOGIA

**Investidor licencia metodologia pronta (Fase 1):** R$ 120.000  
**Inclui:** Acesso código-fonte, dados processados, documentação completa, treinamento 20h  
**Uso:** Replicação para outras regiões/culturas por conta do licenciado  
**Modelo:** Licença perpétua não-exclusiva + royalties 5% sobre receita derivada

---

## 📋 CRONOGRAMA MACRO

```
MÊS 1-3   | FASE 1 ✅ CONCLUÍDA
          | - Pesquisa e análise
          | - Desenvolvimento plataformas
          | - Documentação
          |
MÊS 4-7   | FASE 2 (SE APROVADA)
          | - Validação campo
          | - Módulos avançados
          | - Marketing inicial
          |
MÊS 8-15  | FASE 3 (SE APROVADA)
          | - Expansão regional
          | - Desenvolvimento SaaS
          | - IA e ML
          | - Go-to-market
          |
MÊS 16+   | OPERAÇÃO COMERCIAL
          | - Vendas B2B
          | - Escala produto
          | - Novas rodadas captação
```

---

## 🔒 GARANTIAS E ENTREGAS

### Fase 1 (Concluída) - Entregas Realizadas:
✅ Relatório técnico completo (50+ páginas)  
✅ Dashboard interativo (9 abas) com modo escuro  
✅ Business Plan HTML detalhado  
✅ Pitch Deck executivo  
✅ 15+ mapas interativos (heatmaps, cold spots)  
✅ Código-fonte documentado (GitHub)  
✅ Dados processados (CSV, GeoJSON)  
✅ Posts LinkedIn (4 versões)  

### Fase 2 (Proposta) - Entregas Previstas:
📋 20 entrevistas transcritas + análise qualitativa  
📋 Calculadora ROI interativa  
📋 Simulador de rotas otimizadas  
📋 Dashboard financeiro avançado  
📋 3 vídeos demonstrativos  
📋 Relatório validação campo (30+ páginas)  

### Fase 3 (Proposta) - Entregas Previstas:
📋 Análise completa SC + PR + RS (1.191 municípios)  
📋 4 módulos culturas (horticultura, fruticultura, pecuária, florestal)  
📋 Plataforma SaaS funcional (MVP)  
📋 3 modelos IA/ML treinados  
📋 Infraestrutura cloud escalável  
📋 Documentação técnica API  

---

## 📞 CONTATO PARA PROPOSTA COMERCIAL

**Responsável:** Ronan Armando Caetano  
**Formação:** Geoprocessamento (IFSC) | Ciências Biológicas (UFSC)  
**E-mail:** ronan.caetano@ufsc.br  
**LinkedIn:** [Inserir link]  
**GitHub:** github.com/caetanoronan/geomarketing-drones-sc  
**Portfolio:** https://caetanoronan.github.io/geomarketing-drones-sc/

---

## 📎 ANEXOS

1. **Demonstração ao vivo:** Dashboard interativo disponível 24/7
2. **Portfólio GitHub:** Código-fonte, commits, documentação
3. **Relatório técnico completo:** RELATORIO_FINAL_DRONES_AGRO_SC.md
4. **Business Plan detalhado:** business_plan_drones_agro_sc.html
5. **Mapas interativos:** 15 visualizações geoespaciais
6. **Dados brutos processados:** 295 municípios mapeados

---

**Documento gerado em:** Novembro 2025  
**Validade proposta:** 60 dias  
**Versão:** 1.0

---

*Este orçamento reflete valores de mercado brasileiro para serviços especializados em geoprocessamento, análise de dados, desenvolvimento web e consultoria AgTech. Todos os valores podem ser ajustados mediante negociação e escopo detalhado.*
