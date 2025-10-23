# TicketLine API Guide

## Overview

TicketLine is a comprehensive event ticketing system REST API built with Spring Boot. It provides secure ticket reservation and purchase functionality with JWT authentication, role-based authorization, and PostgreSQL/H2 database persistence.

## Features

- **JWT Authentication & Authorization** - Secure token-based authentication
- **Role-Based Access Control** - ADMIN and CUSTOMER roles
- **Event Management** - Create, update, and manage events (Admin only)
- **Ticket Reservations** - Reserve tickets with expiration handling
- **Ticket Purchases** - Complete purchases with mock payment processing
- **Idempotent Operations** - Prevent duplicate reservations and purchases
- **Swagger Documentation** - Interactive API documentation
- **H2 Console** - In-memory database for development

## Getting Started

### Prerequisites

- Java 21 or higher
- Maven 3.9+

### Running the Application

```bash
# Build the application
./mvnw clean package

# Run the application
./mvnw spring-boot:run
```

The application will start on `http://localhost:8080`

## API Documentation

Once the application is running, access the interactive Swagger UI at:
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **API Docs**: http://localhost:8080/v3/api-docs
- **H2 Console**: http://localhost:8080/h2-console

### H2 Console Access
- **JDBC URL**: `jdbc:h2:mem:ticketline_db`
- **Username**: `sa`
- **Password**: (leave empty)

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@example.com",
  "password": "password123",
  "role": "ADMIN"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer",
  "userId": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "ADMIN"
}
```

### Events (Admin)

#### Create Event
```http
POST /api/events
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Tech Conference 2025",
  "description": "Annual technology conference",
  "eventDate": "2025-12-15T09:00:00",
  "venue": "Convention Center",
  "totalTickets": 500,
  "ticketPrice": 99.99
}
```

#### Update Event
```http
PUT /api/events/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Tech Conference 2025 - Updated",
  "description": "Annual technology conference with new speakers",
  "eventDate": "2025-12-15T09:00:00",
  "venue": "Convention Center Hall A",
  "totalTickets": 600,
  "ticketPrice": 89.99
}
```

#### Delete Event
```http
DELETE /api/events/{id}
Authorization: Bearer <token>
```

### Events (Public)

#### Get All Events
```http
GET /api/events
```

#### Get Event by ID
```http
GET /api/events/{id}
```

#### Get Upcoming Events
```http
GET /api/events/upcoming
```

#### Get Available Events
```http
GET /api/events/available
```

### Tickets (Customer)

#### Reserve Tickets
```http
POST /api/tickets/reserve
Authorization: Bearer <token>
Content-Type: application/json

{
  "eventId": 1,
  "quantity": 2
}
```

**Response:**
```json
{
  "id": 1,
  "userId": 2,
  "eventId": 1,
  "eventName": "Tech Conference 2025",
  "quantity": 2,
  "totalAmount": 199.98,
  "reservationToken": "RES-12345678-90AB-CDEF-1234-567890ABCDEF",
  "status": "ACTIVE",
  "expiresAt": "2025-10-23T11:00:00",
  "createdAt": "2025-10-23T10:45:00"
}
```

#### Purchase Reserved Tickets
```http
POST /api/tickets/purchase
Authorization: Bearer <token>
Content-Type: application/json

{
  "reservationToken": "RES-12345678-90AB-CDEF-1234-567890ABCDEF",
  "idempotencyKey": "unique-key-123"
}
```

**Response:**
```json
{
  "id": 1,
  "userId": 2,
  "eventId": 1,
  "eventName": "Tech Conference 2025",
  "quantity": 2,
  "totalAmount": 199.98,
  "purchaseToken": "PUR-12345678-90AB-CDEF-1234-567890ABCDEF",
  "paymentReference": "PAY-ABC12345",
  "purchasedAt": "2025-10-23T10:50:00"
}
```

#### Get My Reservations
```http
GET /api/tickets/my-reservations
Authorization: Bearer <token>
```

#### Get My Purchases
```http
GET /api/tickets/my-purchases
Authorization: Bearer <token>
```

#### Get Reservation Details
```http
GET /api/tickets/reservations/{reservationToken}
Authorization: Bearer <token>
```

## Testing Workflow

### 1. Register Admin User
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "password123",
    "role": "ADMIN"
  }'
```

### 2. Register Customer User
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer",
    "email": "customer@example.com",
    "password": "password123",
    "role": "CUSTOMER"
  }'
```

### 3. Login as Admin
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

### 4. Create Event (use admin token)
```bash
curl -X POST http://localhost:8080/api/events \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Conference 2025",
    "description": "Annual technology conference",
    "eventDate": "2025-12-15T09:00:00",
    "venue": "Convention Center",
    "totalTickets": 500,
    "ticketPrice": 99.99
  }'
```

### 5. Login as Customer
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer",
    "password": "password123"
  }'
```

### 6. Reserve Tickets (use customer token)
```bash
curl -X POST http://localhost:8080/api/tickets/reserve \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": 1,
    "quantity": 2
  }'
```

### 7. Purchase Tickets (use customer token and reservation token from step 6)
```bash
curl -X POST http://localhost:8080/api/tickets/purchase \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reservationToken": "YOUR_RESERVATION_TOKEN"
  }'
```

## Configuration

### Application Properties

Key configurations in `application.properties`:

- **Server Port**: `server.port=8080`
- **Database**: H2 in-memory (development) or PostgreSQL (production)
- **JWT Secret**: Configure for production
- **JWT Expiration**: 1 hour (3600000 ms)
- **Reservation Expiration**: 15 minutes

### Switching to PostgreSQL

To use PostgreSQL instead of H2:

1. Uncomment PostgreSQL configuration in `application.properties`
2. Comment out H2 configuration
3. Create database: `CREATE DATABASE tickets_db;`
4. Update username and password

## Architecture

### Technology Stack
- **Framework**: Spring Boot 3.5.6
- **Security**: Spring Security with JWT
- **Database**: Spring Data JPA with H2/PostgreSQL
- **API Documentation**: SpringDoc OpenAPI 3
- **Build Tool**: Maven

### Key Components
- **Controllers**: REST API endpoints
- **Services**: Business logic layer
- **Repositories**: Data access layer
- **Security**: JWT authentication and authorization
- **DTOs**: Request/response objects
- **Entities**: JPA database entities

## Security Features

- **Password Encryption**: BCrypt password encoding
- **JWT Tokens**: Secure token-based authentication
- **Role-Based Access**: ADMIN and CUSTOMER roles
- **Token Expiration**: Configurable token lifetime
- **CORS**: Configurable cross-origin resource sharing

## Payment Processing

The current implementation uses a **mock payment service** that simulates payment processing with a 95% success rate. In production, integrate with real payment gateways like:
- Stripe
- PayPal
- Square
- Braintree

## Error Handling

The API provides consistent error responses:

```json
{
  "timestamp": "2025-10-23T10:30:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Insufficient tickets available",
  "path": "/api/tickets/reserve",
  "traceId": "abc123"
}
```

### Common HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **409**: Conflict
- **402**: Payment Required
- **500**: Internal Server Error

## Idempotency

The system implements idempotency for critical operations:
- **Reservations**: Uses unique reservation tokens
- **Purchases**: Supports idempotency keys to prevent duplicate charges

## License

This project is developed for educational purposes.

## Support

For issues or questions, refer to the Swagger documentation at http://localhost:8080/swagger-ui.html
