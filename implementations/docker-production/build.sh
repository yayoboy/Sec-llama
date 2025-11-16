#!/bin/bash
# Build Docker Images for Production Stack

set -e

echo "🏗️ Building Sec-Llama Production Images"
echo ""

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "⚠️ No .env file found. Using defaults."
fi

# Set image tag
TAG=${TAG:-latest}
REGISTRY=${REGISTRY:-localhost}

echo "📦 Building images with tag: $TAG"
echo ""

# Build Web UI
echo "Building Web UI image..."
docker build -t ${REGISTRY}/sec-llama-web-ui:${TAG} \
    -f Dockerfile \
    .

# Build MCP Server
echo "Building MCP Server image..."
docker build -t ${REGISTRY}/sec-llama-mcp:${TAG} \
    -f Dockerfile.mcp \
    .

# Build CLI Tools
echo "Building CLI Tools image..."
docker build -t ${REGISTRY}/sec-llama-cli:${TAG} \
    -f Dockerfile.cli \
    .

echo ""
echo "✅ All images built successfully!"
echo ""
echo "Images created:"
echo "  - ${REGISTRY}/sec-llama-web-ui:${TAG}"
echo "  - ${REGISTRY}/sec-llama-mcp:${TAG}"
echo "  - ${REGISTRY}/sec-llama-cli:${TAG}"
echo ""

# Optional: Push to registry
read -p "Push images to registry? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing images..."
    docker push ${REGISTRY}/sec-llama-web-ui:${TAG}
    docker push ${REGISTRY}/sec-llama-mcp:${TAG}
    docker push ${REGISTRY}/sec-llama-cli:${TAG}
    echo "✅ Images pushed to registry"
fi

echo ""
echo "Next steps:"
echo "  1. Update docker-stack.yml with your image names"
echo "  2. Deploy: docker stack deploy -c docker-stack/docker-stack.yml sec-llama"
echo ""
