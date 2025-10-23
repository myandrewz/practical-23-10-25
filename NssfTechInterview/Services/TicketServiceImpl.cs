using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NssfTechInterview.DatabaseLayer;
using NssfTechInterview.Models;
using static NssfTechInterview.Utils.Enums;

namespace NssfTechInterview.Service
{
    public class TicketServiceImpl : ITicketService
    {

        private readonly IPaymentService _paymentService;
        private readonly ITicketRepository _repo;
        public TicketServiceImpl(IPaymentService paymentService, ITicketRepository repo) {
        
            _paymentService = paymentService;
            _repo = repo;
        }

        public TicketReservation ReserveTickets(TicketReservationRequest request)
        {

            var total = request.Quantity * request.PricePerTicket;

            var reservation = new TicketReservation
            {
                UserId = request.UserId,
                EventId = request.EventId,
                Quantity = request.Quantity,
                TotalAmount = total
            };

            _repo.Add(reservation);

            return reservation;
        }

        public bool CompletePayment(Guid reservationId)
        {
            var reservation = _repo.Get(reservationId);
            if (reservation == null || reservation.Status != ReservationStatus.Pending)
                return false;

            var success = _paymentService.ProcessPayment(reservation.UserId, reservation.TotalAmount);
            if (success)
            {
                reservation.Status = ReservationStatus.Paid;
                _repo.Update(reservation);
            }

            return success;
        }
    }
}
