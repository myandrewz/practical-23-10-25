namespace questionthree.Models
{
    public class OutboxEvent
    {
        public int Id { get; set; }
        public string EventType { get; set; } = default!;
        public string Payload { get; set; } = default!;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public bool Processed { get; set; } = false;
    }
}
