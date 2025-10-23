using Microsoft.EntityFrameworkCore;
using questionthree.Models;

namespace questionthree.Database
{

    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Reservation> Reservations => Set<Reservation>();
        public DbSet<Purchase> Purchases => Set<Purchase>();
        public DbSet<OutboxEvent> OutboxEvents => Set<OutboxEvent>();
    }

}
