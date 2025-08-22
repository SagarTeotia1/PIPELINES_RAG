#!/bin/bash

# RAG Pipeline Deployment Script
# This script provides a comprehensive deployment solution for the RAG Pipeline

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="rag-pipeline"
DOCKER_IMAGE="rag-pipeline:latest"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    success "Docker is running"
}

# Check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        error "Docker Compose is not available. Please install Docker Compose and try again."
        exit 1
    fi
    success "Docker Compose is available"
}

# Check environment file
check_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        error "Environment file $ENV_FILE not found. Please create it with your configuration."
        echo "Required environment variables:"
        echo "  GEMINI_API_KEY=your_gemini_api_key"
        echo "  CHROMA_API_KEY=your_chroma_api_key"
        echo "  CHROMA_TENANT=your_chroma_tenant"
        echo "  CHROMA_DATABASE=your_chroma_database"
        echo "  MONGODB_URI=your_mongodb_uri"
        exit 1
    fi
    success "Environment file found"
}

# Build the application
build_app() {
    log "Building Docker image..."
    docker build -t $DOCKER_IMAGE .
    success "Docker image built successfully"
}

# Start the application
start_app() {
    log "Starting RAG Pipeline..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE up -d
    else
        docker compose -f $COMPOSE_FILE up -d
    fi
    success "RAG Pipeline started successfully"
}

# Stop the application
stop_app() {
    log "Stopping RAG Pipeline..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE down
    else
        docker compose -f $COMPOSE_FILE down
    fi
    success "RAG Pipeline stopped successfully"
}

# Restart the application
restart_app() {
    log "Restarting RAG Pipeline..."
    stop_app
    sleep 2
    start_app
    success "RAG Pipeline restarted successfully"
}

# Show application status
show_status() {
    log "Application Status:"
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE ps
    else
        docker compose -f $COMPOSE_FILE ps
    fi
    
    echo ""
    log "Container Logs:"
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE logs --tail=20
    else
        docker compose -f $COMPOSE_FILE logs --tail=20
    fi
}

# Show application logs
show_logs() {
    log "Showing application logs (press Ctrl+C to exit)..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE logs -f
    else
        docker compose -f $COMPOSE_FILE logs -f
    fi
}

# Clean up resources
cleanup() {
    log "Cleaning up Docker resources..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f $COMPOSE_FILE down -v --remove-orphans
    else
        docker compose -f $COMPOSE_FILE down -v --remove-orphans
    fi
    docker system prune -f
    success "Cleanup completed"
}

# Health check
health_check() {
    log "Performing health check..."
    sleep 10  # Wait for services to start
    
    # Check if the application is responding
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        success "Application is healthy and responding"
        log "Application URL: http://localhost:8000"
        log "API Documentation: http://localhost:8000/docs"
    else
        error "Application health check failed"
        return 1
    fi
}

# Show help
show_help() {
    echo "RAG Pipeline Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  start     Start the application"
    echo "  stop      Stop the application"
    echo "  restart   Restart the application"
    echo "  status    Show application status"
    echo "  logs      Show application logs"
    echo "  health    Perform health check"
    echo "  cleanup   Clean up Docker resources"
    echo "  deploy    Full deployment (build + start + health check)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Full deployment"
    echo "  $0 start     # Start only"
    echo "  $0 logs      # View logs"
}

# Main deployment function
deploy() {
    log "Starting full deployment..."
    check_docker
    check_docker_compose
    check_env_file
    build_app
    start_app
    health_check
    success "Deployment completed successfully!"
}

# Main script logic
case "${1:-deploy}" in
    "build")
        check_docker
        build_app
        ;;
    "start")
        check_docker
        check_docker_compose
        check_env_file
        start_app
        ;;
    "stop")
        check_docker
        check_docker_compose
        stop_app
        ;;
    "restart")
        check_docker
        check_docker_compose
        restart_app
        ;;
    "status")
        check_docker
        check_docker_compose
        show_status
        ;;
    "logs")
        check_docker
        check_docker_compose
        show_logs
        ;;
    "health")
        health_check
        ;;
    "cleanup")
        check_docker
        check_docker_compose
        cleanup
        ;;
    "deploy")
        deploy
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
