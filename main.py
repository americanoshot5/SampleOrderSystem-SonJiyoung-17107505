import sys
from pathlib import Path

from app.controller.sample_controller import SampleController
from app.db import get_connection, init_db
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository

DB_PATH = Path(__file__).parent / "data" / "sample_order.db"


def show_main_menu() -> None:
    print("\n==================== 반도체 시료 생산주문관리 시스템 ====================")
    print("[1] 시료 등록   [2] 시료 목록   [3] 시료 검색   [0] 종료")


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


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    conn = get_connection(DB_PATH)
    init_db(conn)
    controller = SampleController(SampleRepository(conn))

    try:
        while True:
            show_main_menu()
            choice = input("선택 > ").strip()
            if choice == "0":
                print("종료합니다.")
                return
            elif choice == "1":
                print(controller.register_sample(prompt_new_sample()))
            elif choice == "2":
                print(controller.list_samples())
            elif choice == "3":
                keyword = input("검색어(이름) > ").strip()
                print(controller.search_samples(keyword))
            else:
                print("올바른 메뉴를 선택하세요.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
