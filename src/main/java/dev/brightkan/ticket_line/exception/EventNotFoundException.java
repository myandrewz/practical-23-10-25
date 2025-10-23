package dev.brightkan.ticket_line.exception;

public class EventNotFoundException extends TicketLineException {

    public EventNotFoundException(String message) {
        super(message);
    }

    public EventNotFoundException(Long eventId) {
        super("Event not found with ID: " + eventId);
    }
}
