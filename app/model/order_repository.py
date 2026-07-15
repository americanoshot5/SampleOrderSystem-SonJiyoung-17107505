import sqlite3

from app.model.order import Order


class OrderRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def create(self, order: Order) -> None:
        self._conn.execute(
            "INSERT INTO orders (order_no, sample_id, customer_name, quantity, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (order.order_no, order.sample_id, order.customer_name,
             order.quantity, order.status, order.created_at),
        )
        self._conn.commit()

    def find_by_order_no(self, order_no: str) -> Order | None:
        row = self._conn.execute(
            "SELECT * FROM orders WHERE order_no = ?", (order_no,)
        ).fetchone()
        return self._to_order(row) if row is not None else None

    def find_all(self) -> list[Order]:
        rows = self._conn.execute("SELECT * FROM orders ORDER BY order_no").fetchall()
        return [self._to_order(row) for row in rows]

    def update_status(self, order_no: str, status: str) -> None:
        self._conn.execute(
            "UPDATE orders SET status = ? WHERE order_no = ?",
            (status, order_no),
        )
        self._conn.commit()

    @staticmethod
    def _to_order(row: sqlite3.Row) -> Order:
        return Order(
            order_no=row["order_no"],
            sample_id=row["sample_id"],
            customer_name=row["customer_name"],
            quantity=row["quantity"],
            status=row["status"],
            created_at=row["created_at"],
        )
