using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NssfTechInterview.Models;

namespace NssfTechInterview.DatabaseLayer
{
    public interface ITicketRepository
    {
        public TicketReservation Add(TicketReservation reservation);
        public TicketReservation? Get(Guid id);
        public void Update(TicketReservation reservation);
        public IEnumerable<TicketReservation> GetAll();
    }
}
