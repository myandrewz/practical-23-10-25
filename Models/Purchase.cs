namespace questionthree.Models
{
    public class Purchase
    {
        public int Id { get; set; }
        public string UserEmail { get; set; } = default!;
        public string EventName { get; set; } = default!;
        public DateTime PurchasedAt { get; set; } = DateTime.UtcNow;
    }

}
