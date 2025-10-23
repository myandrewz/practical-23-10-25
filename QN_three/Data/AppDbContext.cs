
using QN_three.Models;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Events> Events { get; set; }
    public DbSet<Payments> Payments { get; set; }
    public DbSet<Users> Users { get; set; }
    public DbSet<Reservations> Reservations { get; set; }

     
}