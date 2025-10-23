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

        public async Task<Purchase?> GetPurchaseById(int id)
        {
            return await db.Purchases.FindAsync(id);
        }

        public async Task<List<Purchase>?> GetPurchases()
        {
            return await db.Purchases.ToListAsync();
        }
    }
}
