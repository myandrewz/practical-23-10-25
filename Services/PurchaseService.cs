using Microsoft.EntityFrameworkCore;
using questionthree.Database;
using questionthree.Models;

namespace questionthree.Services
{
    public interface IPurchaseService
    {
        Task<(bool, Purchase)> AddPurchase(int reservationId);
        Task<Purchase?> GetPurchaseById(int id);
        Task<List<Purchase>?> GetPurchases();
    }

    public class PurchaseService : IPurchaseService
    {
        private readonly AppDbContext db;
        private readonly IReservationService reservationService;
        public PurchaseService(AppDbContext db, IReservationService reservationService)
        {
            this.db = db;
            this.reservationService = reservationService;
        }

        /// <summary>
        /// Creates a purchase for the specified reservation and confirms the reservation if it exists.
        /// </summary>
        /// <remarks>The method confirms the reservation before creating the purchase. If the reservation
        /// is not found, no changes are made and the method returns (<see langword="false"/>, default).</remarks>
        /// <param name="reservationId">The unique identifier of the reservation to convert into a purchase. Must correspond to an existing
        /// reservation.</param>
        /// <returns>A tuple containing a Boolean value that indicates whether the purchase was successfully created, and the
        /// resulting Purchase object. If the reservation does not exist, returns (<see langword="false"/>, default).</returns>
        public async Task<(bool, Purchase)> AddPurchase(int reservationId)
        {

            var reservation = await reservationService.GetReservationById(reservationId);
            if (reservation is null) return (false, default!);

            reservation.IsConfirmed = true;
            var purchase = new Purchase
            {
                UserEmail = reservation.UserEmail,
                EventName = reservation.EventName,
                PurchasedAt = DateTime.UtcNow
            };

            db.OutboxEvents.Add(new OutboxEvent
            {
                EventType = "PurchaseCompleted",
                Payload = $"User: {purchase.UserEmail}, Event: {purchase.EventName}"
            });

            db.Purchases.Add(purchase);
            await  db.SaveChangesAsync();

            return (true, purchase);
        }

        /// <summary>
        /// Retrieves a purchase record by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the purchase to retrieve. Must be a positive integer.</param>
        /// <returns>A <see cref="Purchase"/> object representing the purchase with the specified identifier, or <see
        /// langword="null"/> if no matching purchase is found.</returns>
        public async Task<Purchase?> GetPurchaseById(int id)
        {
            return await db.Purchases.FindAsync(id);
        }

        /// <summary>
        /// Asynchronously retrieves all purchase records from the database.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation. The task result contains a list of <see cref="Purchase"/>
        /// objects representing all purchases, or <see langword="null"/> if no purchases are found.</returns>
        public async Task<List<Purchase>?> GetPurchases()
        {
            return await db.Purchases.ToListAsync();
        }
    }
}
