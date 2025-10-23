package dev.brightkan.ticket_line.exception;

public class PaymentProcessingException extends TicketLineException {

    public PaymentProcessingException(String message) {
        super(message);
    }

    public PaymentProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}
