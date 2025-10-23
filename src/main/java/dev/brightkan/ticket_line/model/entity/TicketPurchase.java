package dev.brightkan.ticket_line.model.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "ticket_purchases", indexes = {
    @Index(name = "idx_purchase_token", columnList = "purchaseToken"),
    @Index(name = "idx_payment_reference", columnList = "paymentReference"),
    @Index(name = "idx_user_purchase", columnList = "user_id"),
    @Index(name = "idx_event_purchase", columnList = "event_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TicketPurchase {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "event_id", nullable = false)
    private Event event;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reservation_id", nullable = false)
    private TicketReservation reservation;

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal totalAmount;

    @Column(unique = true, nullable = false, length = 100)
    private String purchaseToken;

    @Column(unique = true, nullable = false, length = 100)
    private String paymentReference;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime purchasedAt;
}
