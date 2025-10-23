package dev.brightkan.ticket_line.repository;

import dev.brightkan.ticket_line.model.entity.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<Event, Long> {

    List<Event> findByEventDateAfter(LocalDateTime date);

    List<Event> findByAvailableTicketsGreaterThan(Integer tickets);

    @Query("SELECT e FROM Event e WHERE e.eventDate > :date AND e.availableTickets > 0 ORDER BY e.eventDate")
    List<Event> findUpcomingEventsWithAvailableTickets(@Param("date") LocalDateTime date);

    @Modifying
    @Query("UPDATE Event e SET e.availableTickets = e.availableTickets - :quantity WHERE e.id = :eventId AND e.availableTickets >= :quantity")
    int decrementAvailableTickets(@Param("eventId") Long eventId, @Param("quantity") Integer quantity);

    @Modifying
    @Query("UPDATE Event e SET e.availableTickets = e.availableTickets + :quantity WHERE e.id = :eventId")
    int incrementAvailableTickets(@Param("eventId") Long eventId, @Param("quantity") Integer quantity);
}
