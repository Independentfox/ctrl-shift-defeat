#!/bin/bash
# CO-FOUNDER AI — Azure Resource Provisioning
# Run: bash infra/provision.sh

set -e

RG="cofounder-ai-rg"
LOCATION="eastus"

echo "=== Creating Resource Group ==="
az group create --name $RG --location $LOCATION

echo "=== Creating Azure OpenAI Service ==="
az cognitiveservices account create \
  --name cofounder-openai \
  --resource-group $RG \
  --kind OpenAI \
  --sku S0 \
  --location $LOCATION

echo "=== Deploying OpenAI Models ==="
# gpt-4o
az cognitiveservices account deployment create \
  --name cofounder-openai \
  --resource-group $RG \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-08-06" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# gpt-4o-mini
az cognitiveservices account deployment create \
  --name cofounder-openai \
  --resource-group $RG \
  --deployment-name gpt-4o-mini \
  --model-name gpt-4o-mini \
  --model-version "2024-07-18" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# text-embedding-ada-002
az cognitiveservices account deployment create \
  --name cofounder-openai \
  --resource-group $RG \
  --deployment-name text-embedding-ada-002 \
  --model-name text-embedding-ada-002 \
  --model-version "2" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

echo "=== Creating Azure AI Search (Free) ==="
az search service create \
  --name cofounder-search \
  --resource-group $RG \
  --sku free \
  --location $LOCATION

echo "=== Creating Cosmos DB ==="
az cosmosdb create \
  --name cofounder-cosmos \
  --resource-group $RG \
  --kind GlobalDocumentDB \
  --default-consistency-level Session \
  --enable-free-tier true

echo "=== Creating Storage Account ==="
az storage account create \
  --name cofounderstorage \
  --resource-group $RG \
  --sku Standard_LRS \
  --location $LOCATION

echo "=== Getting Keys ==="
echo ""
echo "OpenAI Endpoint:"
az cognitiveservices account show --name cofounder-openai --resource-group $RG --query properties.endpoint -o tsv

echo "OpenAI Key:"
az cognitiveservices account keys list --name cofounder-openai --resource-group $RG --query key1 -o tsv

echo "Search Endpoint:"
echo "https://cofounder-search.search.windows.net"

echo "Search Key:"
az search admin-key show --service-name cofounder-search --resource-group $RG --query primaryKey -o tsv

echo "Cosmos Endpoint:"
az cosmosdb show --name cofounder-cosmos --resource-group $RG --query documentEndpoint -o tsv

echo "Cosmos Key:"
az cosmosdb keys list --name cofounder-cosmos --resource-group $RG --query primaryMasterKey -o tsv

echo "Storage Connection String:"
az storage account show-connection-string --name cofounderstorage --resource-group $RG --query connectionString -o tsv

echo ""
echo "=== Done! Copy the above values into your .env file ==="
