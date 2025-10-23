package dev.brightkan.ticket_line.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.annotations.servers.Server;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "TicketLine API",
                version = "1.0",
                description = "Event Ticketing System with JWT Authentication - " +
                        "A comprehensive REST API for managing event tickets, reservations, and purchases. " +
                        "Supports role-based access control with ADMIN and CUSTOMER roles.",
                contact = @Contact(
                        name = "TicketLine Support",
                        email = "support@ticketline.com"
                )
        ),
        servers = {
                @Server(url = "http://localhost:8080", description = "Local Development Server"),
                @Server(url = "https://api.ticketline.com", description = "Production Server")
        }
)
@SecurityScheme(
        name = "Bearer Authentication",
        type = SecuritySchemeType.HTTP,
        bearerFormat = "JWT",
        scheme = "bearer",
        description = "Enter JWT Bearer token obtained from /api/auth/login or /api/auth/register endpoint"
)
public class OpenApiConfig {
}
