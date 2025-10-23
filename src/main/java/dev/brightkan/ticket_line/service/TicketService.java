package dev.brightkan.ticket_line.service;

import dev.brightkan.ticket_line.dto.PurchaseRequest;
import dev.brightkan.ticket_line.dto.PurchaseResponse;
import dev.brightkan.ticket_line.dto.ReservationRequest;
import dev.brightkan.ticket_line.dto.ReservationResponse;
import dev.brightkan.ticket_line.exception.*;
import dev.brightkan.ticket_line.model.entity.Event;
import dev.brightkan.ticket_line.model.entity.TicketPurchase;
import dev.brightkan.ticket_line.model.entity.TicketReservation;
import dev.brightkan.ticket_line.model.entity.User;
import dev.brightkan.ticket_line.model.enums.ReservationStatus;
import dev.brightkan.ticket_line.repository.EventRepository;
import dev.brightkan.ticket_line.repository.TicketPurchaseRepository;
import dev.brightkan.ticket_line.repository.TicketReservationRepository;
import jakarta.persistence.OptimisticLockException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class TicketService {

    private final TicketReservationRepository reservationRepository;
    private final TicketPurchaseRepository purchaseRepository;
    private final EventRepository eventRepository;
    private final UserService userService;
    private final PaymentService paymentService;

    @Value("${ticket.reservation.expiration.minutes:15}")
    private int reservationExpirationMinutes;

    @Transactional
    public ReservationResponse reserveTickets(ReservationRequest request, Long userId) {
        log.info("Creating reservation for user: {}, event: {}, quantity: {}",
                userId, request.getEventId(), request.getQuantity());

        User user = userService.getUserById(userId);
        Event event = eventRepository.findById(request.getEventId())
                .orElseThrow(() -> new EventNotFoundException(request.getEventId()));

        // Check if event has passed
        if (event.getEventDate().isBefore(LocalDateTime.now())) {
            throw new InsufficientTicketsException("Cannot reserve tickets for past events");
        }

        // Generate unique reservation token
        String reservationToken = generateReservationToken();

        // Check for duplicate reservation token (extremely unlikely but defensive)
        while (reservationRepository.existsByReservationToken(reservationToken)) {
            reservationToken = generateReservationToken();
        }

        try {
            // Attempt to decrement available tickets atomically
            int updated = eventRepository.decrementAvailableTickets(
                    request.getEventId(),
                    request.getQuantity()
            );

            if (updated == 0) {
                // Not enough tickets available
                throw new InsufficientTicketsException(
                        request.getEventId(),
                        request.getQuantity(),
                        event.getAvailableTickets()
                );
            }

            // Calculate expiration time
            LocalDateTime expiresAt = LocalDateTime.now().plusMinutes(reservationExpirationMinutes);

            // Create reservation
            TicketReservation reservation = TicketReservation.builder()
                    .user(user)
                    .event(event)
                    .quantity(request.getQuantity())
                    .totalAmount(event.getTicketPrice().multiply(java.math.BigDecimal.valueOf(request.getQuantity())))
                    .reservationToken(reservationToken)
                    .expiresAt(expiresAt)
                    .status(ReservationStatus.ACTIVE)
                    .build();

            TicketReservation savedReservation = reservationRepository.save(reservation);

            log.info("Reservation created successfully: {} (Token: {})",
                    savedReservation.getId(), savedReservation.getReservationToken());

            return toReservationResponse(savedReservation);

        } catch (OptimisticLockException ex) {
            log.error("Concurrent update conflict for event: {}", request.getEventId());
            throw new InsufficientTicketsException("Unable to reserve tickets due to high demand. Please try again.");
        }
    }

    @Transactional
    public PurchaseResponse purchaseTickets(PurchaseRequest request, Long userId) {
        log.info("Processing purchase for reservation: {}, user: {}", request.getReservationToken(), userId);

        // Find reservation
        TicketReservation reservation = reservationRepository.findByReservationToken(request.getReservationToken())
                .orElseThrow(() -> new ReservationNotFoundException("Reservation not found: " + request.getReservationToken()));

        // Verify the reservation belongs to the user
        if (!reservation.getUser().getId().equals(userId)) {
            throw new AuthorizationException("Reservation does not belong to the current user");
        }

        // Check if already purchased
        if (reservation.getStatus() == ReservationStatus.PURCHASED) {
            // Check if purchase already exists
            TicketPurchase existingPurchase = purchaseRepository.findByReservationId(reservation.getId())
                    .orElseThrow(() -> new DuplicateOperationException("Reservation already purchased"));
            return toPurchaseResponse(existingPurchase);
        }

        // Check if reservation has expired
        if (reservation.getStatus() == ReservationStatus.EXPIRED ||
                reservation.getExpiresAt().isBefore(LocalDateTime.now())) {
            reservation.setStatus(ReservationStatus.EXPIRED);
            reservationRepository.save(reservation);
            throw new ReservationExpiredException("Reservation has expired: " + request.getReservationToken());
        }

        // Generate idempotency key if not provided
        String idempotencyKey = request.getIdempotencyKey();
        if (idempotencyKey == null) {
            idempotencyKey = "PURCHASE-" + request.getReservationToken();
        }

        // Check if purchase already exists with this idempotency key
        String finalIdempotencyKey = idempotencyKey;
        purchaseRepository.findByPaymentReference("IDEM-" + finalIdempotencyKey)
                .ifPresent(existingPurchase -> {
                    throw new DuplicateOperationException("Purchase already processed with this idempotency key");
                });

        // Process payment
        String paymentReference;
        try {
            paymentReference = paymentService.processPayment(
                    reservation.getReservationToken(),
                    reservation.getTotalAmount(),
                    idempotencyKey
            );
        } catch (PaymentProcessingException ex) {
            log.error("Payment processing failed for reservation: {}", request.getReservationToken());
            throw ex;
        }

        // Generate purchase token
        String purchaseToken = generatePurchaseToken();

        // Create purchase
        TicketPurchase purchase = TicketPurchase.builder()
                .user(reservation.getUser())
                .event(reservation.getEvent())
                .reservation(reservation)
                .quantity(reservation.getQuantity())
                .totalAmount(reservation.getTotalAmount())
                .purchaseToken(purchaseToken)
                .paymentReference(paymentReference)
                .build();

        TicketPurchase savedPurchase = purchaseRepository.save(purchase);

        // Update reservation status
        reservation.setStatus(ReservationStatus.PURCHASED);
        reservationRepository.save(reservation);

        log.info("Purchase completed successfully: {} (Token: {})",
                savedPurchase.getId(), savedPurchase.getPurchaseToken());

        return toPurchaseResponse(savedPurchase);
    }

    @Transactional(readOnly = true)
    public List<ReservationResponse> getUserReservations(Long userId) {
        List<TicketReservation> reservations = reservationRepository.findByUserIdOrderByCreatedAtDesc(userId);
        return reservations.stream()
                .map(this::toReservationResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<PurchaseResponse> getUserPurchases(Long userId) {
        List<TicketPurchase> purchases = purchaseRepository.findByUserIdOrderByPurchasedAtDesc(userId);
        return purchases.stream()
                .map(this::toPurchaseResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public ReservationResponse getReservation(String reservationToken, Long userId) {
        TicketReservation reservation = reservationRepository.findByReservationToken(reservationToken)
                .orElseThrow(() -> new ReservationNotFoundException("Reservation not found: " + reservationToken));

        // Verify ownership
        if (!reservation.getUser().getId().equals(userId)) {
            throw new AuthorizationException("Reservation does not belong to the current user");
        }

        return toReservationResponse(reservation);
    }

    @Transactional
    public void cleanupExpiredReservations() {
        log.info("Starting cleanup of expired reservations");

        List<TicketReservation> expiredReservations = reservationRepository.findExpiredReservations(
                ReservationStatus.ACTIVE,
                LocalDateTime.now()
        );

        for (TicketReservation reservation : expiredReservations) {
            log.info("Expiring reservation: {} (Token: {})", reservation.getId(), reservation.getReservationToken());

            // Mark as expired
            reservation.setStatus(ReservationStatus.EXPIRED);
            reservationRepository.save(reservation);

            // Return tickets to available pool
            eventRepository.incrementAvailableTickets(reservation.getEvent().getId(), reservation.getQuantity());
        }

        log.info("Cleanup completed. Expired {} reservations", expiredReservations.size());
    }

    private String generateReservationToken() {
        return "RES-" + UUID.randomUUID().toString().toUpperCase();
    }

    private String generatePurchaseToken() {
        return "PUR-" + UUID.randomUUID().toString().toUpperCase();
    }

    private ReservationResponse toReservationResponse(TicketReservation reservation) {
        return ReservationResponse.builder()
                .id(reservation.getId())
                .userId(reservation.getUser().getId())
                .eventId(reservation.getEvent().getId())
                .eventName(reservation.getEvent().getName())
                .quantity(reservation.getQuantity())
                .totalAmount(reservation.getTotalAmount())
                .reservationToken(reservation.getReservationToken())
                .status(reservation.getStatus())
                .expiresAt(reservation.getExpiresAt())
                .createdAt(reservation.getCreatedAt())
                .build();
    }

    private PurchaseResponse toPurchaseResponse(TicketPurchase purchase) {
        return PurchaseResponse.builder()
                .id(purchase.getId())
                .userId(purchase.getUser().getId())
                .eventId(purchase.getEvent().getId())
                .eventName(purchase.getEvent().getName())
                .quantity(purchase.getQuantity())
                .totalAmount(purchase.getTotalAmount())
                .purchaseToken(purchase.getPurchaseToken())
                .paymentReference(purchase.getPaymentReference())
                .purchasedAt(purchase.getPurchasedAt())
                .build();
    }
}
