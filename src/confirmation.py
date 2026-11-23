from src.database import get_order, get_return, set_return_status

PENDING = "pending_confirmation"
NOT_FOUND = {"error": "Return request not found."}


def resolve_return(conn, customer_id, return_id, new_status):
    request = get_return(conn, return_id)
    if request is None:
        return dict(NOT_FOUND)

    order = get_order(conn, request["order_id"])
    if order["customer_id"] != customer_id:
        return dict(NOT_FOUND)
    if request["status"] != PENDING:
        return {"error": "This request is not waiting for confirmation."}

    set_return_status(conn, return_id, new_status)
    return {"return_id": return_id, "status": new_status}


def confirm_return(conn, customer_id, return_id):
    return resolve_return(conn, customer_id, return_id, "confirmed")


def decline_return(conn, customer_id, return_id):
    return resolve_return(conn, customer_id, return_id, "cancelled")
