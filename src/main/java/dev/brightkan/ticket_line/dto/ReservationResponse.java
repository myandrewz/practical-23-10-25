package dev.brightkan.ticket_line.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import dev.brightkan.ticket_line.model.enums.ReservationStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReservationResponse {

    private Long id;
    private Long userId;
    private Long eventId;
    private String eventName;
    private Integer quantity;
    private BigDecimal totalAmount;
    private String reservationToken;
    private ReservationStatus status;

    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime expiresAt;

    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;
}
