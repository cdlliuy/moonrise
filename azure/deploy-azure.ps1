# Azure Container Apps Deployment Script (PowerShell)
# Usage: .\deploy-azure.ps1

param(
    [string]$ResourceGroup = "moonrise-rg",
    [string]$Location = "eastasia",  # Hong Kong - optimal for Asia
    [string]$Environment = "moonrise-env",
    [string]$AppName = "moonrise",
    [string]$AcrName = "moonriseacr",  # Must be globally unique
    [string]$ImageName = "moonrise",
    [string]$ImageTag = "latest"
)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🌙 Moonrise Azure Deployment Script" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
try {
    $azVersion = az --version 2>$null
    Write-Host "✓ Azure CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Check if logged in
Write-Host ""
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    $account = az account show 2>$null | ConvertFrom-Json
    $subscription = $account.name
    Write-Host "✓ Logged in to Azure" -ForegroundColor Green
    Write-Host "  Subscription: $subscription" -ForegroundColor Gray
} catch {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Create resource group
Write-Host ""
Write-Host "[1/7] Creating resource group..." -ForegroundColor Yellow
az group create `
  --name $ResourceGroup `
  --location $Location `
  --output none

Write-Host "✓ Resource group created: $ResourceGroup" -ForegroundColor Green

# Create Azure Container Registry
Write-Host ""
Write-Host "[2/7] Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create `
  --name $AcrName `
  --resource-group $ResourceGroup `
  --location $Location `
  --sku Basic `
  --admin-enabled true `
  --output none

Write-Host "✓ Container Registry created: $AcrName" -ForegroundColor Green

# Build and push Docker image
Write-Host ""
Write-Host "[3/7] Building Docker image..." -ForegroundColor Yellow
Write-Host "  This may take several minutes..." -ForegroundColor Gray

az acr build `
  --registry $AcrName `
  --image "${ImageName}:${ImageTag}" `
  --file Dockerfile `
  .

Write-Host "✓ Docker image built and pushed" -ForegroundColor Green

# Get ACR credentials
Write-Host ""
Write-Host "[4/7] Getting ACR credentials..." -ForegroundColor Yellow
$acrServer = az acr show --name $AcrName --query loginServer -o tsv
$acrUsername = az acr credential show --name $AcrName --query username -o tsv
$acrPassword = az acr credential show --name $AcrName --query passwords[0].value -o tsv

Write-Host "✓ ACR Server: $acrServer" -ForegroundColor Green

# Create Container Apps environment
Write-Host ""
Write-Host "[5/7] Creating Container Apps environment..." -ForegroundColor Yellow
az containerapp env create `
  --name $Environment `
  --resource-group $ResourceGroup `
  --location $Location `
  --output none

Write-Host "✓ Container Apps environment created" -ForegroundColor Green

# Deploy Container App
Write-Host ""
Write-Host "[6/7] Deploying Container App..." -ForegroundColor Yellow
az containerapp create `
  --name $AppName `
  --resource-group $ResourceGroup `
  --environment $Environment `
  --image "${acrServer}/${ImageName}:${ImageTag}" `
  --registry-server $acrServer `
  --registry-username $acrUsername `
  --registry-password $acrPassword `
  --target-port 8080 `
  --ingress external `
  --cpu 0.5 `
  --memory 1Gi `
  --min-replicas 0 `
  --max-replicas 3 `
  --env-vars DEPLOYMENT_PLATFORM=azure PORT=8080 `
  --output none

Write-Host "✓ Container App deployed" -ForegroundColor Green

# Get application URL
Write-Host ""
Write-Host "[7/7] Getting application URL..." -ForegroundColor Yellow
$appUrl = az containerapp show `
  --name $AppName `
  --resource-group $ResourceGroup `
  --query properties.configuration.ingress.fqdn `
  -o tsv

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application URL: https://$appUrl" -ForegroundColor Yellow
Write-Host ""
Write-Host "Resource Group: $ResourceGroup" -ForegroundColor Gray
Write-Host "Location: $Location (East Asia - Hong Kong)" -ForegroundColor Gray
Write-Host "Container App: $AppName" -ForegroundColor Gray
Write-Host "Container Registry: $AcrName" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Visit https://$appUrl in your browser"
Write-Host "2. Monitor at: https://portal.azure.com"
Write-Host "3. View logs: az containerapp logs show -n $AppName -g $ResourceGroup"
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
