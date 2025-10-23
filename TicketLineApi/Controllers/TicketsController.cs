using Microsoft.AspNetCore.Mvc;
using NssfTechInterview.DatabaseLayer;
using NssfTechInterview.Models;
using NssfTechInterview.Service;

namespace TicketLineApi.Controllers
{
    [ApiController]
    [Route("api/V1/[controller]")]
    public class TicketsController : ControllerBase
    {
        private readonly ITicketService _service;
        private readonly ITicketRepository _repo;

        public TicketsController(ITicketService ticketService, ITicketRepository repo)
        {
            _service = ticketService;
            _repo = repo;
        }

        // 1️⃣ Reserve tickets
        [HttpPost("reserve")]
        public IActionResult ReserveTickets([FromBody] TicketReservationRequest request)
        {
            var error = request.Validate();
            if (error != null)
                return BadRequest(new { Message = error });

            var reservation = _service.ReserveTickets(request);

            return Ok(new { Message = "Reservation successful!" });
        }

        // 2️⃣ Complete payment
        [HttpPost("pay/{reservationId}")]
        public IActionResult Pay(Guid reservationId)
        {
            var success = _service.CompletePayment(reservationId);
            if (!success)
                return BadRequest("Payment failed or reservation not found.");

            return Ok(new { Message = "Payment successful!", Reservation = _repo.Get(reservationId) });
        }

        //List all reservations
        [HttpGet("all")]
        public IActionResult GetAll()
        {
            return Ok(_repo.GetAll());
        }
    }
}
