using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NssfTechInterview.Models;

namespace NssfTechInterview.DatabaseLayer
{
    public class TicketRepositoryImpl : ITicketRepository
    {
        private  readonly List<TicketReservation> _reservations = new();

        public  TicketReservation Add(TicketReservation reservation)
        {
            _reservations.Add(reservation);
            return reservation;
        }

        public  TicketReservation? Get(Guid id)
        {
            return _reservations.FirstOrDefault(r => r.Id == id);
        }

        public  void Update(TicketReservation reservation)
        {
            var index = _reservations.FindIndex(r => r.Id == reservation.Id);
            if (index != -1)
                _reservations[index] = reservation;
        }

        public  IEnumerable<TicketReservation> GetAll() => _reservations;
    }
}
