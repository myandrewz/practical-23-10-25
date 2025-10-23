using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using QN_three.Models;

namespace QN_three.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ReservationController : ControllerBase
    {
        private readonly AppDbContext context;

        public ReservationController(AppDbContext context)
        {
            this.context = context;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> get(int id)
        {
            var res = await context.Reservations.FindAsync(id);
            if (res == null) return NotFound();
            return Ok(res);
        }

        [HttpGet()]
        public async Task<IActionResult> list() => Ok(await context.Reservations.ToListAsync());

        [HttpPost]
        public async Task<IActionResult> create([FromBody] Reservations  reservations )
        {
            reservations.CreatedAt = DateTime.Now;
            reservations.UpdatedAt = DateTime.Now;
            context.Reservations.Add(reservations);
            await context.SaveChangesAsync();
            return Ok(reservations);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> put(int id, [FromBody] Reservations  reservations)
        {
            var old = await context.Reservations.FindAsync(id);
            if (old == null) return NotFound();
            old.Status = reservations.Status; 
            old.UpdatedAt = DateTime.Now;
            await context.SaveChangesAsync();
            return NoContent();
        }

        [HttpGet]
        [Route("paid/{userid}")]
        public async Task<IActionResult> paid(int userid)
        {
            return Ok(await context.Reservations.Where(x=> x.userid == userid).Include(x=>x.Events).ToListAsync());
        }
}
