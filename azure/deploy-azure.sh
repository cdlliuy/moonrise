#!/bin/bash

# Azure Container Apps Deployment Script
# Usage: ./deploy-azure.sh

set -e

# Configuration
RESOURCE_GROUP="moonrise-rg"
LOCATION="eastasia"  # Hong Kong - optimal for Asia
ENVIRONMENT="moonrise-env"
APP_NAME="moonrise"
ACR_NAME="moonriseacr"  # Must be globally unique, change if needed
IMAGE_NAME="moonrise"
IMAGE_TAG="latest"

echo "======================================"
echo "🌙 Moonrise Azure Deployment Script"
echo "======================================"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✓ Azure CLI found"

# Check if logged in
echo ""
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "Please login to Azure..."
    az login
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
echo "✓ Logged in to Azure"
echo "  Subscription: $SUBSCRIPTION"

# Create resource group
echo ""
echo "[1/7] Creating resource group..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --output none

echo "✓ Resource group created: $RESOURCE_GROUP"

# Create Azure Container Registry
echo ""
echo "[2/7] Creating Azure Container Registry..."
az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Basic \
  --admin-enabled true \
  --output none

echo "✓ Container Registry created: $ACR_NAME"

# Build and push Docker image
echo ""
echo "[3/7] Building Docker image..."
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME:$IMAGE_TAG \
  --file Dockerfile \
  .

echo "✓ Docker image built and pushed"

# Get ACR credentials
echo ""
echo "[4/7] Getting ACR credentials..."
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo "✓ ACR Server: $ACR_SERVER"

# Create Container Apps environment
echo ""
echo "[5/7] Creating Container Apps environment..."
az containerapp env create \
  --name $ENVIRONMENT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --output none

echo "✓ Container Apps environment created"

# Deploy Container App
echo ""
echo "[6/7] Deploying Container App..."
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG \
  --registry-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8080 \
  --ingress external \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 0 \
  --max-replicas 3 \
  --env-vars DEPLOYMENT_PLATFORM=azure PORT=8080 \
  --output none

echo "✓ Container App deployed"

# Get application URL
echo ""
echo "[7/7] Getting application URL..."
APP_URL=$(az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

echo ""
echo "======================================"
echo "🎉 Deployment Complete!"
echo "======================================"
echo ""
echo "Application URL: https://$APP_URL"
echo ""
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION (East Asia - Hong Kong)"
echo "Container App: $APP_NAME"
echo "Container Registry: $ACR_NAME"
echo ""
echo "Next steps:"
echo "1. Visit https://$APP_URL in your browser"
echo "2. Monitor at: https://portal.azure.com"
echo "3. View logs: az containerapp logs show -n $APP_NAME -g $RESOURCE_GROUP"
echo ""
echo "======================================"
