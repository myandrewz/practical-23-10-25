package dev.brightkan.ticket_line.exception;

public class AuthenticationException extends TicketLineException {

    public AuthenticationException(String message) {
        super(message);
    }

    public AuthenticationException(String message, Throwable cause) {
        super(message, cause);
    }
}
