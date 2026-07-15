from app.model.sample import Sample
from app.view.sample_view import format_sample_table


def test_format_sample_table_with_samples_includes_header_and_rows():
    samples = [
        Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )
    ]

    result = format_sample_table(samples)

    assert "ID" in result
    assert "이름" in result
    assert "S-001" in result
    assert "실리콘 웨이퍼" in result


def test_format_sample_table_with_empty_list_returns_no_data_message():
    result = format_sample_table([])

    assert result == "등록된 시료가 없습니다."
