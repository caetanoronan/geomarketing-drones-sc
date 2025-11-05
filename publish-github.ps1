# Script para Publicar no GitHub Pages
# Automatiza criação do repositório e deploy

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 PUBLICANDO NO GITHUB PAGES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurações
$REPO_NAME = "geomarketing-drones-sc"
$REPO_DESC = "Análise de mercado para drones agrícolas em Santa Catarina com dados IBGE 2024"

Write-Host "📋 Configurações:" -ForegroundColor Yellow
Write-Host "   Nome do repositório: $REPO_NAME"
Write-Host "   Descrição: $REPO_DESC"
Write-Host ""

# 1. Verificar se já é um repositório Git
Write-Host "[1/6] Verificando Git..." -ForegroundColor Green
if (Test-Path ".git") {
    Write-Host "   ⚠️  Repositório Git já existe!" -ForegroundColor Yellow
    $resposta = Read-Host "   Deseja reinicializar? (s/N)"
    if ($resposta -eq "s" -or $resposta -eq "S") {
        Remove-Item -Recurse -Force .git
        Write-Host "   ✓ Git reinicializado" -ForegroundColor Green
        git init
    }
} else {
    git init
    Write-Host "   ✓ Git inicializado" -ForegroundColor Green
}

# 2. Adicionar arquivos
Write-Host ""
Write-Host "[2/6] Adicionando arquivos..." -ForegroundColor Green
git add .
Write-Host "   ✓ Arquivos adicionados" -ForegroundColor Green

# 3. Commit inicial
Write-Host ""
Write-Host "[3/6] Criando commit..." -ForegroundColor Green
git commit -m "feat: Análise Geomarketing Drones Agrícolas SC

- 295 municípios analisados com dados REAIS IBGE PAM 2024
- Ranking completo: Campos Novos #1 (69.1 score, 90.879 ha)
- Mapa interativo otimizado para web (1.58 MB)
- Dashboard interativo com 7 abas
- Dados: 1,68M ha agrícolas, 814k ha soja
- Tecnologias: Python, GeoPandas, Folium, Matplotlib"

Write-Host "   ✓ Commit criado" -ForegroundColor Green

# 4. Verificar autenticação GitHub CLI
Write-Host ""
Write-Host "[4/6] Verificando autenticação GitHub..." -ForegroundColor Green
$auth_status = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ⚠️  Você não está autenticado no GitHub!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Vou abrir o navegador para você fazer login..." -ForegroundColor Cyan
    gh auth login
} else {
    Write-Host "   ✓ Autenticado no GitHub" -ForegroundColor Green
}

# 5. Criar repositório remoto
Write-Host ""
Write-Host "[5/6] Criando repositório no GitHub..." -ForegroundColor Green
Write-Host "   Escolha a visibilidade:" -ForegroundColor Yellow
Write-Host "   [1] Público (recomendado para GitHub Pages)"
Write-Host "   [2] Privado"
$visibilidade = Read-Host "   Escolha (1 ou 2)"

if ($visibilidade -eq "2") {
    $visibility_flag = "--private"
    Write-Host "   📝 Repositório será PRIVADO" -ForegroundColor Yellow
} else {
    $visibility_flag = "--public"
    Write-Host "   📝 Repositório será PÚBLICO" -ForegroundColor Green
}

# Criar repositório
gh repo create $REPO_NAME --source=. --description="$REPO_DESC" $visibility_flag --push

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Repositório criado e código enviado!" -ForegroundColor Green
} else {
    Write-Host "   ❌ Erro ao criar repositório!" -ForegroundColor Red
    Write-Host "   Tente criar manualmente em: https://github.com/new" -ForegroundColor Yellow
    exit 1
}

# 6. Ativar GitHub Pages
Write-Host ""
Write-Host "[6/6] Ativando GitHub Pages..." -ForegroundColor Green

# Obter username do GitHub
$username = gh api user --jq '.login'

# Ativar Pages via API
gh api repos/$username/$REPO_NAME/pages `
    -X POST `
    -f source[branch]=main `
    -f source[path]=/

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ GitHub Pages ativado!" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Não foi possível ativar Pages automaticamente" -ForegroundColor Yellow
    Write-Host "   Active manualmente em: https://github.com/$username/$REPO_NAME/settings/pages" -ForegroundColor Cyan
}

# Resultado final
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ PUBLICAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Seu repositório:" -ForegroundColor Cyan
Write-Host "   https://github.com/$username/$REPO_NAME" -ForegroundColor White
Write-Host ""
Write-Host "📱 Seu site (aguarde 2-3 minutos):" -ForegroundColor Cyan
Write-Host "   https://$username.github.io/$REPO_NAME/" -ForegroundColor White
Write-Host ""
Write-Host "📊 Dashboard principal:" -ForegroundColor Cyan
Write-Host "   https://$username.github.io/$REPO_NAME/data/outputs/apresentacao_drones_agro_sc.html" -ForegroundColor White
Write-Host ""
Write-Host "🗺️ Mapa interativo:" -ForegroundColor Cyan
Write-Host "   https://$username.github.io/$REPO_NAME/data/outputs/maps/mapa_interativo_WEB.html" -ForegroundColor White
Write-Host ""
Write-Host "⏰ Aguarde 2-3 minutos para o site ficar disponível" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 Parabéns! Seu projeto está no ar!" -ForegroundColor Green
Write-Host ""

# Perguntar se quer abrir o navegador
$abrir = Read-Host "Deseja abrir o repositório no navegador? (S/n)"
if ($abrir -ne "n" -and $abrir -ne "N") {
    Start-Process "https://github.com/$username/$REPO_NAME"
}
