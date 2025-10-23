package dev.brightkan.ticket_line.controller;

import dev.brightkan.ticket_line.dto.PurchaseRequest;
import dev.brightkan.ticket_line.dto.PurchaseResponse;
import dev.brightkan.ticket_line.dto.ReservationRequest;
import dev.brightkan.ticket_line.dto.ReservationResponse;
import dev.brightkan.ticket_line.security.CustomUserDetails;
import dev.brightkan.ticket_line.service.TicketService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tickets")
@RequiredArgsConstructor
@Tag(name = "Tickets", description = "Ticket reservation and purchase endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class TicketController {

    private final TicketService ticketService;

    @PostMapping("/reserve")
    @PreAuthorize("hasRole('CUSTOMER')")
    @Operation(summary = "Reserve tickets", description = "Reserve tickets for an event (Customer only)")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Tickets reserved successfully",
                    content = @Content(schema = @Schema(implementation = ReservationResponse.class))),
            @ApiResponse(responseCode = "400", description = "Insufficient tickets or invalid request"),
            @ApiResponse(responseCode = "403", description = "Access denied - Customer role required"),
            @ApiResponse(responseCode = "404", description = "Event not found")
    })
    public ResponseEntity<ReservationResponse> reserveTickets(
            @Valid @RequestBody ReservationRequest request,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        ReservationResponse reservation = ticketService.reserveTickets(request, userDetails.getId());
        return new ResponseEntity<>(reservation, HttpStatus.CREATED);
    }

    @PostMapping("/purchase")
    @PreAuthorize("hasRole('CUSTOMER')")
    @Operation(summary = "Purchase tickets", description = "Complete purchase for reserved tickets (Customer only)")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Tickets purchased successfully",
                    content = @Content(schema = @Schema(implementation = PurchaseResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid reservation or expired"),
            @ApiResponse(responseCode = "402", description = "Payment processing failed"),
            @ApiResponse(responseCode = "403", description = "Access denied - Customer role required"),
            @ApiResponse(responseCode = "404", description = "Reservation not found"),
            @ApiResponse(responseCode = "409", description = "Duplicate purchase request")
    })
    public ResponseEntity<PurchaseResponse> purchaseTickets(
            @Valid @RequestBody PurchaseRequest request,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        PurchaseResponse purchase = ticketService.purchaseTickets(request, userDetails.getId());
        return new ResponseEntity<>(purchase, HttpStatus.CREATED);
    }

    @GetMapping("/my-reservations")
    @PreAuthorize("hasRole('CUSTOMER')")
    @Operation(summary = "Get my reservations", description = "Retrieve all reservations for the current user")
    @ApiResponse(responseCode = "200", description = "Reservations retrieved successfully")
    public ResponseEntity<List<ReservationResponse>> getMyReservations(
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        List<ReservationResponse> reservations = ticketService.getUserReservations(userDetails.getId());
        return ResponseEntity.ok(reservations);
    }

    @GetMapping("/my-purchases")
    @PreAuthorize("hasRole('CUSTOMER')")
    @Operation(summary = "Get my purchases", description = "Retrieve all purchases for the current user")
    @ApiResponse(responseCode = "200", description = "Purchases retrieved successfully")
    public ResponseEntity<List<PurchaseResponse>> getMyPurchases(
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        List<PurchaseResponse> purchases = ticketService.getUserPurchases(userDetails.getId());
        return ResponseEntity.ok(purchases);
    }

    @GetMapping("/reservations/{reservationToken}")
    @PreAuthorize("hasRole('CUSTOMER')")
    @Operation(summary = "Get reservation details", description = "Retrieve details of a specific reservation")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Reservation found",
                    content = @Content(schema = @Schema(implementation = ReservationResponse.class))),
            @ApiResponse(responseCode = "403", description = "Access denied"),
            @ApiResponse(responseCode = "404", description = "Reservation not found")
    })
    public ResponseEntity<ReservationResponse> getReservation(
            @PathVariable String reservationToken,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        ReservationResponse reservation = ticketService.getReservation(reservationToken, userDetails.getId());
        return ResponseEntity.ok(reservation);
    }
}
