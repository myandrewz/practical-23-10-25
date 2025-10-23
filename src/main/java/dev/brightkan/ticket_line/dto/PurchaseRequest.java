package dev.brightkan.ticket_line.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PurchaseRequest {

    @NotBlank(message = "Reservation token is required")
    private String reservationToken;

    private String idempotencyKey; // Optional - for duplicate prevention
}
