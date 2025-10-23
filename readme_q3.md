# 🎟️ TicketKine Event System

A simple Flask app to handle ticket reservations and confirm payments for events.

## 🚀 How It Works

1. Users reserve tickets for an event.
2. Payment is confirmed via a separate endpoint.
3. On success, the reservation becomes a purchase.
4. Downstream services are notified (email and analytics).

## 📦 Endpoints

### `/reserve` (POST)

Reserve tickets for an event.

**Request JSON:**
```json
{
  "user_id": "user123",
  "event_id": "event456",
  "num_tickets": 2
}

```

***Example ***
```
#Testing Reservation
 curl -X POST http://localhost:5000/reserve \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"event_id":101,"num_tickets":2}'

curl -X POST http://localhost:5000/reserve \
  -H "Content-Type: application/json" \
  -d '{"user_id":2,"event_id":101,"num_tickets":4}'


#Testing Confirmation of Payment
curl -X POST http://localhost:5000/pay \
  -H "Content-Type: application/json" \
  -d '{"reservation_id":"1-101"}'

#Testing Confirming Purchae
curl http://localhost:5000/status


