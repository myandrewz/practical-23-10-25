using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static NssfTechInterview.Utils.Enums;

namespace NssfTechInterview.Models
{
    public class TicketReservation
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public int EventId { get; set; }
        public int UserId { get; set; }
        public int Quantity { get; set; }
        public decimal TotalAmount { get; set; }
        public ReservationStatus Status { get; set; } = ReservationStatus.Pending;
    }
}
