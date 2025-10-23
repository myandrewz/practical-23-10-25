using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NssfTechInterview.Models;

namespace NssfTechInterview.DatabaseLayer
{
    public static class TicketRepository
    {
        private static readonly List<TicketReservation> _reservations = new();

        public static TicketReservation Add(TicketReservation reservation)
        {
            _reservations.Add(reservation);
            return reservation;
        }

        public static TicketReservation? Get(Guid id)
        {
            return _reservations.FirstOrDefault(r => r.Id == id);
        }

        public static void Update(TicketReservation reservation)
        {
            var index = _reservations.FindIndex(r => r.Id == reservation.Id);
            if (index != -1)
                _reservations[index] = reservation;
        }

        public static IEnumerable<TicketReservation> GetAll() => _reservations;
    }
}
