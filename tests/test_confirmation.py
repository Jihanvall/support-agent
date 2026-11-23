import pytest

from src.confirmation import confirm_return, decline_return
from src.database import connect, create_return, get_return, init_db


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    return connection


@pytest.fixture
def return_id(conn):
    return create_return(conn, 1001, "too small", "2026-10-20")


def test_confirm_changes_the_status(conn, return_id):
    result = confirm_return(conn, 1, return_id)
    assert result["status"] == "confirmed"
    assert get_return(conn, return_id)["status"] == "confirmed"


def test_decline_cancels_the_request(conn, return_id):
    result = decline_return(conn, 1, return_id)
    assert result["status"] == "cancelled"
    assert get_return(conn, return_id)["status"] == "cancelled"


def test_another_customer_cannot_confirm(conn, return_id):
    result = confirm_return(conn, 2, return_id)
    assert "error" in result
    assert get_return(conn, return_id)["status"] == "pending_confirmation"


def test_unknown_request_is_not_found(conn):
    assert "error" in confirm_return(conn, 1, 999)


def test_cannot_confirm_twice(conn, return_id):
    confirm_return(conn, 1, return_id)
    result = confirm_return(conn, 1, return_id)
    assert "not waiting" in result["error"]
