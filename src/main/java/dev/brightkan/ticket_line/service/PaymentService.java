package dev.brightkan.ticket_line.service;

import dev.brightkan.ticket_line.exception.PaymentProcessingException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Mock Payment Service - Simulates payment processing
 * In production, this would integrate with real payment gateways like Stripe, PayPal, etc.
 */
@Slf4j
@Service
public class PaymentService {

    // Store processed payment references for idempotency (in-memory for demo)
    private final Map<String, String> processedPayments = new ConcurrentHashMap<>();

    /**
     * Process payment for a reservation
     * @param reservationToken The reservation token
     * @param amount The amount to charge
     * @param idempotencyKey Optional idempotency key for duplicate prevention
     * @return Payment reference
     */
    public String processPayment(String reservationToken, BigDecimal amount, String idempotencyKey) {
        log.info("Processing payment for reservation: {}, amount: {}", reservationToken, amount);

        // Check idempotency - if payment already processed with this key, return existing reference
        if (idempotencyKey != null && processedPayments.containsKey(idempotencyKey)) {
            String existingReference = processedPayments.get(idempotencyKey);
            log.info("Payment already processed with idempotency key: {}, returning existing reference: {}",
                    idempotencyKey, existingReference);
            return existingReference;
        }

        // Simulate payment processing delay
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Mock payment logic - 95% success rate for demonstration
        double random = Math.random();
        if (random < 0.95) {
            // Payment successful
            String paymentReference = "PAY-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();

            // Store for idempotency
            if (idempotencyKey != null) {
                processedPayments.put(idempotencyKey, paymentReference);
            }

            log.info("Payment processed successfully. Reference: {}", paymentReference);
            return paymentReference;
        } else {
            // Payment failed
            log.error("Payment processing failed for reservation: {}", reservationToken);
            throw new PaymentProcessingException("Payment declined by payment processor");
        }
    }

    /**
     * Verify a payment reference
     * @param paymentReference The payment reference to verify
     * @return true if payment reference is valid
     */
    public boolean verifyPayment(String paymentReference) {
        // In a real system, this would check with the payment gateway
        // For our mock, we just check if the reference follows our format
        boolean isValid = paymentReference != null && paymentReference.startsWith("PAY-");
        log.info("Payment verification for {}: {}", paymentReference, isValid ? "VALID" : "INVALID");
        return isValid;
    }

    /**
     * Simulate a refund (for testing purposes)
     * @param paymentReference The payment reference to refund
     */
    public void refundPayment(String paymentReference) {
        log.info("Processing refund for payment reference: {}", paymentReference);
        // In a real system, this would process an actual refund through the payment gateway
        // For our mock, we just log it
        log.info("Refund processed successfully for: {}", paymentReference);
    }
}
