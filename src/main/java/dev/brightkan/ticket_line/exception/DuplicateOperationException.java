package dev.brightkan.ticket_line.exception;

public class DuplicateOperationException extends TicketLineException {

    public DuplicateOperationException(String message) {
        super(message);
    }
}
