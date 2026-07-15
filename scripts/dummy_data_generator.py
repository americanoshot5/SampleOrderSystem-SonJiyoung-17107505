import argparse
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db import get_connection, init_db
from app.model.order import Order
from app.model.order_numbering import generate_next_order_no
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_numbering import generate_next_sample_id
from app.model.sample_repository import SampleRepository

DEFAULT_DB_PATH = Path(__file__).parent.parent / "data" / "sample_order.db"

SAMPLE_NAME_POOL = [
    "실리콘 웨이퍼-8인치",
    "GaN 에피택셜-4인치",
    "SiC 파워기판-6인치",
    "포토레지스트-PR7",
    "산화막 웨이퍼-SiO2",
    "질화막 웨이퍼-Si3N4",
    "폴리싱 웨이퍼-12인치",
    "테스트 다이-TD1",
]

CUSTOMER_NAME_POOL = [
    "삼성전자 파운드리",
    "SK하이닉스",
    "LG이노텍",
    "DB하이텍",
    "한양대 반도체연구실",
    "KAIST 나노랩",
]

ORDER_STATUS_POOL = ["RESERVED", "CONFIRMED", "PRODUCING", "RELEASE"]


def generate_samples(repository: SampleRepository, count: int) -> list[str]:
    existing_ids = [sample.sample_id for sample in repository.find_all()]
    generated_ids = []
    for _ in range(count):
        sample_id = generate_next_sample_id(existing_ids)
        repository.create(
            Sample(
                sample_id=sample_id,
                name=random.choice(SAMPLE_NAME_POOL),
                avg_production_time=round(random.uniform(0.1, 1.0), 2),
                yield_rate=round(random.uniform(0.70, 0.99), 2),
                stock_quantity=random.randint(0, 1000),
            )
        )
        existing_ids.append(sample_id)
        generated_ids.append(sample_id)
    return generated_ids


def generate_orders(
    sample_repository: SampleRepository, order_repository: OrderRepository, count: int
) -> list[str]:
    sample_ids = [sample.sample_id for sample in sample_repository.find_all()]
    if not sample_ids:
        raise ValueError("주문을 생성할 시료가 없습니다. 시료를 먼저 생성하세요.")

    existing_order_nos = [order.order_no for order in order_repository.find_all()]
    generated_order_nos = []
    for _ in range(count):
        order_no = generate_next_order_no(existing_order_nos)
        created_at = (datetime.now() - timedelta(minutes=random.randint(0, 10_000))) \
            .isoformat(timespec="seconds")
        order_repository.create(
            Order(
                order_no=order_no,
                sample_id=random.choice(sample_ids),
                customer_name=random.choice(CUSTOMER_NAME_POOL),
                quantity=random.randint(10, 500),
                status=random.choice(ORDER_STATUS_POOL),
                created_at=created_at,
            )
        )
        existing_order_nos.append(order_no)
        generated_order_nos.append(order_no)
    return generated_order_nos


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sample/Order 더미 데이터 생성 도구")
    parser.add_argument("--samples", type=int, default=10, help="생성할 시료 개수 (기본값: 10)")
    parser.add_argument("--orders", type=int, default=20, help="생성할 주문 개수 (기본값: 20)")
    parser.add_argument(
        "--db", type=str, default=str(DEFAULT_DB_PATH),
        help="데이터를 삽입할 SQLite DB 경로 (기본값: ./data/sample_order.db)",
    )
    return parser.parse_args()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()

    conn = get_connection(Path(args.db))
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)

        sample_ids = generate_samples(sample_repository, args.samples)
        print(f"시료 {len(sample_ids)}건 생성 완료: {', '.join(sample_ids)}")

        order_nos = generate_orders(sample_repository, order_repository, args.orders)
        print(f"주문 {len(order_nos)}건 생성 완료: {', '.join(order_nos)}")

        print(f"\nDB 저장 위치: {args.db}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
