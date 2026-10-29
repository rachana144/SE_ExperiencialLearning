
"""Movie theater ticket booking and seating management module."""

import hashlib
import os
import secrets

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve a seat if it exists and is unsold."""
    if order_history is None:
        order_history = []

    if seat_id not in THEATER_SEATS or THEATER_SEATS[seat_id]["is_sold"]:
        return False

    THEATER_SEATS[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Release a seat, returning False if the seat ID does not exist."""
    if seat_id not in THEATER_SEATS:
        return False

    THEATER_SEATS[seat_id]["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True if the seat exists and is available."""
    seat = THEATER_SEATS.get(seat_id)

    if seat is None:
        return False

    return not seat["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Return the discounted seat price; 0.20 means 20% off."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")

    base_price = THEATER_SEATS[seat_id]["price"]
    return base_price * (1 - discount_rate)


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 hex digest for a ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a cryptographically secure four-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the seating chart to a file."""
    with open(filename, "w", encoding="utf-8") as chart_file:
        for seat_id, details in THEATER_SEATS.items():
            status = "SOLD" if details["is_sold"] else "AVAILABLE"
            chart_file.write(
                f"{seat_id}: {details['tier']} ${details['price']:.2f} "
                f"{status}\n"
            )

    print("Seating chart exported to:", filename)


def get_theater_summary(seats):
    """Return the number of sold seats."""
    return sum(
        1 for details in seats.values() if details["is_sold"]
    )


def main():
    """Run a demo of the booking system."""
    box_office_key = os.environ.get("BOX_OFFICE_KEY")

    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(THEATER_SEATS))
    print(
        "Box office key configured:",
        box_office_key is not None,
    )


if __name__ == "__main__":
    main()
