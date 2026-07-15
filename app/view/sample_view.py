from app.model.sample import Sample


def format_sample_table(samples: list[Sample]) -> str:
    if not samples:
        return "등록된 시료가 없습니다."

    header = f"{'ID':<10}{'이름':<20}{'평균생산시간':<14}{'수율':<8}{'재고':<8}"
    rows = [
        f"{s.sample_id:<10}{s.name:<20}{s.avg_production_time:<14}"
        f"{s.yield_rate:<8}{s.stock_quantity:<8}"
        for s in samples
    ]
    return "\n".join([header, *rows])
