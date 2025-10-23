# Quick Start Guide for Instructors

This guide will get TicketLine running in under 2 minutes.

## Fastest Way to Run (Docker)

If you have Docker installed:

```bash
# 1. Navigate to the project directory
cd ticket-line

# 2. Run the quick start script
./start.sh

# OR manually:
docker-compose up -d
```

The application will be available at:
- **API**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **Health Check**: http://localhost:8080/actuator/health

## Alternative: Run Locally (Java)

If you prefer to run without Docker:

```bash
# 1. Navigate to the project directory
cd ticket-line

# 2. Run the application
./mvnw spring-boot:run
```

The application will start with an in-memory H2 database.

## Test the API

Open your browser and go to:
```
http://localhost:8080/swagger-ui.html
```

This interactive documentation lets you test all API endpoints directly from your browser.

### Quick API Test (Command Line)

```bash
# 1. Register a user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"password123","role":"ADMIN"}'

# 2. Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# 3. View the Swagger UI for more
# Open http://localhost:8080/swagger-ui.html
```

## Stopping the Application

### Docker:
```bash
docker-compose down
```

### Local:
Press `Ctrl+C` in the terminal where the application is running.

## What's Running?

### With Docker:
- PostgreSQL database on port 5432
- TicketLine API on port 8080

### Local:
- H2 in-memory database
- TicketLine API on port 8080
- H2 Console at http://localhost:8080/h2-console

## Troubleshooting

### Port 8080 already in use:
```bash
# Find what's using port 8080
lsof -i :8080

# Kill it or change the port in docker-compose.yml or application.properties
```

### Docker issues:
```bash
# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Full Documentation

For complete documentation, see [README.md](README.md)

For API details, see [API_GUIDE.md](API_GUIDE.md)
