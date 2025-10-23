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
    }
}
