namespace questionthree.Models
{
    public class Reservation
    {
        public int Id { get; set; }
        public string UserEmail { get; set; } = default!;
        public string EventName { get; set; } = default!;
        public DateTime ReservedAt { get; set; } = DateTime.UtcNow;
        public bool IsConfirmed { get; set; }
    }
}
