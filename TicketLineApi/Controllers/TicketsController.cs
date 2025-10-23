using System.IdentityModel.Tokens.Jwt;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using NssfTechInterview.DatabaseLayer;
using NssfTechInterview.Models;
using NssfTechInterview.Models.Dtos;
using NssfTechInterview.Service;

namespace TicketLineApi.Controllers
{
    [ApiController]
    [Route("api/V1/[controller]")]
    public class TicketsController : ControllerBase
    {
        private readonly ITicketService _service;
        private readonly ITicketRepository _repo;

        private readonly IConfiguration _config;

        public TicketsController(ITicketService ticketService, ITicketRepository repo, IConfiguration config)
        {
            _service = ticketService;
            _repo = repo;
            _config = config;
        }
        [HttpPost("GetToken")]
        [AllowAnonymous]
        public IActionResult Login([FromBody] TokenRequest login)
        {
            if (login.UserName == "user" && login.Password == "12345")
            {
                var tokenString = GenerateJwtToken(login.UserName);

                return Ok(new
                {
                    Token = tokenString,
                    ExpiresIn = 3600 // seconds
                });

               
            }
            return Unauthorized();

        }

        // 1️⃣ Reserve tickets
        [HttpPost("reserve")]
        [Authorize]
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
        [Authorize]
        public IActionResult Pay(Guid reservationId)
        {
            var success = _service.CompletePayment(reservationId);
            if (!success)
                return BadRequest("Payment failed or reservation not found.");

            return Ok(new { Message = "Payment successful!", Reservation = _repo.Get(reservationId) });
        }

        //List all reservations
        [HttpGet("all")]
        [Authorize]
        public IActionResult GetAll()
        {
            return Ok(_repo.GetAll());
        }

        private string GenerateJwtToken(string username)
        {
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                _config["Jwt:Issuer"],
                _config["Jwt:Audience"],
                expires: DateTime.Now.AddHours(1),
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
