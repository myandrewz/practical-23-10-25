using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using QN_three.Models;

namespace QN_three.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EventController : ControllerBase
    {
        private readonly AppDbContext context;

        public EventController(AppDbContext context)
        {
            this.context = context;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> get(int id)
        {
            var res = await context.Events.FindAsync(id);
            if (res == null) return NotFound();
            return Ok(res);
        }

        [HttpGet()]
        public async Task<IActionResult> list() => Ok(await context.Events.ToListAsync());

        [HttpPost]
        public async Task<IActionResult> create([FromBody] Events events)
        {
            events.CreatedAt = DateTime.Now;
            events.UpdatedAt = DateTime.Now;
            context.Events.Add(events);
            await context.SaveChangesAsync();
            return Ok(events);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> put(int id, [FromBody] Events events)
        {
            var old = await context.Events.FindAsync(id);
            if (old == null) return NotFound();
            old.Name = events.Name;
            old.Description = events.Description;
            old.UpdatedAt = DateTime.Now;
            await context.SaveChangesAsync();
            return NoContent();
        }
    }
}
