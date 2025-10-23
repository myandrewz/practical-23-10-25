""" 1. Users reserver tickets for an event
2. Payment is confirmed
3. On Success reservations become purchases
4. Downstream services """

"""Minni Challenge: TicketKine Events System With Payments
 - My Code does not capture amounts but confirms paynments
  On Successful payment Reservation Chanes to Purchases and Email is Sent """
from flask import Flask, request, jsonify

app = Flask(__name__)

#Tables for Reservations and Purches
reservations = {}
purchases = {}

# End Point for Reserving Purchase
@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    user_id = data['user_id']
    event_id = data['event_id']
    num_tickets = data['num_tickets']
    reservation_id = f"{user_id}-{event_id}"
    reservations[reservation_id] = {
        'user_id': user_id,
        'event_id': event_id,
        'num_tickets': num_tickets,
        'status': 'reserved'
    }
    return jsonify({'message': 'Reservation successful', 'reservation_id': reservation_id})

# Confirming Payment
@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    reservation_id = data['reservation_id']
    if reservation_id not in reservations:
        return jsonify({'error': 'Reservation not found'}), 404

    # Payment Success
    reservations[reservation_id]['status'] = 'paid'

    # Change reservation to purchase
    purchases[reservation_id] = reservations[reservation_id]
    purchases[reservation_id]['status'] = 'purchased'
    notify_downstream(purchases[reservation_id])

    return jsonify({'message': 'Payment confirmed and purchase completed'})

# Inform downstream services of Payment Success
def notify_downstream(purchase):
    print(f"[Downstream] User {purchase['user_id']} purchased {purchase['num_tickets']} tickets for event {purchase['event_id']}")
    send_email(purchase)
    update_analytics(purchase)

def send_email(purchase):
    print(f"[Email] Confirmation sent to user {purchase['user_id']}")

def update_analytics(purchase):
    print(f"[Analytics] Event {purchase['event_id']} updated with {purchase['num_tickets']} tickets sold")

# View all reservations and purchases
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'reservations': reservations,
        'purchases': purchases
    })

if __name__ == '__main__':
    app.run(debug=True)
