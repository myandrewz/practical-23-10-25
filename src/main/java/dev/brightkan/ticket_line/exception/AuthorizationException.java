package dev.brightkan.ticket_line.exception;

public class AuthorizationException extends TicketLineException {

    public AuthorizationException(String message) {
        super(message);
    }

    public AuthorizationException(String message, Throwable cause) {
        super(message, cause);
    }
}
