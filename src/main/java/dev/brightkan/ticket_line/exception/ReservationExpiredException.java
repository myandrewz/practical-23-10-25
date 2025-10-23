package dev.brightkan.ticket_line.exception;

public class ReservationExpiredException extends TicketLineException {

    public ReservationExpiredException(String message) {
        super(message);
    }
}
