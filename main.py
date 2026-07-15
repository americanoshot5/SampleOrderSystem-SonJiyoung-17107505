import sys
from datetime import datetime
from pathlib import Path

from app.controller.monitoring_controller import MonitoringController
from app.controller.order_controller import OrderController
from app.controller.production_controller import ProductionController
from app.controller.release_controller import ReleaseController
from app.controller.sample_controller import SampleController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository
from app.view.input_parser import parse_float, parse_int

DB_PATH = Path(__file__).parent / "data" / "sample_order.db"


def prompt_int(prompt: str) -> int:
    while True:
        value = parse_int(input(prompt).strip())
        if value is not None:
            return value
        print("숫자를 입력하세요.")


def prompt_float(prompt: str) -> float:
    while True:
        value = parse_float(input(prompt).strip())
        if value is not None:
            return value
        print("숫자를 입력하세요.")


def show_main_menu(monitoring_controller: MonitoringController) -> None:
    print("\n==================== 반도체 시료 생산주문관리 시스템 ====================")
    print(monitoring_controller.summarize_dashboard())
    print("[1] 시료 등록   [2] 시료 목록   [3] 시료 검색   [4] 시료 주문   "
          "[5] 주문 승인/거절   [6] 생산 라인   [7] 출고 처리   [8] 모니터링   [0] 종료")


def prompt_new_sample() -> Sample:
    sample_id = input("시료 ID > ").strip()
    name = input("이름 > ").strip()
    avg_production_time = prompt_float("평균 생산시간(min/ea) > ")
    yield_rate = prompt_float("수율(0~1) > ")
    stock_quantity = prompt_int("초기 재고 > ")
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
    quantity = prompt_int("주문 수량 > ")
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


def handle_production_line(production_controller: ProductionController) -> None:
    print(production_controller.list_production_queue())
    choice = input("[1] 다음 생산 처리   [0] 뒤로 > ").strip()
    if choice == "1":
        print(production_controller.process_next_production())


def handle_release(release_controller: ReleaseController) -> None:
    print(release_controller.list_confirmed_orders())
    order_no = input("출고할 주문번호 > ").strip()
    print(release_controller.release_order(order_no))


def handle_monitoring(monitoring_controller: MonitoringController) -> None:
    print("\n[상태별 주문 현황]")
    print(monitoring_controller.summarize_order_status())
    print("\n[시료별 재고 현황]")
    print(monitoring_controller.summarize_stock_status())


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    conn = get_connection(DB_PATH)
    init_db(conn)
    sample_repository = SampleRepository(conn)
    sample_controller = SampleController(sample_repository)
    order_repository = OrderRepository(conn)
    order_controller = OrderController(sample_repository, order_repository)
    production_controller = ProductionController(sample_repository, order_repository)
    release_controller = ReleaseController(order_repository)
    monitoring_controller = MonitoringController(order_repository, sample_repository)

    try:
        while True:
            show_main_menu(monitoring_controller)
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
            elif choice == "6":
                handle_production_line(production_controller)
            elif choice == "7":
                handle_release(release_controller)
            elif choice == "8":
                handle_monitoring(monitoring_controller)
            else:
                print("올바른 메뉴를 선택하세요.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
