from app.model.sample_numbering import generate_next_sample_id


def test_generate_next_sample_id_with_empty_list_returns_first_id():
    assert generate_next_sample_id([]) == "S-001"


def test_generate_next_sample_id_returns_next_sequence_after_max_existing():
    assert generate_next_sample_id(["S-001", "S-003"]) == "S-004"
