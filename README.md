# TicketLine - Event Ticketing System

A production-ready Spring Boot REST API for event ticketing with secure JWT authentication, ticket reservations, and payment processing.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Development](#option-2-local-development)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Testing the API](#testing-the-api)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

## Features

- JWT-based authentication and authorization
- Role-based access control (ADMIN, CUSTOMER)
- Event management (CRUD operations)
- Ticket reservations with automatic expiration (15 minutes)
- Ticket purchase with payment processing
- Idempotent operations to prevent duplicate charges
- Optimistic locking for concurrent ticket bookings
- Interactive Swagger/OpenAPI documentation
- Health checks and monitoring endpoints
- PostgreSQL for production, H2 for development

## Prerequisites

### For Docker Deployment (Recommended)
- Docker 20.10+
- Docker Compose 2.0+

### For Local Development
- Java 21 or higher
- Maven 3.9+
- PostgreSQL 12+ (for production mode)

## Quick Start

### Option 1: Docker (Recommended)

This is the easiest way to run the application with all dependencies.

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd ticket-line

# 2. Start the application with Docker Compose
docker-compose up -d

# 3. Wait for the application to start (about 30 seconds)
# Check logs
docker-compose logs -f ticketline-api

# 4. Access the application
# API: http://localhost:8080
# Swagger UI: http://localhost:8080/swagger-ui.html
# Health Check: http://localhost:8080/actuator/health
```

To stop the application:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
```

### Option 2: Local Development

Run the application locally with H2 in-memory database.

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd ticket-line

# 2. Build the application
./mvnw clean package

# 3. Run the application
./mvnw spring-boot:run

# 4. Access the application
# API: http://localhost:8080
# Swagger UI: http://localhost:8080/swagger-ui.html
# H2 Console: http://localhost:8080/h2-console
# Health Check: http://localhost:8080/actuator/health
```

#### H2 Console Access (Development Only)
- JDBC URL: `jdbc:h2:mem:ticketline_db`
- Username: `sa`
- Password: (leave empty)

## Production Deployment

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env

# Edit the file with your production values
nano .env
```

Required environment variables:
```bash
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=tickets_db
DB_USERNAME=your-db-user
DB_PASSWORD=your-secure-password
JWT_SECRET=your-very-long-random-secret-key-minimum-256-bits
```

### Deployment Options

#### 1. Docker Compose (Recommended)

```bash
# 1. Configure environment variables
cp .env.example .env
# Edit .env with your production values

# 2. Update docker-compose.yml with production settings
# - Change database password
# - Update JWT secret
# - Configure any additional environment variables

# 3. Deploy
docker-compose up -d

# 4. View logs
docker-compose logs -f

# 5. Check health
curl http://localhost:8080/actuator/health
```

#### 2. Build and Deploy JAR

```bash
# 1. Build the production JAR
./mvnw clean package -DskipTests

# 2. Set environment variables
export SPRING_PROFILES_ACTIVE=prod
export DB_HOST=your-database-host
export DB_USERNAME=your-db-user
export DB_PASSWORD=your-db-password
export JWT_SECRET=your-secret-key

# 3. Run the application
java -jar target/ticket-line-0.0.1-SNAPSHOT.jar
```

#### 3. Docker Container Only

```bash
# 1. Build the Docker image
docker build -t ticketline-api .

# 2. Run the container
docker run -d \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e DB_HOST=your-db-host \
  -e DB_USERNAME=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e JWT_SECRET=your-secret-key \
  --name ticketline-api \
  ticketline-api
```

### Database Setup

For production, you need PostgreSQL:

```bash
# 1. Create database
psql -U postgres
CREATE DATABASE tickets_db;
CREATE USER ticketline_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE tickets_db TO ticketline_user;
\q

# 2. Update application configuration
# Edit .env or set environment variables with your database credentials
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **OpenAPI JSON**: http://localhost:8080/v3/api-docs
- **Health Check**: http://localhost:8080/actuator/health

For detailed API usage examples, see [API_GUIDE.md](API_GUIDE.md)

## Testing the API

### Quick Test Workflow

```bash
# 1. Register an admin user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "password123",
    "role": "ADMIN"
  }'

# 2. Login to get JWT token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
# Save the token from the response

# 3. Create an event (use the token from step 2)
curl -X POST http://localhost:8080/api/events \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Conference 2025",
    "description": "Annual technology conference",
    "eventDate": "2025-12-15T09:00:00",
    "venue": "Convention Center",
    "totalTickets": 500,
    "ticketPrice": 99.99
  }'

# 4. View all events (public endpoint)
curl http://localhost:8080/api/events

# 5. Register a customer
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer",
    "email": "customer@example.com",
    "password": "password123",
    "role": "CUSTOMER"
  }'

# 6. Login as customer
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer",
    "password": "password123"
  }'

# 7. Reserve tickets
curl -X POST http://localhost:8080/api/tickets/reserve \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": 1,
    "quantity": 2
  }'
