using Microsoft.AspNetCore.Mvc;
using QN_three.Models;

namespace QN_three.Controllers
{
    public class UserController : ControllerBase
    {
        private readonly AppDbContext context;

        public UserController(AppDbContext context)
        {
            this.context = context;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> get(int id)
        {
            var user = await context.Users.FindAsync(id);
            if (user == null) return NotFound();
            return Ok(user);
        }

        [HttpGet()]
        public async Task<IActionResult> list() => Ok(await context.Users.ToListAsync());

        [HttpPost]
        public async Task<IActionResult> create([FromBody] Users user)
        {
            user.CreatedAt = DateTime.Now;
            user.UpdatedAt = DateTime.Now;
            context.Users.Add(user);
            await context.SaveChangesAsync();
            return Ok(user);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> put(int id, [FromBody] Users user)
        {
            var old = await context.Users.FindAsync(id);
            if (old == null) return NotFound();
            old.Name = user.Name;
            old.Email = user.Email;
            old.UpdatedAt = DateTime.Now;
            await context.SaveChangesAsync();
            return NoContent();
        }


    }
}
