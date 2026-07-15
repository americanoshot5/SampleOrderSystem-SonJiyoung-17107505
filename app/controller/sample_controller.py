from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


class SampleController:
    def __init__(self, repository: SampleRepository):
        self._repository = repository

    def register_sample(self, sample: Sample) -> str:
        try:
            self._repository.create(sample)
        except ValueError as e:
            return f"등록 실패: {e}"
        return f"시료 '{sample.name}' 등록 완료."
