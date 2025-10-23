using questionthree.Database;
using questionthree.Models;

namespace questionthree.Services
{
    public interface IReservationService
    {
        Task AddReservation(Reservation reservation);
        Task<Reservation?> GetReservationById(int id);
    }

    public class ReservationService : IReservationService
    {
        private readonly AppDbContext db;
        public ReservationService(AppDbContext db)
        {
            this.db = db;
        }
        public async Task AddReservation(Reservation reservation)
        {
            reservation.ReservedAt = DateTime.UtcNow;
            db.Reservations.Add(reservation);
            await db.SaveChangesAsync();
        }

        public async Task<Reservation?> GetReservationById(int id)
        {
            return await db.Reservations.FindAsync(id);
        }
    }

    
}
