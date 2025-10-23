using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using QN_three.Models;

namespace QN_three.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PaymentController : ControllerBase
    {
        private readonly AppDbContext context;

        public PaymentController(AppDbContext context)
        {
            this.context = context;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> get(int id)
        {
            var res = await context.Payments.FindAsync(id);
            if (res == null) return NotFound();
            return Ok(res);
        }

        [HttpGet()]
        public async Task<IActionResult> list() => Ok(await context.Payments.ToListAsync());

        [HttpPost]
        public async Task<IActionResult> create([FromBody] Payments payments)
        {
            payments.CreatedAt = DateTime.Now;
            payments.UpdatedAt = DateTime.Now;
            context.Payments.Add(payments);
            await context.SaveChangesAsync();

            if (!string.IsNullOrEmpty(payments.ResponseCode))
            {
                var reservation = await context.Reservations.FindAsync(payments.ReservationId);
                if (reservation != null)
                {
                    reservation.Status = payments.ResponseCode.Contains("SUCCESS")? "PAID": payments.ResponseCode.Contains("FAILED")?"FAILED": "PENDING";
                    reservation.UpdatedAt = DateTime.Now;
                    context.Reservations.Update(reservation);
                    await context.SaveChangesAsync();

                }
            }

            return Ok(payments);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> put(int id, [FromBody] Payments payments)
        {
            var old = await context.Payments.FindAsync(id);
            if (old == null) return NotFound();
            old.Reference = payments.Reference;
            old.Narration = payments.Narration;
            old.ResponseCode = payments.ResponseCode;
            old.ResponsreDetails = payments.ResponsreDetails;
            old.UpdatedAt = DateTime.Now;
            await context.SaveChangesAsync();

            if (!string.IsNullOrEmpty(payments.ResponseCode))
            {
                var reservation = await context.Reservations.FindAsync(payments.ReservationId);
                if (reservation != null)
                {
                    reservation.Status = payments.ResponseCode.Contains("SUCCESS") ? "PAID" : payments.ResponseCode.Contains("FAILED") ? "FAILED" : "PENDING";
                    reservation.UpdatedAt = DateTime.Now;
                    context.Reservations.Update(reservation);
                    await context.SaveChangesAsync();
                }
            }

            return NoContent();
        }
    }
}
