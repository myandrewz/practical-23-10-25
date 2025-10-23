using questionthree.Database;

namespace questionthree.Services
{
    public interface INotificationService
    {
        Task SendPurchaseNotification(string payload);
    }

    public class NotificationService : INotificationService
    {
        private readonly AppDbContext db;
        public NotificationService(AppDbContext db)
        {
            this.db = db;
        }

        public async Task SendPurchaseNotification(string payload)
        {
            // Simulate sending email notification
            await Task.Delay(500);
            Console.WriteLine($"[Notification] {payload}");
        }
    }
}
