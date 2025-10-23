package dev.brightkan.ticket_line.repository;

import dev.brightkan.ticket_line.model.entity.TicketPurchase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TicketPurchaseRepository extends JpaRepository<TicketPurchase, Long> {

    Optional<TicketPurchase> findByPurchaseToken(String purchaseToken);

    Optional<TicketPurchase> findByPaymentReference(String paymentReference);

    List<TicketPurchase> findByUserId(Long userId);

    List<TicketPurchase> findByEventId(Long eventId);

    @Query("SELECT tp FROM TicketPurchase tp WHERE tp.user.id = :userId ORDER BY tp.purchasedAt DESC")
    List<TicketPurchase> findByUserIdOrderByPurchasedAtDesc(@Param("userId") Long userId);

    boolean existsByPurchaseToken(String purchaseToken);

    boolean existsByPaymentReference(String paymentReference);

    Optional<TicketPurchase> findByReservationId(Long reservationId);
}
