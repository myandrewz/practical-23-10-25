package dev.brightkan.ticket_line.exception;

public class InsufficientTicketsException extends TicketLineException {

    public InsufficientTicketsException(String message) {
        super(message);
    }

    public InsufficientTicketsException(Long eventId, Integer requested, Integer available) {
        super(String.format("Insufficient tickets for event ID %d. Requested: %d, Available: %d",
            eventId, requested, available));
    }
}