# Save the reservationToken from the response

# 8. Purchase tickets
curl -X POST http://localhost:8080/api/tickets/purchase \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reservationToken": "YOUR_RESERVATION_TOKEN"
  }'
```

For more detailed API examples, refer to [API_GUIDE.md](API_GUIDE.md) or use the interactive Swagger UI.

## Configuration

### Key Configuration Files

- `src/main/resources/application.properties` - Development configuration (H2 database)
- `src/main/resources/application-prod.properties` - Production configuration (PostgreSQL)
- `.env.example` - Template for environment variables
- `docker-compose.yml` - Docker deployment configuration

### Important Settings

| Setting | Development | Production |
|---------|------------|------------|
| Database | H2 (in-memory) | PostgreSQL |
| Port | 8080 | 8080 (configurable) |
| JWT Expiration | 1 hour | 1 hour (configurable) |
| Reservation Expiration | 15 minutes | 15 minutes (configurable) |
| Logging Level | DEBUG | INFO/WARN |
| H2 Console | Enabled | Disabled |

### Security Configuration

**IMPORTANT**: Before deploying to production:

1. Change the JWT secret key in `.env`:
   ```bash
   JWT_SECRET=your-very-long-random-secret-key-minimum-256-bits
   ```
   Generate a secure key:
   ```bash
   openssl rand -base64 64
   ```

2. Update database credentials
3. Configure CORS if needed (in `SecurityConfig.java`)
4. Enable HTTPS/TLS for production

## Project Structure

```
ticket-line/
├── src/
│   ├── main/
│   │   ├── java/dev/brightkan/ticket_line/
│   │   │   ├── controller/        # REST API endpoints
│   │   │   ├── service/           # Business logic
│   │   │   ├── repository/        # Data access layer
│   │   │   ├── model/             # Entities and DTOs
│   │   │   ├── security/          # JWT and security config
│   │   │   ├── config/            # Application configuration
│   │   │   └── exception/         # Custom exceptions
│   │   └── resources/
│   │       ├── application.properties           # Dev config
│   │       └── application-prod.properties      # Prod config
│   └── test/                      # Test classes
├── Dockerfile                     # Docker image configuration
├── docker-compose.yml             # Docker Compose setup
├── .env.example                   # Environment variables template
├── pom.xml                        # Maven dependencies
├── README.md                      # This file
└── API_GUIDE.md                   # Detailed API documentation
```

## Security

### Authentication & Authorization

- **JWT Tokens**: Used for stateless authentication
- **Password Encryption**: BCrypt with strength 10
- **Role-Based Access Control**:
  - `ADMIN`: Can manage events
  - `CUSTOMER`: Can reserve and purchase tickets

### API Security

- Public endpoints: `/api/auth/**`, `/api/events` (GET)
- Admin endpoints: `/api/events` (POST, PUT, DELETE)
- Customer endpoints: `/api/tickets/**`
- Swagger UI: Public (disable in production if needed)

### Payment Security

**NOTE**: The current implementation uses a mock payment service for demonstration purposes. For production:

1. Integrate with a real payment gateway (Stripe, PayPal, Square)
2. Implement PCI DSS compliance
3. Add webhook handlers for payment confirmations
4. Implement proper refund handling

## Troubleshooting

### Application won't start

```bash
# Check Java version
java -version  # Should be 21+

# Check if port 8080 is available
lsof -i :8080

# Check logs
docker-compose logs ticketline-api
# or
./mvnw spring-boot:run
```

### Database connection issues

```bash
# For Docker
docker-compose ps  # Check if postgres is running
docker-compose logs postgres

# For local PostgreSQL
psql -U ticketline_user -d tickets_db -h localhost
```

### Docker issues

```bash
# Rebuild containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker-compose ps

# View logs
docker-compose logs -f
```

### H2 Console not accessible

Make sure you're running in development mode (not production profile):
```bash
./mvnw spring-boot:run
# or
java -jar target/ticket-line-0.0.1-SNAPSHOT.jar
```

### JWT token errors

- Ensure JWT_SECRET is properly set
- Check token expiration (default: 1 hour)
- Verify the Bearer token format: `Authorization: Bearer <token>`

## Tech Stack

- **Framework**: Spring Boot 3.5.6
- **Language**: Java 21
- **Security**: Spring Security + JWT
- **Database**: PostgreSQL (production), H2 (development)
- **Documentation**: SpringDoc OpenAPI 3 (Swagger)
- **Build Tool**: Maven 3.9+
- **Containerization**: Docker & Docker Compose

## License

This project is developed for educational purposes.

## Support

For detailed API documentation and examples, see [API_GUIDE.md](API_GUIDE.md)

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the Swagger documentation at http://localhost:8080/swagger-ui.html
3. Check application logs

---

**Made with Spring Boot** | **Ready for Production**
