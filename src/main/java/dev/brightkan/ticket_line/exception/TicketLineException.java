package dev.brightkan.ticket_line.exception;

public class TicketLineException extends RuntimeException {

    public TicketLineException(String message) {
        super(message);
    }

    public TicketLineException(String message, Throwable cause) {
        super(message, cause);
    }
}
