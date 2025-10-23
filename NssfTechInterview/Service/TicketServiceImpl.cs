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
        public TicketServiceImpl(IPaymentService paymentService) {
        
            _paymentService = paymentService;
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

            TicketRepository.Add(reservation);

            return reservation;
        }

        public bool CompletePayment(Guid reservationId)
        {
            var reservation = TicketRepository.Get(reservationId);
            if (reservation == null || reservation.Status != ReservationStatus.Pending)
                return false;

            var success = _paymentService.ProcessPayment(reservation.UserId, reservation.TotalAmount);
            if (success)
            {
                reservation.Status = ReservationStatus.Paid;
                TicketRepository.Update(reservation);
            }

            return success;
        }
    }
}
