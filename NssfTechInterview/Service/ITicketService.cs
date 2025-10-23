using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NssfTechInterview.Models;

namespace NssfTechInterview.Service
{
    public interface ITicketService
    {
        public TicketReservation ReserveTickets(TicketReservationRequest request);
        public bool CompletePayment(Guid reservationId);

    }
}
