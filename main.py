import sys
from datetime import datetime
from pathlib import Path

from app.controller.order_controller import OrderController
from app.controller.sample_controller import SampleController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository

DB_PATH = Path(__file__).parent / "data" / "sample_order.db"


def show_main_menu() -> None:
    print("\n==================== 반도체 시료 생산주문관리 시스템 ====================")
    print("[1] 시료 등록   [2] 시료 목록   [3] 시료 검색   [4] 시료 주문   "
          "[5] 주문 승인/거절   [0] 종료")


def prompt_new_sample() -> Sample:
    sample_id = input("시료 ID > ").strip()
    name = input("이름 > ").strip()
    avg_production_time = float(input("평균 생산시간(min/ea) > ").strip())
    yield_rate = float(input("수율(0~1) > ").strip())
    stock_quantity = int(input("초기 재고 > ").strip())
    return Sample(
        sample_id=sample_id,
        name=name,
        avg_production_time=avg_production_time,
        yield_rate=yield_rate,
        stock_quantity=stock_quantity,
    )


def prompt_new_order() -> tuple[str, str, int]:
    sample_id = input("시료 ID > ").strip()
    customer_name = input("고객명 > ").strip()
    quantity = int(input("주문 수량 > ").strip())
    return sample_id, customer_name, quantity


def handle_order_approval(order_controller: OrderController) -> None:
    print(order_controller.list_reserved_orders())
    order_no = input("승인/거절할 주문번호 > ").strip()
    decision = input("[Y] 승인   [N] 거절 > ").strip().upper()
    if decision == "Y":
        print(order_controller.approve_order(order_no))
    elif decision == "N":
        print(order_controller.reject_order(order_no))
    else:
        print("올바른 선택을 입력하세요.")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    conn = get_connection(DB_PATH)
    init_db(conn)
    sample_repository = SampleRepository(conn)
    sample_controller = SampleController(sample_repository)
    order_controller = OrderController(sample_repository, OrderRepository(conn))

    try:
        while True:
            show_main_menu()
            choice = input("선택 > ").strip()
            if choice == "0":
                print("종료합니다.")
                return
            elif choice == "1":
                print(sample_controller.register_sample(prompt_new_sample()))
            elif choice == "2":
                print(sample_controller.list_samples())
            elif choice == "3":
                keyword = input("검색어(이름) > ").strip()
                print(sample_controller.search_samples(keyword))
            elif choice == "4":
                sample_id, customer_name, quantity = prompt_new_order()
                created_at = datetime.now().isoformat(timespec="seconds")
                print(order_controller.place_order(sample_id, customer_name, quantity, created_at))
            elif choice == "5":
                handle_order_approval(order_controller)
            else:
                print("올바른 메뉴를 선택하세요.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
