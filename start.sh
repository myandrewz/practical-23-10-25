#!/bin/bash

# TicketLine Quick Start Script

echo "=================================="
echo "TicketLine - Quick Start"
echo "=================================="
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ Docker and Docker Compose found"
    echo ""
    echo "Starting TicketLine with Docker..."
    echo ""

    # Start services
    docker-compose up -d

    echo ""
    echo "=================================="
    echo "Waiting for services to be ready..."
    echo "=================================="

    # Wait for application to be ready
    sleep 10

    echo ""
    echo "=================================="
    echo "TicketLine is starting!"
    echo "=================================="
    echo ""
    echo "Application will be available at:"
    echo "  - API:         http://localhost:8080"
    echo "  - Swagger UI:  http://localhost:8080/swagger-ui.html"
    echo "  - Health:      http://localhost:8080/actuator/health"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop:"
    echo "  docker-compose down"
    echo ""
    echo "=================================="

elif command -v java &> /dev/null && command -v ./mvnw &> /dev/null; then
    echo "✓ Java and Maven found"
    echo ""
    echo "Starting TicketLine locally..."
    echo ""

    # Build and run
    ./mvnw clean spring-boot:run

else
    echo "ERROR: Neither Docker nor Java/Maven found"
    echo ""
    echo "Please install one of the following:"
    echo "  1. Docker and Docker Compose (recommended)"
    echo "  2. Java 21+ and Maven 3.9+"
    echo ""
    exit 1
fi
