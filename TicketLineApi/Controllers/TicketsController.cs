using Microsoft.AspNetCore.Mvc;
using NssfTechInterview.DatabaseLayer;
using NssfTechInterview.Models;
using NssfTechInterview.Service;

namespace TicketLineApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TicketsController : ControllerBase
    {
        private readonly ITicketService _service;

        public TicketsController(ITicketService ticketService)
        {
            _service = ticketService;
        }

        // 1️⃣ Reserve tickets
        [HttpPost("reserve")]
        public IActionResult ReserveTickets([FromBody] TicketReservationRequest request)
        {
            var reservation = _service.ReserveTickets(request);

            return Ok(reservation);
        }

        // 2️⃣ Complete payment
        [HttpPost("pay/{reservationId}")]
        public IActionResult Pay(Guid reservationId)
        {
            var success = _service.CompletePayment(reservationId);
            if (!success)
                return BadRequest("Payment failed or reservation not found.");

            return Ok(new { Message = "Payment successful!", Reservation = TicketRepository.Get(reservationId) });
        }

        //List all reservations
        [HttpGet("all")]
        public IActionResult GetAll()
        {
            return Ok(TicketRepository.GetAll());
        }
    }
}
