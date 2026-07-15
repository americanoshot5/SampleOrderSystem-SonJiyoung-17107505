PREFIX = "S-"


def generate_next_sample_id(existing_sample_ids: list[str]) -> str:
    sequences = [
        int(sample_id[len(PREFIX):])
        for sample_id in existing_sample_ids
        if sample_id.startswith(PREFIX) and sample_id[len(PREFIX):].isdigit()
    ]
    next_sequence = max(sequences, default=0) + 1
    return f"{PREFIX}{next_sequence:03d}"
