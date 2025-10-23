using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NssfTechInterview.Models
{
    public class TicketReservationRequest
    {
        public int EventId { get; set; }
        public int UserId { get; set; }
        public int Quantity { get; set; }
        public decimal PricePerTicket { get; set; }

        // Returns a single validation error message or null if valid
        public string? Validate()
        {
            if (EventId <= 0)
                return "EventId must be greater than zero.";

            if (UserId <= 0)
                return "UserId must be greater than zero.";

            if (Quantity <= 0)
                return "Quantity must be at least 1.";

            if (PricePerTicket <= 0)
                return "PricePerTicket must be greater than zero.";

            return null; // ✅ Valid
        }
    }
}
