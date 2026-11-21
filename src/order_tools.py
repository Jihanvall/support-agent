from src.database import get_order, get_orders_for_customer

PUBLIC_FIELDS = ("id", "product", "status", "total", "ordered_on", "delivered_on")
NOT_FOUND = {"error": "Order not found for this customer."}


def public_view(order):
    return {field: order[field] for field in PUBLIC_FIELDS}


def make_order_tools(conn, customer_id):
    def get_order_status(order_id: int) -> dict:
        """Get the details and status of one of the current customer's orders by its number."""
        order = get_order(conn, order_id)
        if order is None or order["customer_id"] != customer_id:
            return dict(NOT_FOUND)
        return public_view(order)

    def list_my_orders() -> list[dict]:
        """List all orders of the current customer, newest first."""
        return [public_view(order) for order in get_orders_for_customer(conn, customer_id)]

    return get_order_status, list_my_orders
