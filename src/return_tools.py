from datetime import date

from src.database import create_return, get_order, get_return_for_order
from src.order_tools import NOT_FOUND

RETURN_WINDOW_DAYS = 30


def make_return_tool(conn, customer_id, today=None):
    def request_return(order_id: int, reason: str) -> dict:
        """Start a return request for one of the current customer's delivered orders.

        The request stays pending until the customer confirms it.
        """
        current = today or date.today()
        order = get_order(conn, order_id)
        if order is None or order["customer_id"] != customer_id:
            return dict(NOT_FOUND)
        if order["status"] != "delivered":
            return {"error": "Only delivered orders can be returned."}

        delivered = date.fromisoformat(order["delivered_on"])
        if (current - delivered).days > RETURN_WINDOW_DAYS:
            return {"error": f"The {RETURN_WINDOW_DAYS}-day return window has passed."}
        if get_return_for_order(conn, order_id) is not None:
            return {"error": "A return was already requested for this order."}

        return_id = create_return(conn, order_id, reason, current.isoformat())
        return {
            "return_id": return_id,
            "status": "pending_confirmation",
            "order_id": order_id,
            "product": order["product"],
        }

    return request_return
