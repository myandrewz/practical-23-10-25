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

        /// <summary>
        /// Adds a new reservation to the database asynchronously and sets its reservation timestamp.
        /// </summary>
        /// <param name="reservation">The reservation to add. Must not be null. The reservation's ReservedAt property will be set to the current
        /// UTC time.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        public async Task AddReservation(Reservation reservation)
        {
            reservation.ReservedAt = DateTime.UtcNow;
            db.Reservations.Add(reservation);
            await db.SaveChangesAsync();
        }

        /// <summary>
        /// Retrieves a reservation by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the reservation to retrieve.</param>
        /// <returns>A <see cref="Reservation"/> object representing the reservation with the specified identifier, or <see
        /// langword="null"/> if no matching reservation is found.</returns>
        public async Task<Reservation?> GetReservationById(int id)
        {
            return await db.Reservations.FindAsync(id);
        }
    }

    
}
