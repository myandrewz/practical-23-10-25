package dev.brightkan.ticket_line.repository;

import dev.brightkan.ticket_line.model.entity.TicketReservation;
import dev.brightkan.ticket_line.model.enums.ReservationStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface TicketReservationRepository extends JpaRepository<TicketReservation, Long> {

    Optional<TicketReservation> findByReservationToken(String reservationToken);

    List<TicketReservation> findByUserIdAndStatus(Long userId, ReservationStatus status);

    List<TicketReservation> findByEventIdAndStatus(Long eventId, ReservationStatus status);

    @Query("SELECT tr FROM TicketReservation tr WHERE tr.status = :status AND tr.expiresAt < :currentTime")
    List<TicketReservation> findExpiredReservations(@Param("status") ReservationStatus status, @Param("currentTime") LocalDateTime currentTime);

    @Query("SELECT tr FROM TicketReservation tr WHERE tr.user.id = :userId ORDER BY tr.createdAt DESC")
    List<TicketReservation> findByUserIdOrderByCreatedAtDesc(@Param("userId") Long userId);

    boolean existsByReservationToken(String reservationToken);
}
