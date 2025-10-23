namespace QN_three.Models
{
    public class Reservations
    {
        public int Id { get; set; }
        public int EventId { get; set; }
        public  decimal Amount { get; set; } = 0;
        public string Status { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set;
    }
}
