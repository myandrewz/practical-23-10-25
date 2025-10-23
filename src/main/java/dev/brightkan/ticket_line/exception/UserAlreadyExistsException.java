package dev.brightkan.ticket_line.exception;

public class UserAlreadyExistsException extends TicketLineException {

    public UserAlreadyExistsException(String message) {
        super(message);
    }
}
